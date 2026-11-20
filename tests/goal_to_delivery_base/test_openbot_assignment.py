from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from tests.goal_to_delivery_base.support import RepositoryTestCase, SKILL_ROOT, file_tree_snapshot
from scripts.errors import ValidationError
from scripts.workflow_init import ProviderObservedWork


class OpenBotAssignmentTests(RepositoryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.worktree = self.linked_worktree("issue-branch")
        self.lead = self.manager(self.worktree)

    def check(self, descriptor: dict, *, issue: str = "LUCH-180", **overrides: str):
        arguments = {
            "repository-root": os.fspath(self.worktree),
            "repository-key": "test-repository",
            "workflow-id": descriptor["workflowId"],
            "artifact-folder": descriptor["artifactFolder"],
            "issue-id": issue,
            "completion-boundary": descriptor["completionBoundary"],
            "state-home": os.fspath(self.state_base),
            **overrides,
        }
        command = [sys.executable, os.fspath(SKILL_ROOT / "scripts/cli.py"), "verify-assignment"]
        for key, value in arguments.items():
            command.extend([f"--{key}", value])
        return subprocess.run(command, capture_output=True, text=True, check=False)

    def test_matches_observed_tracker_issue_registered_in_this_worktree(self) -> None:
        descriptor = self.lead.initialize_provider(
            observed_work=ProviderObservedWork("linear", "LUCH-180", "provider-read"),
            workflow="autonomous",
            goal="Show the assigned project",
            completion_boundary="pr",
        )
        before = file_tree_snapshot(self.state_base)
        result = self.check(descriptor)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({"status": "verified", "workflowId": descriptor["workflowId"]}, json.loads(result.stdout))
        for change in (
            {"issue-id": "LUCH-181"},
            {"completion-boundary": "merge"},
            {"artifact-folder": str(Path(descriptor["artifactFolder"]).parent)},
            {"repository-root": str(self.repository)},
            {"repository-root": str(Path(descriptor["artifactFolder"]))},
            {"local-work-key": descriptor["workKey"]},
        ):
            with self.subTest(change=change):
                result = self.check(descriptor, **change)
                self.assertEqual(2, result.returncode)
                self.assertEqual("failed", json.loads(result.stderr)["status"])
                self.assertFalse(result.stdout)
        self.assertEqual(before, file_tree_snapshot(self.state_base))
        self.assertEqual(descriptor, self.lead.resume(workflow_id=descriptor["workflowId"]))
        for unsupported in ("OTHER-1", "luch-1", "LUCH-01", "../LUCH-1"):
            with self.subTest(unsupported=unsupported), self.assertRaises(ValidationError):
                ProviderObservedWork("linear", unsupported, "provider-read")

    def test_fixture_maps_its_issue_to_local_key_without_real_tracker_authority(self) -> None:
        descriptor = self.lead.initialize_local(workflow="semi-autonomous", goal="Show a fixture welcome")
        mapping = {"local-work-key": descriptor["workKey"]}
        result = self.check(descriptor, issue="DEMO-1", **mapping)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(2, self.check(descriptor, issue="DEMO-1").returncode)
        self.assertEqual(2, self.check(descriptor, issue="DEMO-1", **{"local-work-key": "999"}).returncode)
        self.assertEqual(2, self.check(descriptor, issue=" ", **mapping).returncode)
        publish = self.lead.initialize_local(workflow="semi-autonomous", goal="Local fixture", completion_boundary="pr")
        self.assertEqual(2, self.check(publish, issue="DEMO-2", **{"local-work-key": publish["workKey"]}).returncode)
        self.assertEqual({"provider": "none", "externalId": None}, descriptor["tracking"])

    def test_verification_neither_creates_missing_state_nor_recovers_a_transaction(self) -> None:
        descriptor = self.lead.initialize_local(workflow="semi-autonomous", goal="Verify a registration")
        local = {"local-work-key": descriptor["workKey"]}
        missing = self.root / "missing-state"
        result = self.check(descriptor, **local, **{"state-home": str(missing)})
        self.assertEqual(2, result.returncode)
        self.assertFalse(missing.exists())

        pending = self.lead.home.repository / "transactions" / "interrupted.json"
        pending.parent.mkdir(exist_ok=True)
        pending.write_text("Interrupted operation", encoding="utf-8")
        before = file_tree_snapshot(self.state_base)
        result = self.check(descriptor, **local)
        self.assertEqual(2, result.returncode)
        self.assertIn("needs recovery", json.loads(result.stderr)["error"])
        self.assertEqual(before, file_tree_snapshot(self.state_base))
