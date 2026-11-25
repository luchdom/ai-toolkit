# ai-toolkit

Reusable agents, skills, and project instructions for Codex and Claude Code.

## Run delivery

Use [Spec-driven Delivery](src/skills/spec-driven-delivery/SKILL.md) for one named stage. Use [Goal to Delivery](src/skills/goal-to-delivery/SKILL.md) to run the applicable stages for one selected goal. The [shared workflow](src/tool-instructions/shared/delivery-workflow.md) routes ordinary requests and defines where to stop.

An external runner can call an agent or pass one verified assignment to Goal to Delivery. The runner owns scheduling and issue state. Existing users can follow the [OpenBot handoff](src/skills/goal-to-delivery/references/openbot-handoff.md) or the [standalone Linear loop guide](docs/mvp-linear-delivery-loop.md).

### Agents

| Agent | Use it for |
| --- | --- |
| [Senior Full-Stack Engineer](src/agents/senior-full-stack-engineer.md) | Plan and implement one assignment, including its UI specification when needed. |
| [Product Manager](src/agents/product-manager.md) | Clarify the user journey and acceptance criteria, then evaluate the result. |
| [Staff Engineer](src/agents/staff-engineer.md) | Assess technical choices and independently audit readiness or review code. |
| [QA Engineer](src/agents/qa.md) | Check running behavior and verify changed screens in a browser. |
| [.NET Engineer](src/agents/dotnet.md) | Implement C#/.NET backend changes with [`$dotnet-implementation`](src/skills/dotnet-implementation/SKILL.md). |

Use [`$refine`](src/skills/refine/SKILL.md) to pressure-test a goal or decision before planning delivery. Use the [Twelve-Factor guide](docs/twelve-factor-for-agentic-development.md) for engineering decisions and review.

## Build, validate, and install

Follow [platform support](docs/platform-support.md) to choose a verified Python 3.11 or newer. The local validation command builds the adapters and runs the tests.

```sh
python3 scripts/platform_info.py
python3 scripts/validate.py
python3 scripts/sync.py --tool all
```

On Windows use `py -3` or the verified interpreter. Use `--tool codex` or `--tool claude` to install for one tool. Add `--project "<project-path>"` to install project guidance in its shared `AGENTS.md`. Back up local agent and skill customizations before syncing.

Normal project sync preserves text outside managed blocks. If markers are malformed, fix the reported file and retry. `--force` replaces the entire project `AGENTS.md`. See [sync recovery](docs/platform-support.md#sync-verification-and-recovery).

Normal sync includes pinned imports from [external-skills.toml](external-skills.toml). Use `--skip-external` to install repository content only. See the [external skill guide](EXTERNAL-SKILLS.md), [companion tools](EXTERNAL-TOOLS.md), and [MCP servers](MCP-SERVERS.md) for setup.

## Maintain the toolkit

- Edit `src/agents/`, `src/skills/`, and `src/tool-instructions/`. Build the generated adapters in `dist/` with `python3 scripts/build.py`.
- Use the [project documentation guide](docs/project-documentation.md) for docs ownership, templates, and reviews.
- Use the [artifact contract](src/tool-instructions/shared/artifact-contract.md) for plans and evidence and the [worktree policy](src/tool-instructions/shared/worktrees.md) for linked Git worktrees.
- Apply the [plain-English rule](src/tool-instructions/shared/reply-style.md) to shared instructions. Run [Markdown lint](docs/markdown-linting.md) on changed files.
