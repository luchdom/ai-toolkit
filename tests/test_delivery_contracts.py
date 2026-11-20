"""Semantic regression tests for the three delivery workflows."""
from __future__ import annotations

import json
import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_aggregate_validation():
    spec = importlib.util.spec_from_file_location("ai_toolkit_aggregate_validation", ROOT / "scripts" / "validate.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load scripts/validate.py for contract tests.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


aggregate_validation = load_aggregate_validation()

from validation.delivery_contracts import (
    CANONICAL_REFERENCES,
    DOCS_AI_ALLOWLIST,
    SHARED_REFERENCES,
    STAGE_REFERENCES,
    WORKFLOW_ROUTES,
    check_artifact_layout,
    check_canonical_references,
    check_docs_ai_allowlist,
    check_entry_policies,
    check_forbidden_operational_terms,
    check_projection_manifest,
    check_shared_specialists_and_routing,
    check_tool_instruction_cutover,
    check_worktree_policy,
    validate_repository,
)


def write(root: Path, relative: str | Path, content: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def valid_schema() -> str:
    names = {
        "schemaVersion",
        "workflowId",
        "workflow",
        "workSource",
        "workKey",
        "slug",
        "repositoryKey",
        "repositoryRoot",
        "goal",
        "acceptanceCriteria",
        "nonGoals",
        "tracking",
        "completionBoundary",
        "physicalWorktreeFingerprint",
        "riskFlags",
    }
    return json.dumps(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                **{name: {} for name in sorted(names)},
                "schemaVersion": {"const": "2.0"},
                "workflow": {"enum": ["autonomous", "semi-autonomous", "manual"]},
                "workSource": {"enum": ["linear", "local"]},
                "completionBoundary": {"enum": ["artifact", "working-tree", "commit", "pr", "merge"]},
            },
            "required": sorted(names),
        }
    )


def canonical_fixture(root: Path) -> None:
    for reference in CANONICAL_REFERENCES:
        content = valid_schema() if reference.suffix == ".json" else f"# {reference.name}\n"
        write(root, reference, content)
    for source, targets in WORKFLOW_ROUTES.items():
        links = []
        for target in targets:
            relative = Path(os.path.relpath(target, start=source.parent)).as_posix()
            links.append(f"- [{target.name}]({relative})")
        write(root, source, "\n".join(links))


class DeliveryContractTests(unittest.TestCase):
    def test_repository_satisfies_delivery_contracts(self) -> None:
        self.assertEqual([], validate_repository(ROOT))

    def test_historical_docs_ai_is_not_operational_doctrine(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            legacy_root = "docs" + "-ai"
            write(root, f"{legacy_root}/history/old.md", "Ready for Codex used Slack for LUC-42")
            self.assertEqual([], check_forbidden_operational_terms(root))

    def test_retired_operational_terms_fail(self) -> None:
        cases = (
            "Ready for Codex",
            "Send the approval through Slack",
            "Send the approval through Telegram",
            "Use LUC-42 for the current SaaS issue",
            "Skill references are portable summaries, not the source of truth",
        )
        for index, content in enumerate(cases):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write(root, f"docs/current-{index}.md", content)
                self.assertTrue(check_forbidden_operational_terms(root))

    def test_missing_and_competing_canonical_references_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical_fixture(root)
            self.assertEqual([], check_canonical_references(root))
            (root / STAGE_REFERENCES / "design-gates.md").unlink()
            write(root, "src/skills/goal-to-delivery/references/design-gates.md", "competing copy")
            findings = check_canonical_references(root)
            self.assertTrue(any("Missing canonical" in finding for finding in findings))
            self.assertTrue(any("Competing delivery reference" in finding for finding in findings))
            self.assertTrue(any("broken local reference" in finding for finding in findings))

    def test_workflow_route_cannot_skip_goal_to_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical_fixture(root)
            loop = root / "src/skills/linear-delivery-loop/SKILL.md"
            text = loop.read_text(encoding="utf-8")
            loop.write_text(text.replace("../goal-to-delivery/", "../spec-driven-delivery/"), encoding="utf-8")
            findings = check_canonical_references(root)
            self.assertTrue(any("missing canonical reference links" in item and "goal-to-delivery" in item for item in findings))

    def test_renamed_normative_protocol_copy_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical_fixture(root)
            first_block = (
                "The canonical stage owner must produce independently reviewable evidence, preserve the active "
                "entry authority boundary, and return deterministic output to the caller without selecting work."
            )
            second_block = (
                "A completed stage never substitutes for independent audit, exact-diff code review, runtime "
                "acceptance verification, or durable documentation when those gates apply to the requested goal."
            )
            write(
                root,
                STAGE_REFERENCES / "delivery-stages.md",
                f"# Delivery Stages\n\n{first_block}\n\n{second_block}\n",
            )
            write(
                root,
                "src/skills/spec-driven-delivery/references/renamed-policy.md",
                f"# Locally Renamed Policy\n\n{first_block}\n\n{second_block}\n",
            )
            findings = check_canonical_references(root)
            self.assertTrue(any("Competing renamed delivery doctrine" in finding for finding in findings))

    def test_historical_layout_is_read_only_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            legacy_root = "docs" + "-ai"
            write(
                root,
                SHARED_REFERENCES / "artifact-contract.md",
                f".ai/work/ artifactFolder exact registered legacy {legacy_root} historical read-only",
            )
            write(root, "src/agents/planner.md", f"Use {legacy_root}/<NNN>-<slug>-<YYYY-MM-DD>/")
            findings = check_artifact_layout(root)
            self.assertTrue(any("active producer/consumer" in finding for finding in findings))

    def test_legacy_literal_allowlist_is_path_and_purpose_specific(self) -> None:
        literal = "docs" + "-ai"
        artifact = SHARED_REFERENCES / "artifact-contract.md"
        contract_line = next(line for line in (ROOT / artifact).read_text(encoding="utf-8").splitlines() if literal in line)
        runtime_line = next(
            line
            for line in (
                ROOT / "src/skills/goal-to-delivery/scripts/descriptor.py"
            ).read_text(encoding="utf-8").splitlines()
            if literal in line
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root, artifact, contract_line)
            write(root, Path("dist/codex") / artifact.relative_to("src"), contract_line)
            self.assertEqual([], check_docs_ai_allowlist(root))

            write(root, artifact, contract_line + f"\nCreate current work in {literal}/new-work.\n")
            self.assertTrue(check_docs_ai_allowlist(root), "stale current doctrine must fail in an allowlisted path")

            write(root, artifact, runtime_line)
            self.assertTrue(check_docs_ai_allowlist(root), "an allowed line must fail under the wrong path/purpose")

        for relative in (
            "src/agents/unlisted.md",
            "tests/unreviewed.py",
            "dist/codex/agents/unlisted.toml",
        ):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write(root, relative, runtime_line)
                self.assertTrue(check_docs_ai_allowlist(root), "active source, tests, and dist must all be scanned")

        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.dict(
                DOCS_AI_ALLOWLIST,
                {"README.md": {"unsupported purpose": frozenset()}},
                clear=True,
            ):
                self.assertTrue(check_docs_ai_allowlist(Path(directory)))

    def test_tool_instruction_cutover_rejects_retired_path_and_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src/tool-instructions").mkdir(parents=True)
            self.assertEqual([], check_tool_instruction_cutover(root))

            retired_leaf = "project" + "-templates"
            (root / "src" / retired_leaf).mkdir()
            self.assertTrue(check_tool_instruction_cutover(root))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "src/tool-instructions").mkdir(parents=True)
            retired_name = "Project" + " templates"
            write(root, "README.md", f"Keep {retired_name} here.")
            self.assertTrue(check_tool_instruction_cutover(root))

    def test_tool_instruction_paths_and_identifiers_are_canonical(self) -> None:
        expected = (
            "src/tool-instructions/codex/AGENTS.md",
            "src/tool-instructions/claude/AGENTS.md",
        )
        self.assertTrue(all((ROOT / relative).is_file() for relative in expected))
        self.assertFalse((ROOT / "src" / ("project" + "-templates")).exists())
        for relative in expected:
            instruction = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("`tool-instructions/shared/delivery-workflow.md`", instruction)
            self.assertNotIn("goal-to-delivery/references/", instruction)

        build = (ROOT / "scripts/build.py").read_text(encoding="utf-8")
        sync = (ROOT / "scripts/sync.py").read_text(encoding="utf-8")
        bootstrap = (ROOT / "scripts/bootstrap_existing.py").read_text(encoding="utf-8")
        self.assertIn("def validate_tool_instruction_skills", build)
        self.assertIn("def sync_tool_instructions", sync)
        self.assertIn("SRC_TOOL_INSTRUCTIONS", bootstrap)
        self.assertIn("def write_tool_instructions", bootstrap)

    def test_worktree_policy_requires_the_recorded_commit(self) -> None:
        self.assertEqual([], check_worktree_policy(ROOT))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = SHARED_REFERENCES / "worktrees.md"
            policy = write(root, relative, (ROOT / relative).read_text(encoding="utf-8"))
            self.assertEqual([], check_worktree_policy(root))
            resolved_command = "git worktree add -b <branch> <exact-path> <resolved-base-commit>"
            movable_command = "git worktree add -b <branch> <exact-path> <remote-ref>"
            policy.write_text(
                policy.read_text(encoding="utf-8").replace(resolved_command, movable_command),
                encoding="utf-8",
            )
            findings = check_worktree_policy(root)
            self.assertTrue(
                any("never a movable remote ref" in finding for finding in findings),
                "the policy validator must reject a movable-ref execution command",
            )

    def test_worktree_creation_pins_authorized_commit_when_remote_ref_moves(self) -> None:
        def git(cwd: Path, *args: str) -> str:
            return subprocess.run(
                ["git", *args],
                cwd=cwd,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = root / "repository"
            repository.mkdir()
            git(repository, "init")
            git(repository, "config", "user.name", "Worktree Policy Fixture")
            git(repository, "config", "user.email", "worktree-policy@example.invalid")

            tracked = repository / "tracked.txt"
            tracked.write_text("authorized\n", encoding="utf-8")
            git(repository, "add", "tracked.txt")
            git(repository, "commit", "-m", "authorized base")
            authorized_commit = git(repository, "rev-parse", "HEAD")
            git(repository, "update-ref", "refs/remotes/origin/main", authorized_commit)

            tracked.write_text("advanced\n", encoding="utf-8")
            git(repository, "commit", "-am", "advance movable ref")
            advanced_commit = git(repository, "rev-parse", "HEAD")
            git(repository, "update-ref", "refs/remotes/origin/main", advanced_commit)
            self.assertNotEqual(authorized_commit, advanced_commit)
            self.assertEqual(advanced_commit, git(repository, "rev-parse", "refs/remotes/origin/main"))

            worktrees = root / "worktrees"
            worktrees.mkdir()
            destination = worktrees / "authorized"
            git(
                repository,
                "worktree",
                "add",
                "-b",
                "fixture-authorized",
                str(destination),
                authorized_commit,
            )

            self.assertEqual(authorized_commit, git(destination, "rev-parse", "HEAD"))
            self.assertNotEqual(advanced_commit, git(destination, "rev-parse", "HEAD"))

    def test_entry_policy_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root,
                "src/skills/goal-to-delivery/SKILL.md",
                "automatically working-tree queue selection only when called by the active loop "
                "one focused question Staff Engineer authorized boundary is verified "
                "owner-enabled OpenBot Workflow Coordinator references/openbot-handoff.md",
            )
            write(
                root,
                "src/skills/spec-driven-delivery/SKILL.md",
                "manual exactly one return control one focused question explicit request for that stage "
                "registered `artifactFolder`",
            )
            linear = write(
                root,
                "src/skills/linear-delivery-loop/SKILL.md",
                "autonomous .ai/loop.json autonomous label human-decision label at most one "
                "In Progress Backlog Done continuation issue "
                "DECIDE <ISSUE> CUSTOM <SUGGESTION> notification click target "
                "quiet standalone scheduled run set_thread_archived raw archive directive "
                "record any new decisions verify that Goal to Delivery reached",
            )
            self.assertEqual([], check_entry_policies(root))
            linear.write_text("autonomous helper", encoding="utf-8")
            self.assertTrue(check_entry_policies(root))

    def test_linear_loop_archives_only_quiet_standalone_runs(self) -> None:
        skill = (ROOT / "src/skills/linear-delivery-loop/SKILL.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs/mvp-linear-delivery-loop.md").read_text(encoding="utf-8")

        for fragment in (
            "quiet standalone scheduled run",
            "set_thread_archived",
            "After releasing any acquired lease",
            "Never archive an attended pilot",
            "no newer valid owner decision",
            "If native archiving is unavailable",
        ):
            self.assertIn(fragment, skill)
        self.assertIn("Quiet-run cleanup", guide)
        self.assertIn("Do not archive attended pilots", guide)

    def test_linear_loop_recommends_larger_implementation_budgets(self) -> None:
        config = json.loads(
            (ROOT / "src/skills/linear-delivery-loop/references/project-config.example.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            {
                "maxRunMinutes": 90,
                "maxFiles": 30,
                "maxChangedLines": 5000,
                "maxTestMinutes": 30,
            },
            config["limits"],
        )

    def test_feature_driver_routing_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stages = STAGE_REFERENCES / "delivery-stages.md"
            stage_text = (ROOT / stages).read_text(encoding="utf-8")
            stage_file = write(root, stages, stage_text)
            quality_gates = STAGE_REFERENCES / "quality-gates.md"
            quality_text = (ROOT / quality_gates).read_text(encoding="utf-8")
            quality_file = write(root, quality_gates, quality_text)
            write(
                root,
                SHARED_REFERENCES / "completion-boundaries.md",
                "merge applicable UI design conformance one independent code review applicable QA",
            )
            design_gates = write(
                root,
                STAGE_REFERENCES / "design-gates.md",
                "binding design sources design specification mechanical change design conformance review "
                "every change to rendered UI or interaction real browser PASS FAIL registered `artifactFolder` "
                "reviewed state `--02`",
            )
            for source in (ROOT / "src/agents").glob("*.md"):
                write(root, source.relative_to(ROOT), source.read_text(encoding="utf-8"))
            write(
                root,
                "src/skills/ui-review-spec/SKILL.md",
                "binding design sources exact implementation identity design-review-template.md "
                "real rendered evidence `--02`",
            )
            feature = write(
                root,
                "src/agents/feature-driver.md",
                "---\nname: feature-driver\n---\ncompatibility alias to $goal-to-delivery; never autonomous",
            )
            write(root, "src/skills/docs-as-code/SKILL.md", "durable documentation")
            write(
                root,
                "src/skills/multi-agent-delivery/SKILL.md",
                "$goal-to-delivery $spec-driven-delivery $linear-delivery-loop "
                "caller supplies the stage. queue selection and external actions stay with the caller. "
                "design conformance review",
            )
            self.assertEqual([], check_shared_specialists_and_routing(root))

            quality_file.write_text(
                quality_text.replace("before publishing code or finishing automatic code delivery", "for automatic code delivery"),
                encoding="utf-8",
            )
            self.assertTrue(any("review before code publication" in item for item in check_shared_specialists_and_routing(root)))
            quality_file.write_text(quality_text, encoding="utf-8")

            qa_row = next(line for line in stage_text.splitlines() if line.startswith("| `qa` |"))
            review_row = next(line for line in stage_text.splitlines() if line.startswith("| `review` |"))
            stage_file.write_text(stage_text.replace(f"{qa_row}\n{review_row}", f"{review_row}\n{qa_row}"), encoding="utf-8")
            self.assertTrue(any("out of order" in item for item in check_shared_specialists_and_routing(root)))
            stage_file.write_text(stage_text, encoding="utf-8")

            original_gates = design_gates.read_text(encoding="utf-8")
            design_gates.write_text("binding design sources", encoding="utf-8")
            self.assertTrue(
                any("frontend/UI design gate contract" in item for item in check_shared_specialists_and_routing(root))
            )
            design_gates.write_text(original_gates, encoding="utf-8")

            for role in ("senior-full-stack-engineer", "product-manager", "qa", "staff-engineer"):
                profile = root / f"src/agents/{role}.md"
                original = profile.read_text(encoding="utf-8")
                profile.write_text("Profile without assigned responsibilities", encoding="utf-8")
                self.assertTrue(
                    any(f"{role} delivery responsibilities" in item for item in check_shared_specialists_and_routing(root))
                )
                profile.write_text(original, encoding="utf-8")

            for role in ("product-designer", "code-reviewer"):
                retired = write(root, f"src/agents/{role}.md", "Obsolete profile")
                self.assertTrue(any("retired role is still installable" in item
                                    for item in check_shared_specialists_and_routing(root)))
                retired.unlink()

            feature.write_text(
                "---\nname: feature-driver\n---\ncompatibility $goal-to-delivery never autonomous\n"
                "Required workflow: copied orchestration",
                encoding="utf-8",
            )
            self.assertTrue(
                any("retired orchestration doctrine" in item for item in check_shared_specialists_and_routing(root))
            )

    def test_projection_manifest_detects_source_and_generated_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = write(root, "src/agents/example.md", "canonical")
            output = write(root, "dist/codex/agents/example.toml", "generated")
            (root / "src/skills").mkdir(parents=True)
            (root / "src/tool-instructions").mkdir(parents=True)
            (root / "src/tool-instructions/.DS_Store").write_bytes(b"\xff")

            import hashlib

            manifest = {
                "schemaVersion": 1,
                "canonicalRoot": "src",
                "generatedRoot": "dist",
                "entries": [
                    {
                        "source": "src/agents/example.md",
                        "sourceSha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                        "projections": [
                            {
                                "path": "dist/codex/agents/example.toml",
                                "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                            }
                        ],
                    }
                ],
            }
            write(root, "dist/manifest.json", json.dumps(manifest))
            self.assertEqual([], check_projection_manifest(root))
            output.write_text("drift", encoding="utf-8")
            self.assertTrue(any("projection drift" in item for item in check_projection_manifest(root)))

    def test_aggregate_manifest_is_local_and_complete(self) -> None:
        manifest = json.loads((ROOT / "validation/manifest.json").read_text(encoding="utf-8"))
        names = [step["name"] for step in manifest["steps"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(
            ["command", "command", "unittest-discovery"],
            [step["type"] for step in manifest["steps"]],
        )
        rendered = json.dumps(manifest).casefold()
        self.assertIn("scripts/build.py", rendered)
        self.assertIn("scripts/test_sync_markers.py", rendered)
        self.assertIn('"startdirectory": "tests"', rendered)
        self.assertNotIn("sync.py --tool", rendered)

    def test_aggregate_gate_passes_physical_temp_root_to_children(self) -> None:
        step = {"name": "build", "type": "command", "argv": ["{python}", "scripts/build.py"]}
        temporary_alias = str(ROOT / ".." / ROOT.name)
        with mock.patch.object(aggregate_validation, "load_manifest", return_value={"steps": [step]}), mock.patch.object(
            aggregate_validation.tempfile, "gettempdir", return_value=temporary_alias
        ), mock.patch.object(aggregate_validation.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run:
            self.assertEqual(0, aggregate_validation.main())
        environment = run.call_args.kwargs["env"]
        for name in ("TMPDIR", "TEMP", "TMP"):
            self.assertEqual(str(ROOT.resolve()), environment[name])
        self.assertEqual("1", environment["PYTHONDONTWRITEBYTECODE"])

    def test_aggregate_manifest_accepts_only_fixed_local_shapes(self) -> None:
        safe = {
            "schemaVersion": 1,
            "steps": [
                {
                    "name": "build",
                    "type": "command",
                    "argv": ["{python}", "scripts/build.py"],
                },
                {
                    "name": "tests",
                    "type": "unittest-discovery",
                    "startDirectory": "tests",
                    "pattern": "test*.py",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            manifest = write(Path(directory), "manifest.json", json.dumps(safe))
            self.assertEqual(safe, aggregate_validation.load_manifest(manifest))

    def test_aggregate_manifest_rejects_mutating_or_external_commands(self) -> None:
        unsafe_argv = (
            ["{python}", "scripts/sync.py", "--tool", "all"],
            ["{python}", "scripts/build.py", "scripts/sync.py"],
            ["{python}", "scripts/build.py && scripts/sync.py"],
            ["{python}", "-c", "import scripts.sync"],
            ["{python}", "-m", "pip", "install", "package"],
            ["pwsh", "-File", "scripts/build.py"],
            ["cmd", "/c", "python scripts/build.py"],
            ["bash", "-c", "python scripts/build.py"],
            ["curl", "https://example.invalid"],
            ["gh", "pr", "checks"],
            ["git", "push"],
            ["linear", "issue", "update"],
        )
        for index, argv in enumerate(unsafe_argv):
            with self.subTest(argv=argv), tempfile.TemporaryDirectory() as directory:
                data = {
                    "schemaVersion": 1,
                    "steps": [{"name": f"unsafe-{index}", "type": "command", "argv": argv}],
                }
                manifest = write(Path(directory), "manifest.json", json.dumps(data))
                with self.assertRaisesRegex(aggregate_validation.ManifestError, "not allowlisted"):
                    aggregate_validation.load_manifest(manifest)

    def test_aggregate_manifest_rejects_shell_fields_and_discovery_drift(self) -> None:
        unsafe_steps = (
            {
                "name": "shell-field",
                "type": "command",
                "argv": ["{python}", "scripts/build.py"],
                "shell": True,
            },
            {
                "name": "external-tests",
                "type": "unittest-discovery",
                "startDirectory": "../tests",
                "pattern": "test*.py",
            },
            {
                "name": "arbitrary-pattern",
                "type": "unittest-discovery",
                "startDirectory": "tests",
                "pattern": "*.py",
            },
        )
        for step in unsafe_steps:
            with self.subTest(step=step["name"]), tempfile.TemporaryDirectory() as directory:
                data = {"schemaVersion": 1, "steps": [step]}
                manifest = write(Path(directory), "manifest.json", json.dumps(data))
                with self.assertRaises(aggregate_validation.ManifestError):
                    aggregate_validation.load_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
