# Markdown linting

Agents must lint `.md` and `.markdown` files they create or edit before reporting completion. Project commands and configuration take precedence. This toolkit uses [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2), pinned in `package-lock.json`, with shared defaults in [markdownlint.json](../src/tool-instructions/shared/markdownlint.json).

## Install

Use Node.js 22 or newer and npm. These commands work in macOS zsh and Windows PowerShell:

```sh
npm ci
npm install --global markdownlint-cli2@0.24.0
markdownlint-cli2 --help
```

The local dependency provides reproducible repository checks. The global command supports agents working in projects without their own Markdown tooling. Use Python 3.11 or newer, then build and sync as usual:

```sh
python3 scripts/build.py
python3 scripts/sync.py --tool all
```

On Windows, use the verified `py -3` interpreter instead of `python3`. Sync installs the fallback configuration at `~/.config/ai-toolkit/markdownlint-cli2.jsonc` on either platform and maintains a dedicated Markdown guidance block in `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`, and `~/.copilot/copilot-instructions.md` for the selected tools. It preserves content outside that block, even in existing unmarked user instruction files. Malformed or duplicate Markdown markers stop that update. The existing rules for project instruction markers are unchanged.

The generated specialist agents also include the shared rule. Cursor receives the rule through its generated project instructions and specialist rules; it has no user-level sync in this toolkit. Start a new agent session after syncing to load updated instructions. Sync does not install npm packages or change editor settings.

## Check changed files

Run from the repository root. Use one quoted argument per file; `:` makes the path literal, including brackets and other glob characters:

```sh
npm run lint:md:files -- ":README.md" ":docs/markdown-linting.md"
npm run lint:md:fix -- ":docs/markdown-linting.md"
npm run lint:md:files -- ":docs/markdown-linting.md"
```

Review the diff after `--fix`. It cannot repair every violation. Preserve prose, front matter, examples, and unrelated edits; do not disable a rule merely to make a check pass. Check the reported file count as well as the exit status: zero matching files is not verification.

For a project with its own configuration, use its command or run `markdownlint-cli2 --no-globs ":path/to/changed.md"` from its root. If it has no configuration, use the installed fallback explicitly:

```sh
markdownlint-cli2 --no-globs --config "$HOME/.config/ai-toolkit/markdownlint-cli2.jsonc" ":path/to/changed.md"
```

This one-line command also works in PowerShell. Configuration lookup starts at the working directory; a home configuration is not automatically discovered from every project. If the CLI is unavailable, install it when authorized or report the limitation. Do not silently download tools during a check.

## Rules and scope

The default rules check heading/list/fence spacing, whitespace, link syntax, and other Markdown structure. The shared configuration allows long lines (`MD013`), repeated heading names in separate sections (`MD024` with `siblings_only`), multiple top-level headings in composite instructions (`MD025`), inline HTML (`MD033`), fragments without an initial heading (`MD041`), and unaligned table columns (`MD060`). YAML front matter is supported by the linter. These choices accommodate agent instructions and prose without reflowing their content.

`npm run lint:md` audits the repository's Markdown. Its configuration excludes dependencies, generated adapters, Git metadata, and workflow evidence. An all-file audit can expose pre-existing violations; routine editing should use the explicit-file command and repair the changed files. Lint checks syntax/style, not factual accuracy or whether local links resolve.

The Python validation gate remains dependency-free. Run Markdown lint alongside it for Markdown changes. Agent instructions require the check but are not a filesystem write hook; enforcement at commit or CI time requires a separate repository gate.

## Verify and undo

Verify the CLI with `markdownlint-cli2 --help`, lint an actual file, and inspect the installed guidance and fallback configuration. Back up local agent customizations before sync: user-level generated agents and skills are refreshed, while the Markdown block update preserves surrounding user instructions.

To undo the user-level setup, restore the backed-up instruction files or remove only their `AI-TOOLKIT-MARKDOWN` blocks, remove the installed fallback configuration if unused, and run `npm uninstall --global markdownlint-cli2`. A later normal toolkit sync reinstalls the guidance; change its canonical source if the policy should change permanently.
