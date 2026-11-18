"""Exercise documentation installation without touching real user homes."""
from __future__ import annotations

import importlib.util
import io
import re
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("project_docs_sync", ROOT / "scripts" / "sync.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


def assert_resource_links_resolve(test: unittest.TestCase, path: Path) -> None:
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        if "://" in target or target.startswith("#"):
            continue
        relative = target.split("#", 1)[0]
        test.assertTrue((path.parent / relative).is_file(), f"Broken resource link in {path}: {target}")


class ProjectDocsSyncTests(unittest.TestCase):
    def test_user_sync_installs_resources_and_preserves_personal_instructions(self) -> None:
        tools = (
            (sync.sync_codex, ".codex", "AGENTS.md"),
            (sync.sync_claude, ".claude", "CLAUDE.md"),
        )
        for install, folder, instruction_name in tools:
            with self.subTest(tool=folder), tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                tool_home = home / folder
                tool_home.mkdir()
                instructions = tool_home / instruction_name
                prefix = b"# Personal rules\r\n\r\n@RTK.md\r\n"
                suffix = b"\r\n# Local choices\r\n"
                instructions.write_bytes(prefix)
                with mock.patch.object(Path, "home", return_value=home), redirect_stdout(io.StringIO()):
                    install()
                    first = instructions.read_bytes()
                    instructions.write_bytes(first + suffix)
                    install()
                self.assertTrue(first.startswith(prefix))
                self.assertEqual(first + suffix, instructions.read_bytes())
                self.assertEqual(1, first.count(b"<!-- AI-TOOLKIT-PROJECT-DOCS:START -->"))

                skills = tool_home / "skills"
                for name in ("project-docs", "project-docs-review"):
                    entry = skills / name / "SKILL.md"
                    self.assertTrue(entry.is_file())
                    assert_resource_links_resolve(self, entry)
                for name in ("PRD.md", "DESIGN_SYSTEM.md", "ARCHITECTURE.md", "AGENTS.md"):
                    self.assertTrue((skills / "project-docs" / "assets" / name).is_file())

                agent_name = "staff-engineer.toml" if folder == ".codex" else "staff-engineer.md"
                staff_engineer = tool_home / "agents" / agent_name
                guide = tool_home / "tool-instructions" / "shared" / "twelve-factor-for-agentic-development.md"
                self.assertIn(f"](../{guide.relative_to(tool_home).as_posix()})", staff_engineer.read_text(encoding="utf-8"))
                self.assertEqual((ROOT / "docs" / guide.name).read_bytes(), guide.read_bytes())

    def test_malformed_docs_markers_preserve_existing_instructions(self) -> None:
        start = "<!-- AI-TOOLKIT-PROJECT-DOCS:START -->"
        end = "<!-- AI-TOOLKIT-PROJECT-DOCS:END -->"
        for original in (start, end, end + start, start + end + start + end):
            with self.subTest(original=original), tempfile.TemporaryDirectory() as directory:
                instructions = Path(directory) / "AGENTS.md"
                instructions.write_text(original, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Malformed Project documentation markers"):
                    sync.sync_project_docs_guidance(instructions)
                self.assertEqual(original, instructions.read_text(encoding="utf-8"))

    def test_project_sync_shares_agents_and_preserves_existing_tool_file(self) -> None:
        for tools in ({"claude"}, {"codex", "claude"}):
            with self.subTest(tools=tools), tempfile.TemporaryDirectory() as directory:
                project = Path(directory)
                with redirect_stdout(io.StringIO()):
                    sync.sync_tool_instructions(project, tools, False)
                instructions = project / "AGENTS.md"
                first = instructions.read_bytes()
                self.assertFalse((project / "CLAUDE.md").exists())
                self.assertEqual(1, first.count(b"<!-- AI-TOOLKIT-PROJECT-DOCS:START -->"))
                self.assertNotIn(b"{{PROJECT_DOCUMENTATION_GUIDANCE}}", first)

                custom_tool = project / "CLAUDE.md"
                custom_tool.write_bytes(b"# Existing custom instructions\r\n")
                suffix = b"\r\n# Repository choices\r\n"
                instructions.write_bytes(first + suffix)
                with redirect_stdout(io.StringIO()):
                    sync.sync_tool_instructions(project, tools, False)
                self.assertEqual(first + suffix, instructions.read_bytes())
                self.assertEqual(b"# Existing custom instructions\r\n", custom_tool.read_bytes())

    def test_project_sync_preserves_unmanaged_foundations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            originals = {
                "AGENTS.md": b"# Custom project rules\r\n",
                "docs/product.md": b"# Existing product brief\r\n",
                "docs/design/tokens.md": b"# Existing token guide\r\n",
            }
            for relative, content in originals.items():
                path = project / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
            with redirect_stdout(io.StringIO()):
                sync.sync_tool_instructions(project, {"claude"}, False)
            for relative, content in originals.items():
                self.assertEqual(content, (project / relative).read_bytes())
            self.assertEqual(set(originals), {path.relative_to(project).as_posix() for path in project.rglob("*") if path.is_file()})

if __name__ == "__main__":
    unittest.main()
