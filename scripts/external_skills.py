"""Import selected, pinned skill directories without running upstream code."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import tomllib
import unicodedata
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "external-skills.toml"
TOOLS = {"codex", "claude", "copilot", "cursor"}
RECEIPT = ".ai-toolkit-external-skills.json"
RESERVED = re.compile(r"^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)", re.I)


class ImportError(ValueError):
    """An unsafe or unsuccessful external skill import."""


def safe_name(value: object) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", value)) and not value.endswith(".") and not RESERVED.match(value)


def safe_source_path(value: object) -> bool:
    if value == ".":
        return True
    return isinstance(value, str) and not value.endswith("/") and safe_inventory_path(value)


def load_manifest(path: Path = MANIFEST, canonical_root: Path | None = None) -> list[dict]:
    """Validate the complete selection before any destination is changed."""
    try:
        with path.open("rb") as stream:
            document = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ImportError("Cannot read a valid external-skills.toml manifest.") from exc
    if set(document) != {"version", "skills"} or type(document["version"]) is not int or document["version"] != 1 or not isinstance(document["skills"], list):
        raise ImportError("External skills manifest requires version = 1 and a skills array only.")
    canonical_root = canonical_root if canonical_root is not None else ROOT / "src" / "skills"
    canonical = {p.name.casefold() for p in canonical_root.iterdir() if p.is_dir()}
    names: set[str] = set()
    for entry in document["skills"]:
        if not isinstance(entry, dict) or set(entry) != {"name", "repo", "path", "revision", "tools"}:
            raise ImportError("Each external skill requires name, repo, path, revision, and tools only.")
        name = entry["name"]
        if not safe_name(name):
            raise ImportError("External skill name must be one portable directory name.")
        if name.casefold() in names or name.casefold() in canonical:
            raise ImportError(f"Duplicate or repository-owned skill name: {name}")
        names.add(name.casefold())
        if not isinstance(entry["repo"], str) or not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git", entry["repo"]):
            raise ImportError(f"Skill {name} needs a public HTTPS GitHub .git URL without credentials.")
        if not safe_source_path(entry["path"]):
            raise ImportError(f"Skill {name} has an unsafe repository-relative path.")
        if not isinstance(entry["revision"], str) or not re.fullmatch(r"[0-9a-f]{40}", entry["revision"]):
            raise ImportError(f"Skill {name} needs a full lowercase 40-character commit revision.")
        targets = entry["tools"]
        if not isinstance(targets, list) or not targets or any(not isinstance(t, str) or t not in TOOLS for t in targets) or len(set(targets)) != len(targets):
            raise ImportError(f"Skill {name} needs distinct supported tool names.")
    return document["skills"]


def is_link_or_reparse(path: Path) -> bool:
    """Detect Windows junctions on Python 3.11 as well as ordinary symlinks."""
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(metadata.st_mode) or bool(
        getattr(metadata, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def check_path(path: Path, boundary: Path) -> None:
    """Refuse links/reparse points, including ancestors of a selected boundary."""
    try:
        path.relative_to(boundary)
    except ValueError as exc:
        raise ImportError("External skill destination escapes its selected home or project.") from exc
    for candidate in [*reversed(path.parents), path]:
        if is_link_or_reparse(candidate):
            raise ImportError("External skill destination contains a symlink or junction; preserved existing content.")


def tree_hashes(directory: Path) -> dict[str, str]:
    """Hash contents and executable bits, including empty directories."""
    if is_link_or_reparse(directory) or not directory.is_dir():
        raise ImportError("A skill must be a regular directory, not a symlink.")
    result = {}
    aliases = set()
    for item in sorted(directory.rglob("*")):
        relative = item.relative_to(directory).as_posix()
        if is_link_or_reparse(item):
            raise ImportError("Skill content contains a symlink or junction; import refused.")
        if not safe_inventory_path(relative) or relative.casefold() in aliases:
            raise ImportError("Skill content has a non-portable relative path; import refused.")
        aliases.add(relative.casefold())
        mode = item.stat().st_mode
        if stat.S_ISDIR(mode):
            result[relative + "/"] = "directory"
        elif stat.S_ISREG(mode):
            result[relative] = hashlib.sha256(item.read_bytes() + str(mode & 0o111).encode()).hexdigest()
        else:
            raise ImportError("Skill content contains a non-regular file; import refused.")
    return result


def fetch_skill(entry: dict, directory: Path) -> Path:
    """Fetch only the pinned commit, with user Git hooks/configuration disabled."""
    # This is an importer-owned temporary directory; normalize host aliases such as macOS /var.
    directory = directory.resolve()
    repository = directory / "repository"
    template = directory / "empty-template"
    template.mkdir()
    environment = os.environ.copy()
    for key in list(environment):
        if key.startswith("GIT_"):
            del environment[key]
    environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
    common = ["git", "-c", f"core.hooksPath={template}", "-c", "protocol.file.allow=never"]
    commands = [
        [*common, "init", f"--template={template}", str(repository)],
        [*common, "-C", str(repository), "fetch", "--depth=1", "--no-tags", entry["repo"], entry["revision"]],
        [*common, "-C", str(repository), "checkout", "--detach", "FETCH_HEAD"],
    ]
    try:
        for command in commands:
            subprocess.run(command, check=True, capture_output=True, env=environment, timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ImportError(f"Git fetch/checkout failed for {entry['name']}; check Git/network access and the pinned commit.") from exc
    source = repository / entry["path"]
    check_path(source, repository)
    if not (source / "SKILL.md").is_file() or (source / "SKILL.md").is_symlink():
        raise ImportError(f"Pinned source for {entry['name']} has no SKILL.md.")
    shutil.rmtree(repository / ".git")
    return source


def safe_inventory_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or unicodedata.normalize("NFC", value) != value:
        return False
    parts = value.removesuffix("/").split("/")
    return all(part.casefold() not in {"", ".", "..", ".git"} and not RESERVED.match(part) and not part.endswith((".", " ")) and not any(ord(c) < 32 or c in '<>:\"|?*' for c in part) for part in parts)


def load_receipt(root: Path, boundary: Path) -> dict:
    receipt = root / RECEIPT
    check_path(receipt, boundary)
    if not receipt.exists():
        return {"version": 1, "skills": {}}
    try:
        data = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ImportError("Invalid external skill receipt; preserved existing content.") from exc
    if not isinstance(data, dict) or set(data) != {"version", "skills"} or type(data["version"]) is not int or data["version"] != 1 or not isinstance(data["skills"], dict):
        raise ImportError("Invalid external skill receipt; preserved existing content.")
    if len({name.casefold() for name in data["skills"]}) != len(data["skills"]):
        raise ImportError("Invalid external skill receipt; duplicate names.")
    for name, entry in data["skills"].items():
        if not safe_name(name) or not isinstance(entry, dict) or set(entry) != {"repo", "path", "revision", "files"} or not isinstance(entry["files"], dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in entry["files"].items()):
            raise ImportError("Invalid external skill receipt; preserved existing content.")
        if not isinstance(entry["repo"], str) or not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.git", entry["repo"]) or not safe_source_path(entry["path"]) or not isinstance(entry["revision"], str) or not re.fullmatch(r"[0-9a-f]{40}", entry["revision"]):
            raise ImportError("Invalid external skill receipt source identity.")
        aliases = set()
        for name, digest in entry["files"].items():
            if not safe_inventory_path(name) or name.casefold().removesuffix("/") in aliases or (digest != "directory" if name.endswith("/") else not re.fullmatch(r"[0-9a-f]{64}", digest)):
                raise ImportError("Invalid external skill receipt inventory.")
            aliases.add(name.casefold().removesuffix("/"))
    return data


def targets(entry: dict, tools: set[str], home: Path, projects: Iterable[Path]) -> list[tuple[Path, Path]]:
    result = []
    for tool in sorted(set(entry["tools"]) & tools):
        if tool == "cursor":
            result.extend((project / ".cursor" / "skills", project) for project in projects)
        else:
            result.append((home / f".{tool}" / "skills", home))
    return list(dict.fromkeys(result))


def install_skill(entry: dict, source: Path, root: Path, boundary: Path) -> str:
    destination = root / entry["name"]
    check_path(destination, boundary)
    receipt = load_receipt(root, boundary)
    files = tree_hashes(source)
    desired = {key: entry[key] for key in ("repo", "path", "revision")}
    desired["files"] = files
    previous = receipt["skills"].get(entry["name"])
    current = tree_hashes(destination) if destination.exists() else None
    if current is not None:
        if previous is None:
            raise ImportError(f"Unmanaged skill {entry['name']} already exists; preserved existing content.")
        if current != previous["files"]:
            raise ImportError(f"Locally modified skill {entry['name']}; preserved existing content.")
        if current == files and previous == desired:
            return "unchanged"
    root.mkdir(parents=True, exist_ok=True)
    # A sibling staging directory keeps every rename on the same filesystem.
    staging = Path(tempfile.mkdtemp(prefix=".ai-toolkit-import-", dir=root))
    recovery_required = False
    try:
        replacement = staging / "skill"
        shutil.copytree(source, replacement)
        if tree_hashes(replacement) != files:
            raise ImportError("Skill content changed while staging; import refused.")
        updated = {"version": 1, "skills": {**receipt["skills"], entry["name"]: desired}}
        staged_receipt = staging / "receipt.json"
        staged_receipt.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        # Recheck before replacing; roll back the skill if the receipt cannot commit.
        check_path(destination, boundary)
        check_path(root / RECEIPT, boundary)
        if load_receipt(root, boundary) != receipt or (tree_hashes(destination) if destination.exists() else None) != current:
            raise ImportError("External skill destination changed during import; preserved existing content.")
        backup = staging / "previous"
        had_previous = destination.exists()
        if had_previous:
            destination.rename(backup)
        installed = False
        try:
            replacement.rename(destination)
            installed = True
            os.replace(staged_receipt, root / RECEIPT)
        except OSError:
            try:
                if installed:
                    shutil.rmtree(destination)
                if had_previous:
                    backup.rename(destination)
            except OSError as exc:
                recovery_required = True
                raise ImportError(
                    "External skill rollback incomplete; reconciliation required. "
                    f"Recovery directory retained at {json.dumps(str(staging), ensure_ascii=True)}. "
                    "Preserve this directory and the existing receipt until recovery is complete."
                ) from exc
            raise
    finally:
        if not recovery_required:
            shutil.rmtree(staging)
    return "updated" if current is not None else "installed"


def preflight(entries: list[dict], tools: set[str], projects: Iterable[Path] = (), *, home: Path | None = None) -> None:
    """Check local ownership/conflicts before any legacy or external sync writes."""
    home = (home if home is not None else Path.home()).absolute()
    projects = [path.expanduser().absolute() for path in projects]
    for entry in entries:
        for root, boundary in targets(entry, tools, home, projects):
            destination = root / entry["name"]
            check_path(destination, boundary)
            receipt = load_receipt(root, boundary)
            if destination.exists():
                previous = receipt["skills"].get(entry["name"])
                if previous is None:
                    raise ImportError(f"Unmanaged skill {entry['name']} already exists; move or back it up before importing. Existing content preserved.")
                if tree_hashes(destination) != previous["files"]:
                    raise ImportError(f"Locally modified skill {entry['name']}; back up or reconcile it before importing. Existing content preserved.")


def sync_external_skills(entries: list[dict], tools: set[str], projects: Iterable[Path] = (), *, home: Path | None = None, dry_run: bool = False, fetcher: Callable[[dict, Path], Path] = fetch_skill) -> None:
    home = home if home is not None else Path.home()
    home = home.absolute()
    projects = [path.expanduser().absolute() for path in projects]
    preflight(entries, tools, projects, home=home)
    failures = 0
    for entry in entries:
        destinations = targets(entry, tools, home, projects)
        if not destinations:
            print(f"Skipped external skill {entry['name']} (no selected compatible destination)")
            continue
        if dry_run:
            for root, boundary in destinations:
                check_path(root / entry["name"], boundary)
                load_receipt(root, boundary)
                print(f"Would sync external skill {entry['name']} at {entry['revision']} -> {root / entry['name']}")
            continue
        try:
            with tempfile.TemporaryDirectory(prefix="ai-toolkit-fetch-") as temporary:
                source = fetcher(entry, Path(temporary).resolve())
                if not (source / "SKILL.md").is_file():
                    raise ImportError(f"Pinned source for {entry['name']} has no SKILL.md.")
                tree_hashes(source)
                for root, boundary in destinations:
                    try:
                        outcome = install_skill(entry, source, root, boundary)
                        print(f"External skill {entry['name']}: {outcome} -> {root / entry['name']}")
                    except (ImportError, OSError) as exc:
                        failures += 1
                        reason = str(exc) if isinstance(exc, ImportError) else "destination write failed; existing content preserved"
                        print(f"FAILED external skill {entry['name']}: {reason}", file=sys.stderr)
        except (ImportError, OSError) as exc:
            failures += 1
            message = str(exc) if isinstance(exc, ImportError) else "source could not be read"
            print(f"FAILED external skill {entry['name']}: {message}", file=sys.stderr)
    if failures:
        raise ImportError(f"External skill sync failed for {failures} import(s); resolve conflicts or use --skip-external for repository-only sync.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=[*sorted(TOOLS), "all"], default="all")
    parser.add_argument("--project", action="append", default=[], type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Show the local import plan without network access or writes.")
    args = parser.parse_args()
    try:
        entries = load_manifest()
        sync_external_skills(entries, TOOLS if args.tool == "all" else {args.tool}, args.project, dry_run=args.dry_run)
    except (ImportError, OSError) as exc:
        print(f"EXTERNAL SKILLS ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
