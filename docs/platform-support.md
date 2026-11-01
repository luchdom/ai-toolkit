# Windows and macOS setup

Use the OS of the host executing the command, then choose syntax for its active shell. PowerShell also runs on macOS; its presence does not make the host Windows. A remote machine, container, or WSL session has its own OS, home, paths, and installed commands. Do not reuse paths from another host or imported history.

## Agent startup

1. Read the current execution context and repository instructions. Locate the actual checkout and user home; never assume `C:/dev`, `/Users/<name>/dev`, or a particular drive.
2. Run the read-only probe from the toolkit checkout with an available Python: `python3 scripts/platform_info.py` on macOS, or `py -3 scripts/platform_info.py` on Windows. A verified `python` executable is also usable. The JSON identifies the execution OS, architecture, Python executable/version, home, checkout, shell environment hints, and available command paths.
3. Require Python **3.11 or newer** for toolkit maintenance, including the TOML bootstrap helper. The probe itself runs on Python 3.9+ and exits 1 when the interpreter is too old or the host is outside the Windows/macOS support matrix. Select an installed supported interpreter and rerun it. Keep that same executable for build, validation, and sync.
4. Confirm the active shell from the execution tool before choosing syntax. `shellHints` are only environment hints. Verify needed CLIs with their version/status commands; a path in the probe means discoverable, not authenticated or working.
5. Follow the matching commands below, [External Skills](../EXTERNAL-SKILLS.md) for upstream imports and native plugins, [External Tools](../EXTERNAL-TOOLS.md) for companion CLIs, and [MCP Servers](../MCP-SERVERS.md) for explicit server setup. Unsupported hosts need their own verified commands; do not silently use the Windows branch.

The probe does not install tools, authenticate services, edit configuration, or select a delivery workflow.

## Build, validate, and sync

Run these from the toolkit checkout. Replace the Python command if the probe identified a different supported executable. Quote paths containing spaces; PowerShell invokes a quoted executable with `&`, while POSIX shells invoke it directly.

Windows / PowerShell:

```powershell
py -3 scripts/platform_info.py
py -3 scripts/build.py
py -3 scripts/validate.py
py -3 scripts/sync.py --tool all
# Optional project-local instructions; use the actual target path.
py -3 scripts/sync.py --tool all --project "C:/path/to/project"
```

macOS / zsh or another POSIX shell:

```sh
python3 scripts/platform_info.py
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/sync.py --tool all
# Optional project-local instructions; use the actual target path.
python3 scripts/sync.py --tool all --project "$HOME/path/to/project"
```

On macOS, `python3` may still select an older system interpreter even when a newer Python is installed. Use the verified newer executable or correct the shell PATH, then rerun the probe. Do not replace the system Python. On Windows without `py`, use a verified Python 3.11+ executable. Forward slashes in these Python script arguments work on both systems; environment assignment and shell continuation syntax do not carry across shells.

Normal sync includes compatible selected imports from [external-skills.toml](../external-skills.toml). It requires Git and network access to the pinned public repositories. Preview the local import plan with `python3 scripts/external_skills.py --tool all --dry-run` on macOS or `py -3 scripts/external_skills.py --tool all --dry-run` on Windows. Use `--skip-external` with `scripts/sync.py` for offline installation of repository-generated content only. CLI installation, plugin setup, MCP configuration, and login remain separate operations.

`scripts/validate.py` rebuilds generated adapters and runs the repository gate without syncing to a user home. Runtime path guards remain enabled.

## Paths and persistent state

| Purpose | Windows | macOS |
|---|---|---|
| Toolkit location | Actual checkout path | Actual checkout path |
| User-level adapters | `Path.home()/.codex`, `.claude`, `.copilot` | `Path.home()/.codex`, `.claude`, `.copilot` |

The sync script uses `Path.home()` for user-level destinations. Shared docs links are rendered from `LUCHDOM_AI_TOOLKIT_DOCS`, then legacy `LUCHDOM_AI_CONFIG_DOCS`, then this checkout's `docs` directory. These overrides must name a real location on the execution host. After moving the toolkit checkout, refresh marker-managed project instructions so their docs links point to the new location.

## Sync verification and recovery

Before a requested sync, compare and back up any intentional local changes to toolkit-managed agents and skills. Repository-generated user-level agents and skills are refreshed on every sync, including when `--project` is supplied. Agent model choices and sandbox settings are user/tool preferences, separate from platform selection; syncing canonical agents can replace local preferences.

Normal sync preflights the selected external imports before writing repository-generated output. External imports use ownership receipts and preserve unmanaged directories or locally modified imports; `--force` does not bypass these checks. Resolve a reported conflict using [external skill recovery](../EXTERNAL-SKILLS.md#ownership-conflicts-and-recovery), or explicitly select `--skip-external` to sync only repository-generated content.

Project instruction files preserve text outside toolkit markers. Existing unmarked instruction files, project Copilot agents/skills, and Cursor rules are skipped unless `--force` is supplied. `--force` replaces project instruction files in full; use it only when that replacement is intended.

After sync, verify the intended destination files exist and inspect the rendered docs path. To undo a sync, restore the backed-up managed files and instruction blocks. Do not delete unrelated skills or tool configuration. Repo development needs build/validation only; syncing live user homes is a separate installation action.

Windows-only junction/locking checks require a native Windows run. Simulated platform branches on macOS establish default selection, not native Windows filesystem behavior.
