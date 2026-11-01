# External Skills

This repository records the external skills we want to restore into an agent environment. [external-skills.toml](external-skills.toml) is the selected import list; this document explains the process and catalogs native installers and plugins that stay separate.

Repository-owned skills remain canonical under `src/skills/` and are generated into `dist/`. Imported skills stay upstream and are copied directly into the selected environment. They do not become editable source under `src/` or generated `dist/` content.

## Import the Selected Skills

Start with [platform support](docs/platform-support.md). Use Python 3.11 or newer and Git. Normal toolkit sync installs both repository-generated content and the compatible external imports:

macOS / zsh:

```sh
python3 scripts/platform_info.py
python3 scripts/sync.py --tool all
```

Windows / PowerShell:

```powershell
py -3 scripts/platform_info.py
py -3 scripts/sync.py --tool all
```

Use `--skip-external` for offline sync of repository-generated content only. This skips every external import, including the manifest's selected entries. CLI tools, plugins, MCP configuration, and authentication remain separate setup steps.

Preview only the external imports without downloads or filesystem writes:

```sh
python3 scripts/external_skills.py --tool all --dry-run
```

```powershell
py -3 scripts/external_skills.py --tool all --dry-run
```

Install only the selected external imports without rebuilding or syncing repository-generated content:

```sh
python3 scripts/external_skills.py --tool codex
```

```powershell
py -3 scripts/external_skills.py --tool codex
```

Use `--project "/actual/project/path"` with either command when project destinations are required. The option is repeatable. A dry run validates the local manifest and destination plan; it cannot prove that a remote revision, skill directory, or service is available.

### Destinations and Compatibility

| Tool | External skill destination |
| --- | --- |
| Codex | `~/.codex/skills/<name>` |
| Claude Code | `~/.claude/skills/<name>` |
| GitHub Copilot CLI | `~/.copilot/skills/<name>` |
| Cursor | `<project>/.cursor/skills/<name>`; requires `--project` |

See [Cursor's skill documentation](https://cursor.com/docs/skills) for its project skill directory and discovery behavior.

An import is installed only for the tools declared in its manifest entry and selected by `--tool`. A skill written for one agent is not converted automatically for another. Cursor entries without a project are reported as skipped.

The importer fetches the pinned Git revision and copies the complete skill directory, including supporting scripts, references, and assets. It does not execute those scripts, upstream installers, lifecycle hooks, plugin commands, or MCP setup. Review upstream instructions before selecting a skill. Restart the agent after installation and verify its available skill list; files on disk alone do not prove that the current session loaded them.

## Maintain the Import List

All `[[skills]]` entries in [external-skills.toml](external-skills.toml) are selected. Do not duplicate the list in this document. Each entry contains:

| Field | Meaning |
| --- | --- |
| `name` | Portable destination directory name; unique across the manifest |
| `repo` | Public GitHub HTTPS repository URL ending in `.git` |
| `path` | Skill directory inside the repository; `.` means its root |
| `revision` | Full 40-character Git commit SHA |
| `tools` | Explicit compatible targets: `codex`, `claude`, `copilot`, or `cursor` |

The top-level `version` is `1`. Names cannot collide with repository-owned `src/skills` names. The importer rejects malformed or unknown fields, duplicate names, unsafe paths, symlink content, and invalid revisions before importing.

To add a skill, inspect its upstream `SKILL.md`, supporting files, license, and agent requirements. Choose only the needed skill directories, resolve a full commit SHA, add the entry, preview, and install into a disposable test environment before changing a live environment. Prefer the project's native installer when its skills depend on generated bundles, plugins, hooks, or other setup.

To update, inspect the upstream changes, replace the pinned SHA, preview, and verify an isolated installation. Normal sync uses the committed pins; it does not follow a moving branch or silently upgrade them. Keep dependency installation and service authentication separate from the pin update.

### Ownership, Conflicts, and Recovery

The importer records source identity and content hashes in `.ai-toolkit-external-skills.json` beside the imported skill directories. It updates only imports whose current files still match their recorded hashes. Unmanaged skill directories, local edits, unsafe destinations, and collisions stop the affected import with a nonzero result. Toolkit `--force` does not override this protection.

When a conflict is reported, keep the existing directory and inspect its origin. Back up any customization outside the managed skill root before intentionally removing or relocating that exact conflicting directory. Then rerun the importer. Do not delete an agent's whole skill directory or remove unrelated plugins to make an import pass.

For rollback, restore the previous manifest pin and rerun after confirming that the installed import remains unchanged. Preserve any local edits separately first. Removing an entry stops future sync for that skill; it does not uninstall existing files. To uninstall, verify and remove only that skill's exact directory and its receipt entry, preserving other entries. Do not edit receipt hashes to force an update of modified files.

If a filesystem failure also prevents rollback, the importer reports a retained recovery directory. Preserve that directory and the existing receipt, inspect the saved `previous` skill tree, and restore the exact affected skill before retrying. Do not delete recovery data to clear an error.

The installer reports installed, updated, unchanged, skipped, and failed entries. Normal toolkit sync preflights external imports before writing repository-generated output; fix a reported external conflict or explicitly choose `--skip-external` before retrying. A successful file import does not prove companion CLI availability, credentials, MCP access, or agent discovery. Check each required capability separately in a fresh session.

## Native Installers and Plugins

These packages use vendor installation flows. They are not arbitrary commands embedded in the import manifest. Check the linked official documentation before running an installer, as package and plugin interfaces can change.

The social-media toolkit is a separate repository with its own canonical skills, build, validation, and sync commands. Use that repository's instructions; this importer does not copy its generated adapters or run its workflow automatically.

### Ponytail

Link:

- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)

Recommended for:

- YAGNI and standard-library-first implementation guidance
- diff and repository reviews focused on unnecessary complexity

Install the native Codex plugin from its official marketplace:

```powershell
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

Verify:

```powershell
codex plugin list
node --version
```

Notes:

- The plugin uses small Node.js lifecycle hooks, so `node` must be on `PATH`.
- Restart Codex after installation. Open `/hooks`, inspect the Ponytail hooks,
  and trust them only after review.
- Codex exposes the bundled commands as skills, such as `@ponytail`,
  `@ponytail-review`, and `@ponytail-audit`.
- The default mode is `full`; use `@ponytail off` when its always-on minimalism
  is not appropriate for a task.
- Uninstall with `codex plugin remove ponytail@ponytail`.

### Interface Design

Link:

- [Dammyjay93/interface-design](https://github.com/Dammyjay93/interface-design)

Recommended for:

- Claude Code design-oriented UI work.

Official recommended install:

```text
/plugin marketplace add Dammyjay93/interface-design
/plugin menu
```

Manual install from the repository README:

```powershell
git clone https://github.com/Dammyjay93/interface-design.git
cd interface-design
cp -r .claude/* ~/.claude/
cp -r .claude-plugin/* ~/.claude-plugin/
```

Notes:

- Restart Claude Code after installation.
- The repo is plugin-oriented; do not treat it as a Codex skill unless you intentionally adapt it.

### Graphify

Install the [Graphify CLI](EXTERNAL-TOOLS.md#graphify), then install its Codex skill globally:

```text
graphify install --platform codex
```

Verify the skill file on Windows PowerShell:

```powershell
Test-Path "$HOME/.codex/skills/graphify/SKILL.md"
```

macOS / zsh:

```sh
test -f "$HOME/.codex/skills/graphify/SKILL.md"
```

Codex parallel extraction expects this existing feature setting:

```toml
[features]
multi_agent = true
```

Use `$graphify` to invoke the skill explicitly. The global install does not modify a repository. By contrast, `graphify codex install` writes an always-on `AGENTS.md` section and registers `.codex/hooks.json`; do not run that project command automatically in Luchdom repositories, whose primary Codebase Memory policy is repository-owned. Keep extraction local with the CLI guidance in [External Tools](EXTERNAL-TOOLS.md#graphify).

### UI/UX Pro Max

Install the [UI/UX Pro Max CLI](EXTERNAL-TOOLS.md#uiux-pro-max-cli), then generate its global Codex skill bundle:

```text
uipro init --ai codex --global
```

The Codex bundle installs under `~/.agents/skills/`, including the `ui-ux-pro-max` orchestrator, sibling design skills, local datasets, and Python search tools. Verify on Windows PowerShell:

```powershell
Test-Path "$HOME/.agents/skills/ui-ux-pro-max/SKILL.md"
```

macOS / zsh:

```sh
test -f "$HOME/.agents/skills/ui-ux-pro-max/SKILL.md"
```

Restart Codex after installation. Update the CLI and regenerate deliberately:

```text
uipro update
uipro init --ai codex --global --force
```

### Taste Skill

[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) previously provided the Codex-oriented `gpt-taste` directory at `skills/gpt-tasteskill`. The manifest deliberately pins [commit f6831c5](https://github.com/Leonxlnx/taste-skill/tree/f6831c5df8ad546c2567535442f1691a823868e3/skills/gpt-tasteskill) to preserve that existing skill identity: newer upstream revisions removed this directory and consolidated the guidance as `taste-skill`. An update to the new identity needs an explicit manifest and installation migration. No Claude-only conversion is needed for the pinned variant.

The upstream catalog has also provided image-generation, redesign, minimalist, and brutalist variants. Inspect the selected revision and choose only the needed variants so overlapping trigger descriptions do not compete. See [the upstream repository](https://github.com/Leonxlnx/taste-skill) for native installation alternatives.

### Napkin

[blader/napkin](https://github.com/blader/napkin) provides per-repository persistent working guidance for Claude Code and Codex. Select its pinned root directory through the manifest.

The skill activates every session and maintains a repository Markdown runbook. Read its actual instructions after installing; importing files does not grant permission to edit unrelated project files.

### MemPalace

Install the [MemPalace CLI](EXTERNAL-TOOLS.md#mempalace), then install its native Codex plugin:

```text
codex plugin marketplace add MemPalace/mempalace
codex plugin add mempalace@mempalace
codex plugin list
```

The [official plugin](https://github.com/MemPalace/mempalace) includes skills, an MCP server, and automatic-save hooks. Restart Codex and review the hooks before trusting transcript saves. Follow [MCP Servers](MCP-SERVERS.md#mempalace) for server verification and [External Tools](EXTERNAL-TOOLS.md#mempalace) for approved-source initialization and mining. The CLI and plugin can publish at different versions.

### Firecrawl

The [Firecrawl CLI documentation](https://docs.firecrawl.dev/sdks/cli) provides this one-shot skill installation and browser authentication flow:

```text
npx -y firecrawl-cli@latest init --all --browser
```

`--all` installs the skill for detected coding agents; `--browser` opens the authentication flow. Use it when both actions are intended. For CLI-only installation or login, use [External Tools](EXTERNAL-TOOLS.md#firecrawl-cli).

Observed Windows installation placed shared skills under `~/.agents/skills/` and wired supported tools such as Codex and Claude Code to them. They may not appear directly under `~/.codex/skills` or `~/.claude/skills`. Verify the new agent session and authenticate separately if the installer did not complete login.

### Playwright CLI

Install [Playwright CLI](EXTERNAL-TOOLS.md#playwright-cli), then its companion skills:

```text
playwright-cli install --skills
```

Restart the agent afterward. The [upstream README](https://github.com/microsoft/playwright-cli) recommends CLI plus skills for coding-agent workflows. Use [Playwright MCP](MCP-SERVERS.md#playwright) when a persistent introspection session is needed.

### PostHog

Prefer local skills plus [PostHog CLI](EXTERNAL-TOOLS.md#posthog-cli) for coding-agent workflows. The optional [PostHog AI plugin](https://github.com/PostHog/ai-plugin) includes task skills and a bridge to the hosted skills store:

```text
codex plugin marketplace add PostHog/ai-plugin
codex
```

In the new Codex session, run `/plugins`, select PostHog, and install it. Follow [MCP Servers](MCP-SERVERS.md#posthog) only when remote product tools or the hosted skills store are needed.

### Stripe

The [Stripe AI skill repository](https://github.com/stripe/ai/tree/main/skills) includes `stripe-best-practices`, `stripe-directory`, `stripe-projects`, and `upgrade-stripe`. Selected direct imports use pinned upstream directories from the manifest. Review upstream changes before updating those pins.

[Stripe's AI documentation](https://docs.stripe.com/building-with-ai) also provides project-local hosted skills and native plugins. Use one installation route for a given skill; avoid creating competing copies.

Project-local hosted skills:

```text
npx skills add https://docs.stripe.com
```

Codex plugin:

```text
codex plugin add stripe@openai-curated
```

Claude Code plugin:

```text
claude plugin install stripe@claude-plugins-official
```

Run project-local installs from the project that needs Stripe guidance. Native or hosted installs have their own update process. Importing files does not create the [Stripe sandbox](EXTERNAL-TOOLS.md#stripe-cli-sandbox), provision services, or provide credentials.

### OpenAI Curated Linear Skill

The [OpenAI Linear skill](https://github.com/openai/skills/blob/main/skills/.curated/linear/SKILL.md) is a Codex skill. Its manifest target is `~/.codex/skills/linear`; importing it does not configure or authenticate the [Linear MCP server](MCP-SERVERS.md#linear).

## Reference Catalogs

Use these for discovery, then explicitly select and pin a reviewed directory before importing:

- [Anthropic skills](https://github.com/anthropics/skills/tree/main/skills)
- [OpenAI skills](https://github.com/openai/skills)

Codex's built-in `$skill-installer` is an alternative for individual curated or experimental skills. Follow its current documentation rather than copying plugin caches or old machine snapshots. The [historical Codex restore inventory](docs/codex-skill-restore.md) remains a reference for additional system and plugin skills; it is not the active import list.
