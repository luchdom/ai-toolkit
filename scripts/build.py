from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"
SKILL_REF_PATTERN = re.compile(r"\$([a-z0-9][a-z0-9-]*)")
MANIFEST_VERSION = 1
SKILL_ADAPTERS = ("codex", "claude")
TWELVE_FACTOR_GUIDE = Path("docs/twelve-factor-for-agentic-development.md")
SHARED_DELIVERY_FILES = (
    "artifact-contract.md",
    "completion-boundaries.md",
    "delivery-workflow.md",
    TWELVE_FACTOR_GUIDE.name,
    "worktrees.md",
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("Agent source must start with YAML-like frontmatter.")

    try:
        _, raw_frontmatter, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError("Invalid frontmatter block.") from exc

    meta: dict[str, str] = {}
    for line in raw_frontmatter.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        key, value = stripped.split(":", 1)
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = json.loads(value)
        meta[key.strip()] = value
    return meta, body.lstrip("\n")


def render_codex_toml(meta: dict[str, str], body: str) -> str:
    return (
        f'name = {json.dumps(meta["name"])}\n'
        f'description = {json.dumps(meta["description"])}\n'
        f'model = {json.dumps(meta["codex_model"])}\n'
        f'model_reasoning_effort = {json.dumps(meta["codex_model_reasoning_effort"])}\n'
        f'sandbox_mode = {json.dumps(meta["codex_sandbox_mode"])}\n\n'
        'developer_instructions = """\n'
        f"{body.rstrip()}\n"
        '"""\n'
    )


def render_claude_agent(meta: dict[str, str], body: str) -> str:
    lines = [
        "---",
        f'name: {json.dumps(meta["name"])}',
        f'description: {json.dumps(meta["description"])}',
        f'model: {json.dumps(meta.get("claude_model", "inherit"))}',
    ]
    if meta.get("claude_effort"):
        lines.append(f'effort: {json.dumps(meta["claude_effort"])}')
    if meta.get("claude_disallowed_tools"):
        lines.append(f'disallowedTools: {json.dumps(meta["claude_disallowed_tools"])}')
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.rstrip() + "\n"


def validate_tool_instruction_skills() -> None:
    available_skills = {path.name for path in (SRC / "skills").iterdir() if path.is_dir()}
    errors: list[str] = []

    for instruction_path in sorted((SRC / "tool-instructions").rglob("*")):
        if instruction_path.name == ".DS_Store" or not instruction_path.is_file():
            continue
        for skill_id in sorted(set(SKILL_REF_PATTERN.findall(instruction_path.read_text(encoding="utf-8")))):
            if skill_id not in available_skills:
                errors.append(f"{instruction_path}: references unknown skill id ${skill_id}.")

    if errors:
        raise ValueError("Tool instruction skill validation failed:\n" + "\n".join(errors))


def validate_agent_fields() -> None:
    required = ("name", "description", "codex_model", "codex_model_reasoning_effort", "codex_sandbox_mode")
    errors: list[str] = []

    for agent_path in sorted((SRC / "agents").glob("*.md")):
        meta, _ = parse_frontmatter(agent_path.read_text(encoding="utf-8"))
        missing = [field for field in required if not meta.get(field)]
        if missing:
            errors.append(f"{agent_path.name}: missing required frontmatter {', '.join(missing)}.")
        if meta.get("claude_effort") and not meta.get("claude_model"):
            errors.append(f"{agent_path.name}: claude_effort requires claude_model.")

    if errors:
        raise ValueError("Agent frontmatter validation failed:\n" + "\n".join(errors))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def write_projection_manifest(projections: dict[Path, list[Path]]) -> None:
    """Record exactly which canonical source produced each generated file."""
    entries: list[dict[str, object]] = []
    for source in sorted(projections, key=lambda path: path.as_posix()):
        outputs = sorted(projections[source], key=lambda path: path.as_posix())
        entries.append(
            {
                "source": source.relative_to(ROOT).as_posix(),
                "sourceSha256": file_sha256(source),
                "projections": [
                    {
                        "path": output.relative_to(ROOT).as_posix(),
                        "sha256": file_sha256(output),
                    }
                    for output in outputs
                ],
            }
        )
    manifest = {
        "schemaVersion": MANIFEST_VERSION,
        "canonicalRoot": "src",
        "generatedRoot": "dist",
        "entries": entries,
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def rebuild_dist() -> None:
    validate_tool_instruction_skills()
    validate_agent_fields()

    if DIST.exists():
        shutil.rmtree(DIST)

    for tool in SKILL_ADAPTERS:
        (DIST / tool / "agents").mkdir(parents=True, exist_ok=True)
        (DIST / tool / "skills").mkdir(parents=True, exist_ok=True)
        (DIST / "tool-instructions" / tool).mkdir(parents=True, exist_ok=True)

    projections: dict[Path, list[Path]] = {}

    shared = Path("tool-instructions/shared")
    for source in (*sorted((SRC / shared).glob("*.md")), ROOT / TWELVE_FACTOR_GUIDE):
        destinations = [DIST]
        if source.name in SHARED_DELIVERY_FILES:
            # Match the source layout so links from skills work after sync.
            destinations = [DIST / tool for tool in SKILL_ADAPTERS]
        outputs = [destination / shared / source.name for destination in destinations]
        for output in outputs:
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, output)
        projections[source] = outputs

    markdown_guidance = (SRC / shared / "markdown-lint.md").read_text(encoding="utf-8")
    project_docs_guidance = (SRC / shared / "project-docs.md").read_text(encoding="utf-8")
    config_source = SRC / shared / "markdownlint.json"
    config_output = DIST / shared / "markdownlint-cli2.jsonc"
    config_output.write_text(
        json.dumps({"config": json.loads(config_source.read_text(encoding="utf-8"))}, indent=2) + "\n",
        encoding="utf-8",
    )
    projections[config_source] = [config_output]

    installed_guide = shared / TWELVE_FACTOR_GUIDE.name
    for agent_path in sorted((SRC / "agents").glob("*.md")):
        meta, body = parse_frontmatter(agent_path.read_text(encoding="utf-8"))
        body = body.replace(f"../../{TWELVE_FACTOR_GUIDE.as_posix()}", f"../{installed_guide.as_posix()}")
        body = body.rstrip() + "\n\n" + markdown_guidance + "\n" + project_docs_guidance
        codex_text = render_codex_toml(meta, body)
        claude_text = render_claude_agent(meta, body)
        outputs = [
            DIST / "codex" / "agents" / f"{agent_path.stem}.toml",
            DIST / "claude" / "agents" / f"{agent_path.stem}.md",
        ]
        for output, content in zip(outputs, (codex_text, claude_text), strict=True):
            output.write_text(content, encoding="utf-8")
        projections[agent_path] = outputs

    for skill_dir in sorted((SRC / "skills").iterdir()):
        if skill_dir.is_dir():
            destinations = [DIST / tool / "skills" / skill_dir.name for tool in SKILL_ADAPTERS]
            for destination in destinations:
                shutil.copytree(
                    skill_dir,
                    destination,
                    ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
                )
            for source in sorted(
                path
                for path in skill_dir.rglob("*")
                if path.is_file()
                and path.name != ".DS_Store"
                and "__pycache__" not in path.parts
                and path.suffix != ".pyc"
            ):
                relative = source.relative_to(skill_dir)
                projections[source] = [destination / relative for destination in destinations]

    for tool in SKILL_ADAPTERS:
        relative = Path(tool) / "AGENTS.md"
        source = SRC / "tool-instructions" / relative
        if source.exists():
            output = DIST / "tool-instructions" / relative
            output.write_text(
                source.read_text(encoding="utf-8").replace(
                    "{{PROJECT_DOCUMENTATION_GUIDANCE}}", project_docs_guidance.rstrip()
                ),
                encoding="utf-8",
            )
            projections[source] = [output]

    write_projection_manifest(projections)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Codex and Claude Code adapters from canonical AI config sources.")
    parser.parse_args()
    rebuild_dist()
    print("Built adapters into dist/.")


if __name__ == "__main__":
    main()
