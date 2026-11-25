from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


def _load_module(name: str, path: Path):
    # Toolkit skills can also provide a package named scripts.
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
build = _load_module("ai_toolkit_build", ROOT / "scripts/build.py")
external_skills = _load_module("ai_toolkit_external_skills", ROOT / "scripts/external_skills.py")
contracts = _load_module("ai_toolkit_contracts", ROOT / "validation/delivery_contracts.py")
AGENT_EXTENSIONS = {"codex": "toml", "claude": "md"}
REPLACEMENT_AGENTS = (build.SENIOR_AGENT, "staff-engineer", "product-manager", "qa")
MARKER_START = "<!-- AI-TOOLKIT-LUCHDOM:START -->"
MARKER_END = "<!-- AI-TOOLKIT-LUCHDOM:END -->"
LEGACY_MARKER_PAIRS = (("<!-- AI-CONFIG-LUCHDOM:START -->", "<!-- AI-CONFIG-LUCHDOM:END -->"),)
# Known retired adapters from 3f4ba06 and the 6dcfbef writing-rule build.
RETIRED_AGENT_DIGESTS = {
    "codex": {
        "product-designer.toml": (
            "a2e6f1f839e76f22ec9c5260867db669e00ac5a8d8b277bc1337d3c24eb09d26",
            "0eb1dd0f8df61e5bf6965478769c7c7c9b68172f136042088d8596b119f13eed",
        ),
        "code-reviewer.toml": (
            "decf8c891dd2db7dd5cea5fa979ff05f64d20b2d5f7ae8e19e11be5c338dfd19",
            "767945a9ea614eec50f839ee4bbf51c4396c18a291b9324ac023957fa91e8d9c",
        ),
    },
    "claude": {
        "product-designer.md": (
            "4e662143ad3220631d770316f9c2824d6a7da1f6305696e6aa126a0932eb4504",
            "2523a50ccb0a65fd5af4be3b342fe3dd0e041702f6eaabd344b592c8a5cd0515",
        ),
        "code-reviewer.md": (
            "de171546c105817c1f92b5d21d596ee5561b559273a882a7664b9ae945f0db23",
            "031c9e41d53f1d24cd13e097afcf6087d0c64fcae9fc088f7cfb3f30c8e2fa95",
        ),
    },
}


def run_build() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py")], check=True)


def sync_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Copied {src} -> {dest}")


def _intact_senior_profile(tool: str, path: Path) -> bool:
    lines = path.read_bytes().replace(b"\r\n", b"\n").splitlines(keepends=True)
    return bool(lines) and lines[-1] == build.senior_agent_footer(tool, b"".join(lines[:-1]))


def _file_revision(metadata: os.stat_result) -> tuple[int, ...]:
    return (metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns, metadata.st_ctime_ns)


def _check_senior_destination(tool: str, tool_home: Path) -> tuple[int, ...] | None:
    target = tool_home / "agents" / f"{build.SENIOR_AGENT}.{AGENT_EXTENSIONS[tool]}"
    # The system temporary home can be an alias such as /var on macOS. Do not
    # resolve the tool home or the agent path inside that selected user home.
    user_home = tool_home.parent.resolve()
    candidate = user_home / tool_home.name / "agents" / target.name
    try:
        external_skills.check_path(candidate, user_home)
    except external_skills.ImportError as exc:
        raise ValueError(f"Preserved {target}. The agent path contains a symlink or junction.") from exc
    try:
        observed = candidate.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISREG(observed.st_mode) and observed.st_nlink == 1 and _intact_senior_profile(tool, candidate):
        return _file_revision(observed)
    raise ValueError(f"Preserved {target}. Move or back up this custom profile before installing the toolkit role.")


def preflight_agents(tools: set[str], home: Path) -> None:
    """Prove the complete build and each selected role destination before installation."""
    findings = contracts.check_projection_manifest(ROOT)
    if findings:
        raise ValueError(f"Rebuild dist before syncing. {findings[0]}")
    manifest = json.loads((DIST / "manifest.json").read_bytes())
    if manifest.get("generatedRoot") != "dist":
        raise ValueError("Rebuild dist before syncing. The manifest has a different output root.")
    by_source = {entry["source"]: entry["projections"] for entry in manifest["entries"]}
    for tool in sorted(tools):
        extension = AGENT_EXTENSIONS[tool]
        generated = DIST / tool / "agents"
        sources = {path.name for path in generated.glob(f"*.{extension}")}
        if sources.intersection(RETIRED_AGENT_DIGESTS[tool]):
            raise ValueError("Generated adapters still include a retired agent. Rebuild dist before syncing.")
        for role in REPLACEMENT_AGENTS:
            filename = f"{role}.{extension}"
            projections = by_source.get(f"src/agents/{role}.md", [])
            expected = f"dist/{tool}/agents/{filename}"
            if filename not in sources or expected not in {entry["path"] for entry in projections}:
                raise ValueError(f"Rebuild dist before syncing. Missing replacement projection {expected}.")
            external_skills.check_path(generated / filename, ROOT)
        senior = generated / f"{build.SENIOR_AGENT}.{extension}"
        if not _intact_senior_profile(tool, senior):
            raise ValueError(f"Rebuild dist before syncing. The generated Senior profile is unmarked or stale: {senior}.")
        _check_senior_destination(tool, home / f".{tool}")


def _install_senior(tool: str, tool_home: Path, source: Path) -> None:
    destination = tool_home / "agents" / source.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".ai-toolkit-", dir=destination.parent) as directory:
        staged = Path(directory) / "profile.tmp"
        shutil.copy2(source, staged)
        observed = _check_senior_destination(tool, tool_home)
        if observed is None:
            try:
                os.link(staged, destination)  # Exclusive first install.
            except FileExistsError as exc:
                raise ValueError(f"Preserved {destination}. Another profile appeared during installation.") from exc
        elif _file_revision(destination.lstat()) != observed:
            raise ValueError(f"Preserved {destination}. The managed profile changed during installation.")
        else:
            os.replace(staged, destination)
    print(f"Installed toolkit agent {destination}")


def sync_agents(tool: str, tool_home: Path, pattern: str) -> None:
    preflight_agents({tool}, tool_home.parent)
    destination = tool_home / "agents"
    sources = sorted((DIST / tool / "agents").glob(pattern))
    retired = RETIRED_AGENT_DIGESTS[tool]
    for source in sources:
        if source.stem == build.SENIOR_AGENT:
            _install_senior(tool, tool_home, source)
        else:
            sync_file(source, destination / source.name)

    for name, previous_hashes in retired.items():
        target = destination / name
        if not os.path.lexists(target):
            continue
        if target.is_symlink() or not target.is_file() or target.resolve() != target:
            print(f"Preserved retired agent path {target} (link or special file)")
            continue
        content = target.read_bytes().replace(b"\r\n", b"\n")
        if hashlib.sha256(content).hexdigest() in previous_hashes:
            target.unlink(missing_ok=True)
            print(f"Removed retired toolkit agent {target}")
        else:
            print(f"Preserved {target} (content differs from the retired toolkit agent)")


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
        )


def consume_newline(text: str, position: int) -> int:
    if text[position:position + 2] == "\r\n":
        return position + 2
    if text[position:position + 1] == "\n":
        return position + 1
    return position


def project_marker_spans(text: str, path: Path) -> list[tuple[int, int]]:
    end_by_start = dict(((MARKER_START, MARKER_END), *LEGACY_MARKER_PAIRS))
    pattern = "|".join(re.escape(marker) for marker in (*end_by_start, *end_by_start.values()))
    error = f"Malformed toolkit markers in {path}. Fix unmatched or overlapping blocks and rerun sync."
    spans: list[tuple[int, int]] = []
    start: re.Match[str] | None = None
    for marker in re.finditer(pattern, text):
        if start is None and marker.group() in end_by_start:
            start = marker
        elif start is not None and marker.group() == end_by_start[start.group()]:
            spans.append((start.start(), marker.end()))
            start = None
        else:
            raise ValueError(error)
    if start is not None:
        raise ValueError(error)
    return spans


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

    spans = project_marker_spans(existing, dest)
    if not spans:
        print(f"Skipped unmarked {dest}. Use --force only to replace the whole file.")
        return "skipped"

    first_start, end = spans[0]
    parts = [existing[:first_start], rendered.rstrip("\r\n")]
    for start, next_end in spans[1:]:
        parts.append(existing[end:start])
        end = next_end
    parts.append(existing[end:])
    updated = "".join(parts)
    if updated != existing:
        with open(dest, "w", encoding="utf-8", newline="") as file:
            file.write(updated)
        print(f"Spliced {dest} (preserved text outside managed blocks)")
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


def sync_reply_guidance(dest: Path) -> None:
    source = DIST / "tool-instructions" / "shared" / "reply-style.md"
    sync_user_instruction_block(dest, source.read_text(encoding="utf-8"), "REPLY-STYLE", "Writing")


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
        "Use this policy when an older project instruction points to the former Goal to Delivery location.\n"
        "<!-- AI-TOOLKIT-WORKTREES:END -->\n"
    )
    sync_user_instruction_block(instructions, block, "WORKTREES", "Git worktree")


def sync_codex() -> None:
    codex_home = Path.home() / ".codex"
    sync_agents("codex", codex_home, "*.toml")
    sync_skill_dirs(DIST / "codex" / "skills", codex_home / "skills")
    sync_markdown_guidance(codex_home / "AGENTS.md")
    sync_project_docs_guidance(codex_home / "AGENTS.md")
    sync_reply_guidance(codex_home / "AGENTS.md")
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
    sync_agents("claude", claude_home, "*.md")
    sync_skill_dirs(DIST / "claude" / "skills", claude_home / "skills")
    sync_markdown_guidance(claude_home / "CLAUDE.md")
    sync_project_docs_guidance(claude_home / "CLAUDE.md")
    sync_reply_guidance(claude_home / "CLAUDE.md")
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
        help="Replace the entire project AGENTS.md, including personal or unmarked instructions.",
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

    try:
        if len(tools) > 1:
            preflight_agents(tools, Path.home())
        if "codex" in tools:
            sync_codex()
        if "claude" in tools:
            sync_claude()
    except (OSError, ValueError, TypeError, AttributeError, KeyError, external_skills.ImportError) as exc:
        print(f"AGENT SYNC ERROR: {exc}", file=sys.stderr)
        return 1
    try:
        for project in args.project:
            sync_tool_instructions(Path(project), tools, args.force)
    except (OSError, ValueError) as exc:
        print(f"PROJECT SYNC ERROR: {exc}", file=sys.stderr)
        return 1

    if not args.skip_external:
        try:
            external_skills.sync_external_skills(entries, tools)
        except (external_skills.ImportError, OSError) as exc:
            print(f"EXTERNAL SKILLS ERROR: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
