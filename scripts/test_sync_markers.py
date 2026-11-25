"""Dependency-free regression tests for marker-managed tool instructions."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bootstrap_existing  # noqa: E402
import sync  # noqa: E402


BODY = "<!-- AI-TOOLKIT-LUCHDOM:START -->\r\n# Template\r\n<!-- AI-TOOLKIT-LUCHDOM:END -->\r\n"
LEGACY_BODY = "<!-- AI-CONFIG-LUCHDOM:START -->\r\n# Legacy\r\n<!-- AI-CONFIG-LUCHDOM:END -->\r\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as file:
        file.write(content)


def read(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as file:
        return file.read()


def source(root: Path, content: str = BODY) -> Path:
    path = root / "template.md"
    write(path, content)
    return path


def test_fresh_write_and_splice() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        src, dest = source(root), root / "target.md"
        assert sync.write_or_splice_template(src, dest, False) == "new"
        external = "\r\n@RTK.md\r\n<!-- CODEGRAPH_START -->\r\n<!-- CODEGRAPH_END -->\r\n"
        write(dest, read(dest).rstrip("\r\n") + external)
        write(src, BODY.replace("# Template", "# Updated"))
        assert sync.write_or_splice_template(src, dest, False) == "spliced"
        result = read(dest)
        assert "# Updated" in result and result.endswith(external)


def test_legacy_and_force() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        src, dest = source(root), root / "target.md"
        write(dest, "# Hand-written\n")
        assert sync.write_or_splice_template(src, dest, False) == "skipped"
        assert sync.write_or_splice_template(src, dest, True) == "overwrote"

        write(dest, LEGACY_BODY.rstrip("\r\n") + "\r\n@RTK.md\r\n")
        assert sync.write_or_splice_template(src, dest, False) == "spliced"
        result = read(dest)
        assert sync.MARKER_START in result
        assert "AI-CONFIG-LUCHDOM" not in result
        assert result.endswith("\r\n@RTK.md\r\n")


def test_malformed_and_newline_preservation() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        src, dest = source(root), root / "target.md"
        write(dest, "<!-- AI-TOOLKIT-LUCHDOM:START -->\n")
        try:
            sync.write_or_splice_template(src, dest, False)
        except ValueError as exc:
            assert str(dest) in str(exc)
        else:
            raise AssertionError("Unmatched project marker was accepted")
        write(dest, BODY.rstrip("\r\n") + "\n@RTK.md\n")
        assert sync.write_or_splice_template(src, dest, False) == "spliced"
        assert read(dest).endswith("\n@RTK.md\n")


def test_separated_blocks_preserve_all_unmanaged_bytes() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        src, dest = source(root), root / "target.md"
        prefix = "# Before\r\n"
        middle = "\r\n# Keep this project rule\r\n"
        suffix = "\n# After\n"
        existing = prefix + LEGACY_BODY.rstrip("\r\n") + middle + BODY.rstrip("\r\n") + suffix
        write(dest, existing)

        for _ in range(2):
            assert sync.write_or_splice_template(src, dest, False) == "spliced"
            assert read(dest) == prefix + BODY.rstrip("\r\n") + middle + suffix


def test_marker_examples_are_unmanaged() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        src, dest = source(root), root / "target.md"
        examples = (
            f"Sync updates the block between `{sync.MARKER_START}` and `{sync.MARKER_END}`.\r\n"
            f"`{sync.MARKER_START}`\r\n# Personal rule\r\n`{sync.MARKER_END}`\r\n\r\n"
            f"````markdown\r\n```\r\n{LEGACY_BODY}````\r\n\r\n"
            f"~~~html\n{sync.MARKER_START}\n{sync.MARKER_END}\n~~~\n"
            f"- ```markdown\r\n  {sync.MARKER_START}\r\n  # Example\r\n  {sync.MARKER_END}\r\n  ```\r\n\r\n"
            f"10. ~~~html\n    {sync.MARKER_START}\n    {sync.MARKER_END}\n    ~~~\n\n"
            f"  ```\n    ```\n{sync.MARKER_START}\n{sync.MARKER_END}\n  ```\n\n"
        )
        write(dest, examples)
        assert sync.write_or_splice_template(src, dest, False) == "skipped"
        assert read(dest) == examples

        write(dest, examples + LEGACY_BODY + "# Personal footer\r\n")
        assert sync.write_or_splice_template(src, dest, False) == "spliced"
        assert read(dest) == examples + BODY.rstrip("\r\n") + "\r\n# Personal footer\r\n"

        # This list ends without an explicit fence closer when it reaches the real block.
        open_list_example = f"- ```\n  {sync.MARKER_START}\n  {sync.MARKER_END}\n\n"
        write(dest, open_list_example + LEGACY_BODY)
        assert sync.write_or_splice_template(src, dest, False) == "spliced"
        assert read(dest) == open_list_example + BODY

        # List continuation paragraphs can also contain an implicitly closed fence.
        examples = (
            ("- Maintainer example", "  "),
            ("- Maintainer example\nContinue the paragraph.", "  "),
            ("- Maintainer example\n2026 notes continue the paragraph.", "  "),
            ("- Maintainer example\n(Continue the paragraph.)", "  "),
            ("- Maintainer example\n<https://example.com>", "  "),
            ("10. Maintainer example", "    "),
            ("- Example\n  - Nested item", "    "),
        )
        for heading, padding in examples:
            prefix = (
                f"{heading}\n\n{padding}```markdown\n"
                f"{padding}{sync.MARKER_START}\n{padding}# Preserve this example\n"
                f"{padding}{sync.MARKER_END}\n\n"
            )
            write(dest, prefix + LEGACY_BODY)
            for _ in range(2):
                assert sync.write_or_splice_template(src, dest, False) == "spliced"
                assert read(dest) == prefix + BODY

        # These prefixes leave the following two-space fence outside a list.
        for prefix in (
            "- - -\n",
            "A paragraph\n2. More text\n",
            "A paragraph\n01. More text\n-\n",
            "-\n\n",
            "- Maintainer example\n2. New ordered list\n\n",
            "- Maintainer example\n<div>\n</div>\n\n",
        ):
            example = f"{prefix}  ```markdown\n{LEGACY_BODY}  ```\n"
            write(dest, example)
            assert sync.write_or_splice_template(src, dest, False) == "skipped"
            assert read(dest) == example


def test_docs_override_prefers_toolkit_and_supports_legacy() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        src = source(root, "{{LUCHDOM_AI_TOOLKIT_DOCS}}|{{LUCHDOM_AI_CONFIG_DOCS}}")
        toolkit_docs = root / "toolkit-docs"
        legacy_docs = root / "legacy-docs"

        with mock.patch.dict(
            "os.environ",
            {
                "LUCHDOM_AI_TOOLKIT_DOCS": str(toolkit_docs),
                "LUCHDOM_AI_CONFIG_DOCS": str(legacy_docs),
            },
            clear=True,
        ):
            rendered = sync.render_template_text(src)
            expected = toolkit_docs.resolve().as_posix()
            assert rendered == f"{expected}|{expected}"

        with mock.patch.dict("os.environ", {"LUCHDOM_AI_CONFIG_DOCS": str(legacy_docs)}, clear=True):
            rendered = sync.render_template_text(src)
            expected = legacy_docs.resolve().as_posix()
            assert rendered == f"{expected}|{expected}"


def test_project_help_names_tool_instruction_destination() -> None:
    result = subprocess.run(
        [sys.executable, str(Path(sync.__file__)), "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Destination project root to receive tool instructions." in result.stdout


def test_sync_tool_instructions_reads_renamed_dist_root() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        dist = root / "dist"
        instruction = dist / "tool-instructions" / "codex" / "AGENTS.md"
        write(instruction, BODY)
        project = root / "project"
        with mock.patch.object(sync, "DIST", dist):
            sync.sync_tool_instructions(project, {"codex"}, False)
        assert read(project / "AGENTS.md") == BODY


def test_bootstrap_writes_tool_instruction_source_tree() -> None:
    with tempfile.TemporaryDirectory() as directory:
        source_root = Path(directory) / "src" / "tool-instructions"
        with mock.patch.object(bootstrap_existing, "SRC_TOOL_INSTRUCTIONS", source_root):
            bootstrap_existing.write_tool_instructions()
        instruction = source_root / "shared" / "project-agents.md"
        assert "{{PROJECT_DOCUMENTATION_GUIDANCE}}" in read(instruction)


def test_bootstrap_restores_twelve_factor_guide_link() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        codex_home = root / ".codex"
        source_agents = root / "src" / "agents"
        write(
            codex_home / "agents" / "staff-engineer.toml",
            'model = "test-model"\n'
            'model_reasoning_effort = "high"\n'
            'sandbox_mode = "workspace-write"\n'
            'developer_instructions = "Read [the guide](../tool-instructions/shared/twelve-factor-for-agentic-development.md)."\n',
        )
        with mock.patch.object(bootstrap_existing, "CODEX_HOME", codex_home):
            with mock.patch.object(bootstrap_existing, "SRC_AGENTS", source_agents):
                bootstrap_existing.write_agent_sources()
        assert "[the guide](../../docs/twelve-factor-for-agentic-development.md)" in read(
            source_agents / "staff-engineer.md"
        )


def main() -> int:
    tests = (
        test_fresh_write_and_splice,
        test_legacy_and_force,
        test_malformed_and_newline_preservation,
        test_separated_blocks_preserve_all_unmanaged_bytes,
        test_marker_examples_are_unmanaged,
        test_docs_override_prefers_toolkit_and_supports_legacy,
        test_project_help_names_tool_instruction_destination,
        test_sync_tool_instructions_reads_renamed_dist_root,
        test_bootstrap_writes_tool_instruction_source_tree,
        test_bootstrap_restores_twelve_factor_guide_link,
    )
    for test in tests:
        test()
        print(f"{test.__name__}: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
