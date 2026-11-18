from __future__ import annotations

import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Other toolkit skills also provide a package named scripts; load our sibling exactly.
_external_spec = importlib.util.spec_from_file_location("ai_toolkit_external_skills", Path(__file__).with_name("external_skills.py"))
external_skills = importlib.util.module_from_spec(_external_spec)
_external_spec.loader.exec_module(external_skills)


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MARKER_START = "<!-- AI-TOOLKIT-LUCHDOM:START -->"
MARKER_END = "<!-- AI-TOOLKIT-LUCHDOM:END -->"
LEGACY_MARKER_PAIRS = (("<!-- AI-CONFIG-LUCHDOM:START -->", "<!-- AI-CONFIG-LUCHDOM:END -->"),)


def run_build() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py")], check=True)


def sync_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Copied {src} -> {dest}")


def resolve_docs_root() -> str:
    override = os.environ.get("LUCHDOM_AI_TOOLKIT_DOCS") or os.environ.get("LUCHDOM_AI_CONFIG_DOCS")
    if override:
        return Path(override).expanduser().resolve().as_posix()
    return (ROOT / "docs").resolve().as_posix()


def render_template_text(src: Path) -> str:
    docs_root = resolve_docs_root()
    with open(src, "r", encoding="utf-8", newline="") as file:
        return (
            file.read()
            .replace("{{LUCHDOM_AI_TOOLKIT_DOCS}}", docs_root)
            .replace("{{LUCHDOM_AI_CONFIG_DOCS}}", docs_root)
            .replace("{{LUCHDOM_AI_TOOLKIT_ROOT}}", ROOT.as_posix())
        )


def consume_newline(text: str, position: int) -> int:
    if text[position:position + 2] == "\r\n":
        return position + 2
    if text[position:position + 1] == "\n":
        return position + 1
    return position


def write_or_splice_template(src: Path, dest: Path, force: bool) -> str:
    """Render a new managed file or refresh only its marker-owned content."""
    rendered = render_template_text(src)
    dest.parent.mkdir(parents=True, exist_ok=True)

    if not dest.exists():
        with open(dest, "w", encoding="utf-8", newline="") as file:
            file.write(rendered)
        print(f"Rendered {dest} (new)")
        return "new"

    if force:
        with open(dest, "w", encoding="utf-8", newline="") as file:
            file.write(rendered)
        print(f"Overwrote {dest} (--force; now marker-managed)")
        return "overwrote"

    with open(dest, "r", encoding="utf-8", newline="") as file:
        existing = file.read()

    marker_spans: list[tuple[int, int, int, int]] = []
    for start_marker, end_marker in ((MARKER_START, MARKER_END), *LEGACY_MARKER_PAIRS):
        start_positions = [match.start() for match in re.finditer(re.escape(start_marker), existing)]
        end_positions = [match.start() for match in re.finditer(re.escape(end_marker), existing)]
        if not start_positions and not end_positions:
            continue
        if not start_positions or not end_positions:
            print(f"Warning: malformed markers in {dest} (start/end mismatch), skipped")
            return "warning"

        first_start = min(start_positions)
        last_end = max(end_positions)
        if first_start >= last_end:
            print(f"Warning: malformed markers in {dest} (markers out of order), skipped")
            return "warning"
        marker_spans.append((first_start, last_end + len(end_marker), len(start_positions), len(end_positions)))

    if not marker_spans:
        print(f"Skipped existing {dest} (no markers; re-run with --force to adopt)")
        return "skipped"

    first_start = min(span[0] for span in marker_spans)
    last_end = max(span[1] for span in marker_spans)
    if len(marker_spans) > 1 or any(starts > 1 or ends > 1 for _, _, starts, ends in marker_spans):
        print(f"Warning: multiple marker pairs found in {dest}, using outermost")

    prefix = existing[:first_start]
    suffix = existing[consume_newline(existing, last_end):]
    with open(dest, "w", encoding="utf-8", newline="") as file:
        file.write(prefix + rendered + suffix)
    print(f"Spliced {dest} (preserved external content)")
    return "spliced"


def sync_skill_dirs(src_root: Path, dest_root: Path) -> None:
    dest_root.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(src_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        target = dest_root / skill_dir.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(skill_dir, target)
        print(f"Synced skill {skill_dir.name} -> {target}")


def sync_user_instruction_block(dest: Path, block: str, marker: str, label: str) -> None:
    """Update one toolkit-owned block without replacing personal instructions."""
    start = f"<!-- AI-TOOLKIT-{marker}:START -->"
    end = f"<!-- AI-TOOLKIT-{marker}:END -->"
    existing = ""
    if dest.exists():
        with dest.open(encoding="utf-8", newline="") as file:
            existing = file.read()
    if start in existing or end in existing:
        if existing.count(start) != 1 or existing.count(end) != 1 or existing.index(start) >= existing.index(end):
            raise ValueError(f"Malformed {label} markers in {dest}; preserved existing content.")
        end_position = consume_newline(existing, existing.index(end) + len(end))
        updated = existing[:existing.index(start)] + block + existing[end_position:]
    else:
        separator = "" if not existing or existing.endswith("\n\n") else "\n" if existing.endswith("\n") else "\n\n"
        updated = existing + separator + block
    if updated != existing:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("w", encoding="utf-8", newline="") as file:
            file.write(updated)
        print(f"Updated {label} guidance in {dest}")


def sync_markdown_guidance(dest: Path) -> None:
    shared = DIST / "tool-instructions" / "shared"
    guidance = (shared / "markdown-lint.md").read_text(encoding="utf-8")
    sync_user_instruction_block(dest, guidance, "MARKDOWN", "Markdown lint")
    sync_file(shared / "markdownlint-cli2.jsonc", Path.home() / ".config" / "ai-toolkit" / "markdownlint-cli2.jsonc")


def sync_project_docs_guidance(dest: Path) -> None:
    source = DIST / "tool-instructions" / "shared" / "project-docs.md"
    sync_user_instruction_block(dest, source.read_text(encoding="utf-8"), "PROJECT-DOCS", "Project documentation")


def sync_delivery_guidance(tool: str, tool_home: Path, instructions: Path) -> None:
    shared = Path("tool-instructions/shared")
    for source in sorted((DIST / tool / shared).glob("*.md")):
        sync_file(source, tool_home / shared / source.name)
    worktree_policy = (tool_home / shared / "worktrees.md").as_posix()
    block = (
        "<!-- AI-TOOLKIT-WORKTREES:START -->\n"
        "## Git worktrees\n\n"
        "Before creating, resuming, or removing a linked Git worktree, "
        f"follow the [shared worktree policy](<{worktree_policy}>).\n"
        "<!-- AI-TOOLKIT-WORKTREES:END -->\n"
    )
    sync_user_instruction_block(instructions, block, "WORKTREES", "Git worktree")


def sync_codex() -> None:
    codex_home = Path.home() / ".codex"
    for agent_file in sorted((DIST / "codex" / "agents").glob("*.toml")):
        sync_file(agent_file, codex_home / "agents" / agent_file.name)
    sync_skill_dirs(DIST / "codex" / "skills", codex_home / "skills")
    sync_markdown_guidance(codex_home / "AGENTS.md")
    sync_project_docs_guidance(codex_home / "AGENTS.md")
    sync_delivery_guidance("codex", codex_home, codex_home / "AGENTS.md")
    dotnet_routing = DIST / "tool-instructions" / "shared" / "dotnet-routing.md"
    sync_user_instruction_block(
        codex_home / "AGENTS.md",
        dotnet_routing.read_text(encoding="utf-8"),
        "DOTNET",
        ".NET routing",
    )


def sync_claude() -> None:
    claude_home = Path.home() / ".claude"
    for agent_file in sorted((DIST / "claude" / "agents").glob("*.md")):
        sync_file(agent_file, claude_home / "agents" / agent_file.name)
    sync_skill_dirs(DIST / "claude" / "skills", claude_home / "skills")
    sync_markdown_guidance(claude_home / "CLAUDE.md")
    sync_project_docs_guidance(claude_home / "CLAUDE.md")
    sync_delivery_guidance("claude", claude_home, claude_home / "CLAUDE.md")


def sync_tool_instructions(project: Path, tools: set[str], force: bool) -> None:
    project.mkdir(parents=True, exist_ok=True)

    agent_tool = next((tool for tool in ("codex", "claude") if tool in tools), None)
    if agent_tool:
        target = project / "AGENTS.md"
        write_or_splice_template(DIST / "tool-instructions" / agent_tool / "AGENTS.md", target, force)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install generated Codex and Claude Code adapters, skills, and tool instructions.")
    parser.add_argument("--tool", choices=["codex", "claude", "all"], default="all")
    parser.add_argument(
        "--project",
        action="append",
        default=[],
        help="Destination project root to receive tool instructions.",
    )
    parser.add_argument("--no-build", action="store_true", help="Skip rebuilding dist before sync.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Hard-overwrite project tool instructions and adopt unmarked legacy files.",
    )
    parser.add_argument(
        "--skip-external", action="store_true",
        help="Sync repository-generated content only, without external skill imports or network access.",
    )
    args = parser.parse_args()
    tools = external_skills.TOOLS if args.tool == "all" else {args.tool}
    entries = []
    if not args.skip_external:
        try:
            entries = external_skills.load_manifest()
            external_skills.preflight(entries, tools)
        except (external_skills.ImportError, OSError) as exc:
            print(f"EXTERNAL SKILLS ERROR: {exc}", file=sys.stderr)
            return 1

    if not args.no_build:
        run_build()

    if "codex" in tools:
        sync_codex()
    if "claude" in tools:
        sync_claude()

    for project in args.project:
        sync_tool_instructions(Path(project), tools, args.force)

    if not args.skip_external:
        try:
            external_skills.sync_external_skills(entries, tools)
        except (external_skills.ImportError, OSError) as exc:
            print(f"EXTERNAL SKILLS ERROR: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
