"""Exercise the agent upgrade through the normal CLI with isolated tool homes."""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("retired_agent_sync", ROOT / "scripts" / "sync.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class RetiredAgentSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name).resolve()
        self.home = directory / "home"
        self.home.mkdir()
        self.repo = directory / "repository"
        self.repo.mkdir()
        self.dist = self.repo / "dist"
        for area in ("src", "docs", "scripts", "validation"):
            shutil.copytree(ROOT / area, self.repo / area, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.build()
        self.enterContext(mock.patch.object(sync, "ROOT", self.repo))
        self.enterContext(mock.patch.object(sync, "DIST", self.dist))
        self.enterContext(mock.patch.object(Path, "home", return_value=self.home))
        self.old = b"former toolkit profile\n"
        digest = hashlib.sha256(self.old).hexdigest()
        test_hashes = {tool: dict.fromkeys(names, (digest,)) for tool, names in sync.RETIRED_AGENT_DIGESTS.items()}
        self.enterContext(mock.patch.dict(sync.RETIRED_AGENT_DIGESTS, test_hashes))

    def build(self) -> None:
        subprocess.run([sys.executable, "scripts/build.py"], cwd=self.repo, capture_output=True, check=True)

    def install(self, *, succeeds: bool = True) -> str:
        with (
            mock.patch.object(sys, "argv", ["sync.py", "--tool", "all", "--no-build", "--skip-external"]),
            redirect_stdout(io.StringIO()) as output,
            redirect_stderr(io.StringIO()) as errors,
        ):
            result = sync.main()
        self.assertEqual(0 if succeeds else 1, result, errors.getvalue())
        return output.getvalue() + errors.getvalue()

    def agent(self, tool: str, role: str) -> Path:
        return self.home / f".{tool}" / "agents" / f"{role}.{sync.AGENT_EXTENSIONS[tool]}"

    def seed_old(self) -> None:
        for tool in sync.AGENT_EXTENSIONS:
            target = self.agent(tool, "product-designer")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(self.old.replace(b"\n", b"\r\n"))
            self.agent(tool, "code-reviewer").write_bytes(b"my customized retired profile")
            self.agent(tool, "personal").write_bytes(b"independent content")

    def snapshot(self) -> dict[str, bytes | None]:
        return {p.relative_to(self.home).as_posix(): p.read_bytes() if p.is_file() else None for p in self.home.rglob("*")}

    def test_empty_homes_repeat_and_later_managed_upgrade(self) -> None:
        self.install()
        previous = self.agent("codex", sync.build.SENIOR_AGENT).read_bytes()
        for tool in sync.AGENT_EXTENSIONS:
            for role in sync.REPLACEMENT_AGENTS:
                self.assertTrue(self.agent(tool, role).is_file())
        self.install()
        self.assertEqual(previous, self.agent("codex", sync.build.SENIOR_AGENT).read_bytes())
        self.seed_old()
        canonical = self.repo / "src" / "agents" / f"{sync.build.SENIOR_AGENT}.md"
        with canonical.open("a", encoding="utf-8") as writer:
            writer.write("\nInstructions from a later toolkit release.\n")
        self.build()
        self.assertIn("Removed retired toolkit agent", self.install())
        for tool in sync.AGENT_EXTENSIONS:
            self.assertIn(b"later toolkit release", self.agent(tool, sync.build.SENIOR_AGENT).read_bytes())
            self.assertFalse(self.agent(tool, "product-designer").exists())
            self.assertEqual(b"my customized retired profile", self.agent(tool, "code-reviewer").read_bytes())
            self.assertEqual(b"independent content", self.agent(tool, "personal").read_bytes())
        self.install()

    def test_custom_first_install_and_edited_installed_role_preserve_both_homes(self) -> None:
        self.seed_old()
        profile = self.agent("claude", sync.build.SENIOR_AGENT)
        profile.write_text("# My unrelated profile", encoding="utf-8")
        before = self.snapshot()
        error = self.install(succeeds=False)
        self.assertIn(str(profile), error)
        self.assertIn("Move or back up", error)
        self.assertEqual(before, self.snapshot())
        profile.unlink()
        self.install()
        with profile.open("ab") as out:
            out.write(b"Local instruction.")
        before = self.snapshot()
        self.assertIn(str(profile), self.install(succeeds=False))
        self.assertEqual(before, self.snapshot())

    def test_linked_replacement_profile_blocks_both_homes_without_writing_through(self) -> None:
        self.seed_old()
        external = self.repo / "personal.md"
        external.write_bytes(b"owner's original")
        profile = self.agent("claude", sync.build.SENIOR_AGENT)
        try:
            profile.symlink_to(external)
        except OSError as exc:
            self.skipTest(f"Symbolic links unavailable: {exc}")
        before = self.snapshot()
        self.assertIn("symlink", self.install(succeeds=False))
        self.assertEqual(before, self.snapshot())
        self.assertTrue(profile.is_symlink())
        self.assertEqual(b"owner's original", external.read_bytes())
        profile.unlink()
        retired = self.agent("codex", "product-designer")
        retired.unlink()
        retired.symlink_to(external)
        self.install()
        self.assertTrue(retired.is_symlink())
        self.assertEqual(b"owner's original", external.read_bytes())

    def test_arrival_or_edit_after_ownership_check_survives(self) -> None:
        target = self.agent("codex", sync.build.SENIOR_AGENT)
        target.parent.mkdir(parents=True)
        source = self.dist / "codex" / "agents" / target.name
        check = sync._check_senior_destination
        for already_installed in (False, True):
            with self.subTest(already_installed=already_installed):
                if already_installed:
                    shutil.copy2(source, target)

                def owner_writes_after_check(tool: str, home: Path):
                    observed = check(tool, home)
                    self.assertEqual(already_installed, observed is not None)
                    target.write_bytes(b"owner's concurrent edit")
                    return observed

                with mock.patch.object(sync, "_check_senior_destination", side_effect=owner_writes_after_check):
                    with self.assertRaisesRegex(ValueError, "Preserved"):
                        sync._install_senior("codex", self.home / ".codex", source)
                self.assertEqual(b"owner's concurrent edit", target.read_bytes())

    def test_incomplete_damaged_or_mismapped_build_never_modifies_either_home(self) -> None:
        self.seed_old()
        before = self.snapshot()
        for damage in ("missing-root", "no-manifest", "missing-claude-role", "bad-claude-role",
                       "missing-mapping", "stale-canonical", "retired-output"):
            with self.subTest(damage=damage):
                self.build()
                manifest_path = self.dist / "manifest.json"
                staff = self.dist / "claude/agents/staff-engineer.md"
                if damage == "missing-root":
                    shutil.rmtree(self.dist)
                elif damage == "no-manifest":
                    manifest_path.unlink()
                elif damage == "missing-claude-role":
                    staff.unlink()
                elif damage == "bad-claude-role":
                    staff.write_text("corrupt")
                elif damage == "missing-mapping":
                    manifest = json.loads(manifest_path.read_text())
                    entry = next(item for item in manifest["entries"] if item["source"] == "src/agents/staff-engineer.md")
                    entry["projections"] = [p for p in entry["projections"] if "dist/claude" not in p["path"]]
                    manifest_path.write_text(json.dumps(manifest))
                elif damage == "stale-canonical":
                    with (self.repo / "src/agents/staff-engineer.md").open("a") as source:
                        source.write("\nUpdated source")
                else:
                    (self.dist / "claude/agents/code-reviewer.md").write_bytes(self.old)
                self.assertIn("Rebuild dist", self.install(succeeds=False))
                self.assertEqual(before, self.snapshot())


class WritingRuleUpgradeTests(unittest.TestCase):
    def install(self, script: Path, user_home: Path) -> None:
        with (
            mock.patch.object(Path, "home", return_value=user_home),
            mock.patch.object(sys, "argv", [str(script), "--tool", "all", "--no-build", "--skip-external"]),
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()) as errors,
            self.assertRaises(SystemExit) as result,
        ):
            runpy.run_path(str(script), run_name="__main__")
        self.assertEqual(result.exception.code, 0, errors.getvalue())

    def test_upgrade_real_plain_english_install(self) -> None:
        revision = "6dcfbef7d1294fa4c469cc784d747fbe4c83a78c"
        available = subprocess.run(["git", "cat-file", "-e", revision], cwd=ROOT, capture_output=True)
        if available.returncode:
            self.skipTest("Plain-English baseline commit is absent from this checkout")
        archive = subprocess.check_output(["git", "archive", "--format=zip", revision], cwd=ROOT)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            old = root / "baseline"
            with zipfile.ZipFile(io.BytesIO(archive)) as source:
                source.extractall(old)
            subprocess.run([sys.executable, "scripts/build.py"], cwd=old, capture_output=True, check=True)

            script = ROOT / "scripts/sync.py"
            fresh = root / "fresh"
            upgrade = root / "upgrade"
            customized = root / "customized"
            self.install(old / "scripts/sync.py", upgrade)
            shutil.copytree(upgrade, customized)
            tool_configs = {"codex": "AGENTS.md", "claude": "CLAUDE.md"}
            expected_custom = {}
            for tool, extension in sync.AGENT_EXTENSIONS.items():
                relative = Path(f".{tool}/agents/code-reviewer.{extension}")
                local_profile = customized / relative
                expected_custom[relative] = local_profile.read_bytes() + b"\nMy review rules.\n"
                local_profile.write_bytes(expected_custom[relative])

            self.install(script, fresh)
            self.install(script, upgrade)
            self.install(script, customized)
            first = {path.relative_to(upgrade): path.read_bytes() for path in upgrade.rglob("*") if path.is_file()}
            self.install(script, upgrade)
            second = {path.relative_to(upgrade): path.read_bytes() for path in upgrade.rglob("*") if path.is_file()}
            self.assertEqual(first, second)
            for tool, instruction in tool_configs.items():
                agent_files = Path(f".{tool}/agents")
                self.assertEqual(
                    sorted(path.name for path in (fresh / agent_files).iterdir()),
                    sorted(path.name for path in (upgrade / agent_files).iterdir()),
                )
                for name in sync.RETIRED_AGENT_DIGESTS[tool]:
                    self.assertFalse((upgrade / agent_files / name).exists())
                for user_home in (fresh, upgrade, customized):
                    text = (user_home / f".{tool}" / instruction).read_bytes()
                    self.assertEqual(text.count(b"<!-- AI-TOOLKIT-REPLY-STYLE:START -->"), 1)
            for relative, expected in expected_custom.items():
                self.assertEqual((customized / relative).read_bytes(), expected)
