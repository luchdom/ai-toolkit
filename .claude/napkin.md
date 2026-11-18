# Napkin Runbook

## Execution and Validation

1. **[2026-10-21] Use a modern Python for toolkit generation**
   Do instead: run `scripts/platform_info.py` with the available interpreter and keep a verified Python 3.11+ executable for maintenance. Apple system Python 3.9 is too old; PATH may select a newer package-managed Python.

2. **[2026-10-21] Preserve intentional installation preferences**
   Do instead: compare installed agents and skills before syncing and back up intentional model/sandbox preferences. User-level sync overwrites these files; platform runtime defaults now live in canonical source.

3. **[2026-10-21] Avoid the macOS temporary-directory symlink in validation**
   Do instead: run `scripts/validate.py`, which passes a physical temporary base to subprocesses. Direct workflow test fixtures also resolve their root. Keep runtime symlink rejection intact.
