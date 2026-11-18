"""Protect existing user instructions when installing toolkit guidance."""
from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from validation.delivery_contracts import CANONICAL_REFERENCES, WORKFLOW_ROUTES, _resolved_local_links

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("markdown_sync", ROOT / "scripts" / "sync.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class MarkdownSyncTests(unittest.TestCase):
    def test_append_refresh_and_idempotence_preserve_user_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            dest = home / "AGENTS.md"
            original = b"# Personal rules\r\n\r\n@RTK.md\r\n"
            dest.write_bytes(original)
            with mock.patch.object(Path, "home", return_value=home):
                sync.sync_markdown_guidance(dest)
                first = dest.read_bytes()
                self.assertTrue(first.startswith(original))
                self.assertEqual(1, first.count(b"<!-- AI-TOOLKIT-MARKDOWN:START -->"))
                config = home / ".config" / "ai-toolkit" / "markdownlint-cli2.jsonc"
                self.assertEqual(
                    (sync.DIST / "tool-instructions/shared/markdownlint-cli2.jsonc").read_bytes(),
                    config.read_bytes(),
                )
                dest.write_bytes(first + b"\r\n# More personal rules\r\n")
                sync.sync_markdown_guidance(dest)
                refreshed = dest.read_bytes()
                self.assertEqual(first + b"\r\n# More personal rules\r\n", refreshed)
                sync.sync_markdown_guidance(dest)
                self.assertEqual(refreshed, dest.read_bytes())

    def test_fresh_home_gets_guidance_and_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            dest = home / ".claude" / "CLAUDE.md"
            with mock.patch.object(Path, "home", return_value=home):
                sync.sync_markdown_guidance(dest)
            self.assertIn("markdownlint-cli2", dest.read_text())
            self.assertTrue((home / ".config/ai-toolkit/markdownlint-cli2.jsonc").is_file())

    def test_malformed_or_duplicate_markers_are_preserved(self) -> None:
        start = "<!-- AI-TOOLKIT-MARKDOWN:START -->"
        end = "<!-- AI-TOOLKIT-MARKDOWN:END -->"
        for original in (start, end, end + start, start + end + start + end):
            with self.subTest(original=original), tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                dest = home / "AGENTS.md"
                dest.write_text(original)
                with mock.patch.object(Path, "home", return_value=home):
                    with self.assertRaisesRegex(ValueError, "Malformed Markdown lint markers"):
                        sync.sync_markdown_guidance(dest)
                self.assertEqual(original, dest.read_text())
                self.assertFalse((home / ".config").exists())


class DeliveryRoutingSyncTests(unittest.TestCase):
    def assert_delivery_links_resolve(self, installed_root: Path) -> None:
        for reference in {*CANONICAL_REFERENCES, *WORKFLOW_ROUTES}:
            installed = installed_root / reference.relative_to("src")
            self.assertTrue(installed.is_file(), installed)
            if installed.suffix == ".md":
                for target in _resolved_local_links(installed):
                    self.assertTrue(target.is_file() and installed_root.resolve() in target.parents, target)

    def test_sync_installs_portable_delivery_links_and_upgrades_old_worktree_route(self) -> None:
        installations = (
            ("codex", "AGENTS.md", sync.sync_codex),
            ("claude", "CLAUDE.md", sync.sync_claude),
        )
        for tool, instruction_name, install in installations:
            with self.subTest(tool=tool), tempfile.TemporaryDirectory() as directory:
                home = Path(directory) / "Tool Home"
                tool_home = home / f".{tool}"
                obsolete_policy = tool_home / "skills/goal-to-delivery/references/worktree-policy.md"
                obsolete_policy.parent.mkdir(parents=True)
                obsolete_policy.write_text("Old worktree policy\n", encoding="utf-8")
                instructions = tool_home / instruction_name
                instructions.write_text(
                    "# Personal rules\n\n"
                    "<!-- AI-TOOLKIT-WORKTREES:START -->\n"
                    "Read skills/goal-to-delivery/references/worktree-policy.md.\n"
                    "<!-- AI-TOOLKIT-WORKTREES:END -->\n"
                    "\n# More personal rules\n",
                    encoding="utf-8",
                )
                with mock.patch.object(Path, "home", return_value=home), redirect_stdout(io.StringIO()):
                    install()

                content = instructions.read_text(encoding="utf-8")
                policy = tool_home / "tool-instructions/shared/worktrees.md"
                self.assertTrue(content.startswith("# Personal rules\n\n"))
                self.assertIn("# More personal rules\n", content)
                self.assertIn(f"(<{policy.as_posix()}>)", content)
                self.assertIn("when an older project instruction points to the former Goal to Delivery location", content)
                self.assertNotIn("worktree-policy.md", content)
                self.assertFalse(obsolete_policy.exists())
                self.assertIn("git worktree add -b <branch> <exact-path> <resolved-base-commit>", policy.read_text(encoding="utf-8"))
                self.assert_delivery_links_resolve(tool_home)

    def test_project_sync_upgrades_to_a_portable_delivery_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            for tool in ("codex", "claude"):
                with self.subTest(tool=tool), redirect_stdout(io.StringIO()):
                    project = Path(directory) / tool
                    project.mkdir()
                    target = project / "AGENTS.md"
                    target.write_text(
                        "# Local instructions\n\n"
                        f"{sync.MARKER_START}\n"
                        "Read `goal-to-delivery/references/worktree-policy.md`.\n"
                        f"{sync.MARKER_END}\n",
                        encoding="utf-8",
                    )
                    sync.sync_tool_instructions(project, {tool}, False)
                    content = target.read_text(encoding="utf-8")
                    self.assertTrue(content.startswith("# Local instructions\n\n"))
                    self.assertIn("`tool-instructions/shared/delivery-workflow.md` in the active tool's home", content)
                    self.assertNotIn("src/tool-instructions/shared/delivery-workflow.md", content)
                    self.assertNotIn("goal-to-delivery/references/worktree-policy.md", content)


class CodexRoutingSyncTests(unittest.TestCase):
    def test_sync_installs_dotnet_route_and_reference_with_personal_rules_intact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            codex = home / ".codex"
            codex.mkdir()
            instructions = codex / "AGENTS.md"
            original = b"# Personal rules\r\n\r\n@RTK.md\r\n"
            instructions.write_bytes(original)
            with mock.patch.object(Path, "home", return_value=home), redirect_stdout(io.StringIO()):
                sync.sync_codex()
                first = instructions.read_bytes()
                suffix = b"\r\n# More personal rules\r\n"
                instructions.write_bytes(first + suffix)
                sync.sync_codex()

            self.assertTrue(first.startswith(original))
            self.assertEqual(first + suffix, instructions.read_bytes())
            self.assertEqual(1, first.count(b"<!-- AI-TOOLKIT-DOTNET:START -->"))
            self.assertIn(b"$dotnet-implementation", first)
            self.assertTrue((codex / "agents/dotnet.toml").is_file())
            skill = codex / "skills/dotnet-implementation"
            self.assertTrue((skill / "SKILL.md").is_file())
            self.assertTrue((skill / "references/modular-monolith.md").is_file())


if __name__ == "__main__":
    unittest.main()
