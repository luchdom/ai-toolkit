# AI Toolkit Repo Instructions

Use this repo as the source of truth for shared AI agents, skills, project-local tool instructions, and generated tool adapters.

Read [EXTERNAL-TOOLS.md](EXTERNAL-TOOLS.md) for companion CLIs, [EXTERNAL-SKILLS.md](EXTERNAL-SKILLS.md) for selected upstream imports and native plugins, and [MCP-SERVERS.md](MCP-SERVERS.md) for server configuration and authentication.

## Platform selection

Before running setup or runtime commands, follow [platform support](docs/platform-support.md). Detect the execution host, active shell, actual checkout/home, and Python version; do not infer the OS from shell names, old paths, or imported memory. Run `python3 scripts/platform_info.py` on macOS or `py -3 scripts/platform_info.py` on Windows, then use the verified Python 3.11+ executable consistently. Keep Windows/PowerShell and macOS/POSIX instructions available together.

## Delivery workflow ownership

- Exactly three user-facing delivery entries exist: `$goal-to-delivery`, `$spec-driven-delivery`, and `$linear-delivery-loop`.
- For non-trivial work without an explicit entry, default to manual `$spec-driven-delivery`; execute only the requested stage and never infer implementation or publication authority.
- The sole canonical cross-tool protocol is under `src/skills/goal-to-delivery/references/`. Other entry skills and tool instructions link to it rather than copying it.
- Repositories own their project-specific commands, domain rules, definitions of done, and stricter safety constraints.
- Precedence is user/system requirements and repository-specific stricter safety, then the explicitly invoked entry policy, then the canonical shared contract. Unresolved conflict fails closed before implementation or external mutation.
- Use the workflow descriptor's exact registered `artifactFolder`: new/current work belongs under `.ai/work`, an exact registered legacy workflow may continue only at its exact `docs-ai` path, and unregistered or tracked historical `docs-ai` evidence is read-only.
- `feature-driver` is a deprecated one-migration-cycle semi-autonomous alias only. It never routes autonomous work.
- The MVP autonomous entry uses Linear as its durable queue and `.ai/loop.json` as project configuration; it does not require a separate supervisor or memory service.

## When asked to install or sync the AI toolkit

1. Run the platform probe, then `python3 scripts/build.py` on macOS or `py -3 scripts/build.py` on Windows from the repo root. Substitute the verified Python 3.11+ executable when needed.
2. Run the same interpreter with `scripts/sync.py --tool <codex|claude|copilot|cursor|all>`. Normal sync includes the compatible selected imports in `external-skills.toml`; preview them with `scripts/external_skills.py --tool all --dry-run`. Use `--skip-external` for repository-generated content only. External imports preserve unmanaged or modified skills; `--force` does not bypass their protection.
3. If the user wants project-local tool instructions, add `--project <path>`.
4. `scripts/sync.py` resolves `{{LUCHDOM_AI_TOOLKIT_DOCS}}` in tool instructions from `LUCHDOM_AI_TOOLKIT_DOCS` when it is set, otherwise from the legacy `LUCHDOM_AI_CONFIG_DOCS` name or this repo's local `docs` folder.
5. `AGENTS.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` are marker-managed: normal sync emits `<!-- AI-TOOLKIT-LUCHDOM:START -->` and `:END`, accepts and migrates the legacy `AI-CONFIG-LUCHDOM` markers, and preserves content outside them. Existing unmarked files remain untouched unless `--force` explicitly adopts them. Project Copilot agents/skills and Cursor rules remain skip-unless-`--force`. Repository-generated user-level agents and skills are refreshed on every sync; compare and back up intentional local preferences first.
6. Verify the installed files exist after sync.

## Preferred behavior

- After creating or editing Markdown, follow [Markdown linting](docs/markdown-linting.md). Run `npm run lint:md:files -- ":path/to/changed.md"` for the exact changed files, fix findings in scope, and rerun before reporting completion.

- Prefer the scripts in this repo over manual copying.
- Treat `src/` as canonical and `dist/` as generated output.
- When the user says "install for me" without specifying a tool, run `scripts/sync.py --tool all` with the verified platform interpreter.
- If changing shared agents or skills, update `src/` and regenerate `dist/` instead of editing generated files directly.
- If changing shared project-local guidance, update the relevant files under `src/tool-instructions/`.
- Project-local tool instructions route the three explicit entries and worktree behavior into the canonical shared protocol and default unspecified non-trivial work to manual stage control.
- Follow `EXTERNAL-SKILLS.md` for selected imports and native plugins, `EXTERNAL-TOOLS.md` for companion CLIs, and `MCP-SERVERS.md` for explicit server setup. Prefer the linked official installation procedures. Normal skill sync does not install CLIs, run plugins, or configure MCP servers.
- Copilot support in this repo uses user-level `~/.copilot/agents` and `~/.copilot/skills`, plus project-level `.github/agents`, `.github/skills`, and `.github/copilot-instructions.md`.
- Cursor support in this repo is project-level only. Generate `AGENTS.md` plus `.cursor/rules/*.mdc` into the target repo when the user asks for Cursor support. Compatible selected external skills use `.cursor/skills/` and require `--project`.
