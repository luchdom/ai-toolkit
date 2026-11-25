# AI Toolkit repo instructions

This repo owns shared agents, skills, and tool instructions. Edit `src/` and regenerate `dist/` with `scripts/build.py`.

## Docs map

- [Delivery workflow](src/tool-instructions/shared/delivery-workflow.md) defines routes, stages, and authority. Follow its links for artifacts, publication, and worktrees.
- [Project documentation](docs/project-documentation.md) owns docs placement and tool routing. Read its linked standard when changing those rules or templates.
- [Twelve-Factor for agentic development](docs/twelve-factor-for-agentic-development.md) guides engineering refinements, architecture docs, and pull request reviews.
- [Platform support](docs/platform-support.md) owns setup and recovery. [README](README.md) lists the install and validation commands.
- [External skill guide](EXTERNAL-SKILLS.md) and [external-skills.toml](external-skills.toml) own imports. Use [External Tools](EXTERNAL-TOOLS.md) for CLIs and [MCP Servers](MCP-SERVERS.md) for server setup.

## Work in this repo

- Before setup or runtime commands, run `python3 scripts/platform_info.py` on macOS or `py -3 scripts/platform_info.py` on Windows. Use the verified Python 3.11 or newer.
- Run `python3 scripts/validate.py` with the verified interpreter. For changed Markdown, use `npm run lint:md:files -- ":path/to/changed.md"` from the repo root. Follow the [Markdown lint guide](docs/markdown-linting.md).
- Apply the [plain-English rule](src/tool-instructions/shared/reply-style.md) when writing shared guidance.
- When the user asks to install for both tools or gives no tool, build and run `scripts/sync.py --tool all`. Add `--project <path>` only when project instructions are requested. Back up local tool customizations and verify the installed files.
- Project sync migrates legacy toolkit markers and preserves surrounding text. `--force` overwrites the entire project `AGENTS.md`.
