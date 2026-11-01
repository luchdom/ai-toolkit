"""External imports preserve local files and restore exact selected skill trees."""
from __future__ import annotations

import contextlib
import io
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

_sync_spec = importlib.util.spec_from_file_location("ai_toolkit_sync", Path(__file__).resolve().parents[1] / "scripts" / "sync.py")
sync = importlib.util.module_from_spec(_sync_spec)
_sync_spec.loader.exec_module(sync)
imports = sync.external_skills


class ExternalSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.home = self.root / "home"
        self.home.mkdir()
        self.source = self.root / "source"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("---\nname: sample\n---\n# Sample\n")
        (self.source / "scripts").mkdir()
        (self.source / "scripts" / "helper.py").write_text("print('helper')\n")
        self.entry = {"name": "sample", "repo": "https://github.com/example/skills.git", "path": "skills/sample", "revision": "a" * 40, "tools": ["codex"]}
        self.canonical = self.root / "canonical"
        self.canonical.mkdir()
        self.target = self.home / ".codex" / "skills" / "sample"
        self.skill_root = self.target.parent
        self.manifest = self.root / "external-skills.toml"

    def write_manifest(self, entries=None) -> Path:
        entries = [self.entry] if entries is None else entries
        rows = ["version = 1", "skills = []" if not entries else ""]
        for entry in entries:
            rows += ["[[skills]]", *(f"{key} = {json.dumps(value)}" for key, value in entry.items())]
        self.manifest.write_text("\n".join(rows) + "\n")
        return self.manifest

    def run_import(self, entries=None, **kwargs) -> None:
        imports.sync_external_skills(entries or [self.entry], {"codex"}, home=self.home, fetcher=lambda *_: self.source, **kwargs)

    def test_sibling_import_ignores_an_unrelated_scripts_package(self) -> None:
        unrelated = types.ModuleType("scripts")
        with mock.patch.dict(sys.modules, {"scripts": unrelated}):
            module = importlib.util.module_from_spec(_sync_spec)
            _sync_spec.loader.exec_module(module)
        self.assertEqual(Path(imports.__file__), Path(module.external_skills.__file__))

    def test_reparse_detection_works_without_path_is_junction(self) -> None:
        metadata = types.SimpleNamespace(st_mode=0o040755, st_file_attributes=0x400)
        with mock.patch.object(Path, "lstat", return_value=metadata):
            self.assertTrue(imports.is_link_or_reparse(self.root))
            with self.assertRaisesRegex(imports.ImportError, "junction"):
                imports.check_path(self.target, self.home)
            with self.assertRaisesRegex(imports.ImportError, "symlink"):
                imports.tree_hashes(self.source)

    def test_boundary_ancestor_symlink_is_rejected_before_writes(self) -> None:
        alias = self.root / "alias"
        alias.symlink_to(self.home, target_is_directory=True)
        project = alias / "selected-project"
        with self.assertRaisesRegex(imports.ImportError, "symlink"):
            imports.preflight([{**self.entry, "tools": ["cursor"]}], {"cursor"}, [project], home=self.home)
        self.assertFalse((self.home / "selected-project").exists())

    def test_manifest_accepts_selected_pinned_skills_and_empty_selection(self) -> None:
        self.assertEqual([self.entry], imports.load_manifest(self.write_manifest(), self.canonical))
        hidden = {**self.entry, "path": "skills/.curated/linear"}
        self.assertEqual([hidden], imports.load_manifest(self.write_manifest([hidden]), self.canonical))
        self.assertEqual([], imports.load_manifest(self.write_manifest([]), self.canonical))

    def test_manifest_rejects_unsafe_or_unknown_fields_before_destination_changes(self) -> None:
        invalid = [
            ("name", "../elsewhere"), ("name", "CON"), ("name", "trailing."),
            ("path", "../sample"), ("path", "/sample"), ("path", "a\\b"),
            ("path", "skills//sample"), ("path", ".git/hooks"),
            ("revision", "main"), ("revision", "A" * 40),
            ("repo", "https://token@github.com/example/skills.git"),
            ("repo", "file:///tmp/skills"), ("repo", "https://github.com/example/skills.git?token=secret"),
            ("tools", ["unknown"]), ("tools", ["codex", "codex"]),
            ("tools", [1]), ("unknown", "value"),
        ]
        for key, value in invalid:
            with self.subTest(key=key, value=value):
                entry = {**self.entry, key: value}
                with self.assertRaises(imports.ImportError):
                    imports.load_manifest(self.write_manifest([entry]), self.canonical)
        self.assertFalse(self.skill_root.exists())

    def test_manifest_rejects_case_alias_and_canonical_collisions(self) -> None:
        with self.assertRaisesRegex(imports.ImportError, "Duplicate"):
            imports.load_manifest(self.write_manifest([self.entry, {**self.entry, "name": "Sample"}]), self.canonical)
        (self.canonical / "Sample").mkdir()
        with self.assertRaisesRegex(imports.ImportError, "repository-owned"):
            imports.load_manifest(self.write_manifest(), self.canonical)

    def test_install_idempotence_and_pinned_update_keep_supporting_files(self) -> None:
        self.run_import()
        self.assertEqual((self.source / "scripts/helper.py").read_bytes(), (self.target / "scripts/helper.py").read_bytes())
        receipt = (self.skill_root / imports.RECEIPT).read_bytes()
        before = (self.target / "SKILL.md").stat().st_mtime_ns
        self.run_import()
        self.assertEqual(before, (self.target / "SKILL.md").stat().st_mtime_ns)
        self.assertEqual(receipt, (self.skill_root / imports.RECEIPT).read_bytes())
        (self.source / "SKILL.md").write_text("# Updated\n")
        updated = {**self.entry, "revision": "b" * 40}
        self.run_import([updated])
        self.assertEqual("# Updated\n", (self.target / "SKILL.md").read_text())
        data = json.loads((self.skill_root / imports.RECEIPT).read_text())
        self.assertEqual("b" * 40, data["skills"]["sample"]["revision"])

    def test_unmanaged_conflict_even_identical_prevents_fetch_and_adoption(self) -> None:
        self.target.mkdir(parents=True)
        (self.target / "SKILL.md").write_bytes((self.source / "SKILL.md").read_bytes())
        fetch = mock.Mock()
        with self.assertRaisesRegex(imports.ImportError, "Unmanaged"):
            imports.sync_external_skills([self.entry], {"codex"}, home=self.home, fetcher=fetch)
        fetch.assert_not_called()
        self.assertFalse((self.skill_root / imports.RECEIPT).exists())

    def test_local_edits_and_added_empty_directories_are_preserved(self) -> None:
        self.run_import()
        for modification in ("file", "directory"):
            with self.subTest(modification=modification):
                if modification == "file":
                    (self.target / "SKILL.md").write_text("# Local\n")
                else:
                    (self.target / "SKILL.md").write_bytes((self.source / "SKILL.md").read_bytes())
                    (self.target / "local-empty").mkdir()
                with self.assertRaisesRegex(imports.ImportError, "Locally modified"):
                    self.run_import()
        self.assertTrue((self.target / "local-empty").exists())

    @unittest.skipIf(os.name == "nt", "Executable mode preservation needs POSIX file modes")
    def test_executable_permission_changes_are_local_modifications(self) -> None:
        self.run_import()
        (self.target / "scripts/helper.py").chmod(0o755)
        with self.assertRaisesRegex(imports.ImportError, "Locally modified"):
            self.run_import()
        self.assertEqual(0o111, (self.target / "scripts/helper.py").stat().st_mode & 0o111)

    def test_receipt_commit_failure_restores_previous_skill_and_receipt(self) -> None:
        self.run_import()
        original = imports.tree_hashes(self.target)
        receipt = (self.skill_root / imports.RECEIPT).read_bytes()
        (self.source / "SKILL.md").write_text("# New\n")
        with mock.patch.object(imports.os, "replace", side_effect=OSError("injected receipt failure")):
            with self.assertRaises(imports.ImportError):
                self.run_import([{**self.entry, "revision": "b" * 40}])
        self.assertEqual(original, imports.tree_hashes(self.target))
        self.assertEqual(receipt, (self.skill_root / imports.RECEIPT).read_bytes())
        self.assertFalse(list(self.skill_root.glob(".ai-toolkit-import-*")))

    def test_failed_rollback_retains_previous_files_and_receipt_for_recovery(self) -> None:
        self.run_import()
        original = imports.tree_hashes(self.target)
        receipt = (self.skill_root / imports.RECEIPT).read_bytes()
        (self.source / "SKILL.md").write_text("# New\n")
        real_rename = Path.rename

        def fail_restore(path, destination):
            if path.name == "previous":
                raise OSError("rollback blocked")
            return real_rename(path, destination)

        output = io.StringIO()
        with mock.patch.object(imports.os, "replace", side_effect=OSError("receipt blocked")), mock.patch.object(Path, "rename", new=fail_restore), contextlib.redirect_stderr(output):
            with self.assertRaises(imports.ImportError):
                self.run_import([{**self.entry, "revision": "b" * 40}])
        self.assertIn("reconciliation required", output.getvalue())
        recoveries = list(self.skill_root.glob(".ai-toolkit-import-*"))
        self.assertEqual(1, len(recoveries))
        self.assertEqual(original, imports.tree_hashes(recoveries[0] / "previous"))
        self.assertEqual(receipt, (self.skill_root / imports.RECEIPT).read_bytes())

    def test_new_install_receipt_failure_leaves_no_skill(self) -> None:
        with mock.patch.object(imports.os, "replace", side_effect=OSError("injected")):
            with self.assertRaises(imports.ImportError):
                self.run_import()
        self.assertFalse(self.target.exists())
        self.assertFalse((self.skill_root / imports.RECEIPT).exists())

    def test_receipt_inventory_validation_refuses_corrupt_ownership(self) -> None:
        self.run_import()
        receipt_path = self.skill_root / imports.RECEIPT
        original = json.loads(receipt_path.read_text())
        for inventory in ({"../escape": "a" * 64}, {"SKILL.md": "bad"}, {"A": "a" * 64, "a": "b" * 64}):
            with self.subTest(inventory=inventory):
                changed = json.loads(json.dumps(original))
                changed["skills"]["sample"]["files"] = inventory
                receipt_path.write_text(json.dumps(changed))
                with self.assertRaisesRegex(imports.ImportError, "receipt"):
                    self.run_import()
        self.assertTrue((self.target / "SKILL.md").is_file())

    def test_destination_and_receipt_symlinks_are_preserved(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        for kind in ("ancestor", "skill", "receipt"):
            with self.subTest(kind=kind):
                self.skill_root.mkdir(parents=True, exist_ok=True)
                path = self.home / ".codex" if kind == "ancestor" else self.target if kind == "skill" else self.skill_root / imports.RECEIPT
                if kind == "ancestor":
                    self.skill_root.rmdir()
                    path.rmdir()
                path.symlink_to(outside, target_is_directory=True)
                try:
                    with self.assertRaisesRegex(imports.ImportError, "symlink"):
                        self.run_import()
                    self.assertTrue(path.is_symlink())
                    self.assertEqual([], list(outside.iterdir()))
                finally:
                    path.unlink()

    def test_source_symlink_or_missing_skill_is_rejected_without_writes(self) -> None:
        (self.source / "scripts/escape").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(imports.ImportError):
            self.run_import()
        self.assertFalse(self.target.exists())
        (self.source / "scripts/escape").unlink()
        (self.source / "SKILL.md").unlink()
        with self.assertRaises(imports.ImportError):
            self.run_import()
        self.assertFalse(self.target.exists())

    def test_dry_run_has_no_fetch_or_writes_and_reports_compatible_destinations(self) -> None:
        fetch = mock.Mock()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            imports.sync_external_skills([self.entry], {"codex"}, home=self.home, dry_run=True, fetcher=fetch)
        fetch.assert_not_called()
        self.assertIn("Would sync", output.getvalue())
        self.assertFalse(self.skill_root.exists())

    def test_cursor_is_project_only_and_other_agent_targets_are_selected(self) -> None:
        project = self.root / "project"
        entry = {**self.entry, "tools": ["cursor", "claude", "copilot"]}
        imports.sync_external_skills([entry], {"cursor"}, home=self.home, fetcher=mock.Mock(side_effect=AssertionError("must skip")))
        self.assertFalse((self.home / ".cursor").exists())
        imports.sync_external_skills([entry], {"cursor", "claude", "copilot"}, [project], home=self.home, fetcher=lambda *_: self.source)
        self.assertTrue((project / ".cursor/skills/sample/SKILL.md").is_file())
        self.assertTrue((self.home / ".claude/skills/sample/SKILL.md").is_file())
        self.assertTrue((self.home / ".copilot/skills/sample/SKILL.md").is_file())
        self.assertFalse(self.target.exists())

    def test_fetch_failure_is_nonzero_and_does_not_expose_raw_error(self) -> None:
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            with self.assertRaises(imports.ImportError):
                imports.sync_external_skills([self.entry], {"codex"}, home=self.home, fetcher=mock.Mock(side_effect=OSError("secret-token")))
        self.assertNotIn("secret-token", error.getvalue())
        self.assertFalse(self.target.exists())

    def test_sync_skip_external_has_no_manifest_or_network_dependency(self) -> None:
        with mock.patch.object(sys, "argv", ["sync.py", "--tool", "codex", "--no-build", "--skip-external"]), mock.patch.object(sync.external_skills, "load_manifest") as load, mock.patch.object(sync.external_skills, "sync_external_skills") as external, mock.patch.object(sync, "sync_codex") as local:
            self.assertEqual(0, sync.main())
        load.assert_not_called()
        external.assert_not_called()
        local.assert_called_once()

    def test_sync_preflight_error_prevents_all_legacy_writes(self) -> None:
        with mock.patch.object(sys, "argv", ["sync.py", "--tool", "all"]), mock.patch.object(sync.external_skills, "load_manifest", return_value=[self.entry]), mock.patch.object(sync.external_skills, "preflight", side_effect=imports.ImportError("conflict")), mock.patch.object(sync, "run_build") as build, mock.patch.object(sync, "sync_codex") as local:
            self.assertEqual(1, sync.main())
        build.assert_not_called()
        local.assert_not_called()

    def test_real_git_fetch_is_pinned_and_isolates_user_configuration(self) -> None:
        repository = self.root / "upstream"
        repository.mkdir()
        real_run = subprocess.run
        real_run(["git", "init", str(repository)], check=True, capture_output=True)
        (repository / "SKILL.md").write_text("# First\n")
        real_run(["git", "-C", str(repository), "add", "SKILL.md"], check=True, capture_output=True)
        real_run(["git", "-C", str(repository), "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "First"], check=True, capture_output=True)
        revision = real_run(["git", "-C", str(repository), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
        (repository / "SKILL.md").write_text("# Second\n")
        real_run(["git", "-C", str(repository), "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-am", "Second"], check=True, capture_output=True)
        commands = []

        def local_git(command, **kwargs):
            commands.append((list(command), dict(kwargs["env"])))
            if "fetch" in command:
                command = list(command)
                index = command.index("fetch")
                command[index:index] = ["-c", "protocol.file.allow=always"]
                command[command.index(self.entry["repo"])] = str(repository)
            return real_run(command, **kwargs)

        staging = self.root / "fetch"
        staging.mkdir()
        with mock.patch.dict(os.environ, {"GIT_DIR": "/wrong", "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.hooksPath", "GIT_CONFIG_VALUE_0": "/wrong"}), mock.patch.object(imports.subprocess, "run", side_effect=local_git):
            source = imports.fetch_skill({**self.entry, "path": ".", "revision": revision}, staging)
        self.assertEqual("# First\n", (source / "SKILL.md").read_text())
        self.assertFalse((source / ".git").exists())
        for command, environment in commands:
            self.assertNotIn("GIT_DIR", environment)
            self.assertNotIn("GIT_CONFIG_COUNT", environment)
            self.assertEqual(os.devnull, environment["GIT_CONFIG_GLOBAL"])
            self.assertEqual("1", environment["GIT_CONFIG_NOSYSTEM"])
            self.assertTrue(any(arg.startswith("core.hooksPath=") for arg in command))


if __name__ == "__main__":
    unittest.main()
