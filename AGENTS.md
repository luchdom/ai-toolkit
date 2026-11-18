# AI Toolkit Repo Instructions

Use this repo as the source of truth for shared AI agents, skills, project-local tool instructions, and generated tool adapters.

Read [EXTERNAL-TOOLS.md](EXTERNAL-TOOLS.md) for companion CLIs, [EXTERNAL-SKILLS.md](EXTERNAL-SKILLS.md) for selected upstream imports and native plugins, and [MCP-SERVERS.md](MCP-SERVERS.md) for server configuration and authentication.

When changing project documentation skills, templates, or tool routing, read [Project documentation](docs/project-documentation.md) and its linked canonical standard.

## Platform selection

Before running setup or runtime commands, follow [platform support](docs/platform-support.md). Detect the execution host, active shell, actual checkout/home, and Python version; do not infer the OS from shell names, old paths, or imported memory. Run `python3 scripts/platform_info.py` on macOS or `py -3 scripts/platform_info.py` on Windows, then use the verified Python 3.11+ executable consistently. Keep Windows/PowerShell and macOS/POSIX instructions available together.

## Delivery workflow

Read the [shared workflow](src/tool-instructions/shared/delivery-workflow.md) to choose an entry and check its authority. It links the artifact contract, completion boundaries, and worktree policy.

- `$spec-driven-delivery` defines the stages. Use it for the requested stage when a non-trivial request names no entry.
- `$goal-to-delivery` runs those stages automatically for one selected goal.
- `$linear-delivery-loop` selects or resumes one Linear issue and hands it to Goal to Delivery.

`feature-driver` is a temporary alias for direct Goal to Delivery requests.

## When asked to install or sync the AI toolkit

1. Run the platform probe, then `python3 scripts/build.py` on macOS or `py -3 scripts/build.py` on Windows from the repo root. Substitute the verified Python 3.11+ executable when needed.
2. Run the same interpreter with `scripts/sync.py --tool <codex|claude|all>`. Normal sync includes the compatible selected imports in `external-skills.toml`; preview them with `scripts/external_skills.py --tool all --dry-run`. Use `--skip-external` for repository-generated content only. External imports preserve unmanaged or modified skills; `--force` does not bypass their protection.
3. If the user wants project-local tool instructions, add `--project <path>`.
4. `scripts/sync.py` resolves `{{LUCHDOM_AI_TOOLKIT_DOCS}}` in tool instructions from `LUCHDOM_AI_TOOLKIT_DOCS` when it is set, otherwise from the legacy `LUCHDOM_AI_CONFIG_DOCS` name or this repo's local `docs` folder.
5. Codex and Claude Code share the root `AGENTS.md`. Sync updates the block between `<!-- AI-TOOLKIT-LUCHDOM:START -->` and `<!-- AI-TOOLKIT-LUCHDOM:END -->` and preserves text outside it. Sync also migrates the legacy `AI-CONFIG-LUCHDOM` markers. Use `--force` to adopt an unmarked file. Back up local changes to toolkit-managed user agents and skills before syncing.
6. Verify the installed files exist after sync.

## Preferred behavior

- After creating or editing Markdown, follow [Markdown linting](docs/markdown-linting.md). Run `npm run lint:md:files -- ":path/to/changed.md"` for the exact changed files, fix findings in scope, and rerun before reporting completion.

- Prefer the scripts in this repo over manual copying.
- Treat `src/` as canonical and `dist/` as generated output.
- When the user says "install for me" without specifying a tool, run `scripts/sync.py --tool all` with the verified platform interpreter.
- If changing shared agents or skills, update `src/` and regenerate `dist/` instead of editing generated files directly.
- If changing shared project-local guidance, update the relevant files under `src/tool-instructions/`.
- Project-local tool instructions link to the shared workflow in `src/tool-instructions/shared/`.
- Follow `EXTERNAL-SKILLS.md` for selected imports and native plugins, `EXTERNAL-TOOLS.md` for companion CLIs, and `MCP-SERVERS.md` for explicit server setup. Prefer the linked official installation procedures. Normal skill sync does not install CLIs, run plugins, or configure MCP servers.
