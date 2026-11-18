# External skill guide

[external-skills.toml](external-skills.toml) lists the pinned external skill imports, their one-line descriptions, and the preview and sync commands.

## Add or update an import

1. Review the upstream `SKILL.md`, license, supporting files, runtime requirements, and agent compatibility at the intended commit.
2. Add a `[[skills]]` block under its upstream repository heading. Add one short comment under `name` that describes what the skill does.
3. To update an import, review the upstream changes and replace `revision`. Keep `name` stable so the same destination receives the update.

### Manifest fields

The manifest uses `version = 1`. Each `[[skills]]` block contains the following fields.

| Field | Value |
| --- | --- |
| `name` | Destination directory name. Use a portable name distinct from other entries and names in `src/skills/`. |
| `repo` | Public GitHub HTTPS repository URL ending in `.git`. |
| `path` | Repository-relative directory containing `SKILL.md`. Use `.` for the repo root. |
| `revision` | Full lowercase 40-character Git commit SHA. Sync fetches this commit on every import. |
| `tools` | One or more distinct compatible targets from `codex`, `claude`, `copilot`, and `cursor`. |

Replace the example values with those from the reviewed source.

```toml
[[skills]]
name = "example-skill"
# Summarize what the skill does.
repo = "https://github.com/example/example-skills.git"
path = "skills/example-skill"
revision = "0123456789abcdef0123456789abcdef01234567"
tools = ["codex", "claude"]
```

## How sync uses the manifest

The importer selects entries whose `tools` include the requested agent. It copies each skill directory and its bundled files at the pinned revision. Codex, Claude Code, and Copilot use user-level destinations. Cursor uses the supplied project. The preview checks the selection and destination ownership locally.

## Exclude an import

- **Exclude one skill from all syncs.** Remove or comment out its entire `[[skills]]` block. If the manifest becomes empty, keep `version = 1` and set `skills = []`.
- **Exclude a skill for one agent.** Remove that agent from the entry's `tools` array. Remove the block if there are no compatible targets left.

Exclusions take effect on future syncs. Use the removal steps below to remove an installed copy as well.

## Ownership, conflicts, and recovery

Sync records each import's source and file hashes in `.ai-toolkit-external-skills.json` beside the installed directories. It replaces an existing directory only if it recognizes the import and the installed files match the recorded hashes. These checks also apply when toolkit sync uses `--force`.

- **Resolve a conflict.** Inspect and back up the exact unmanaged or modified skill before moving it out of the agent's skill directories.
- **Roll back an update.** Verify the installed import matches its receipt, then restore the previous manifest pin.
- **Remove an installed import.** Exclude the skill from that destination first. Back up and remove its exact directory, then remove only its entry from the receipt.
- **Recover an interrupted replacement.** If sync reports a retained recovery directory, preserve it and the existing receipt. Use the retained `previous` directory to restore the affected skill before retrying.
