# ai-toolkit

Reusable AI agents, skills, and project instructions for Codex and Claude Code.

## Delivery workflows

Choose one of the three [delivery entries](src/tool-instructions/shared/delivery-workflow.md).

- [Spec-driven Delivery](src/skills/spec-driven-delivery/SKILL.md) defines the process. Use `$spec-driven-delivery <stage> <goal-or-selector>` to run one stage.
- [Goal to Delivery](src/skills/goal-to-delivery/SKILL.md) runs the applicable stages automatically for one goal. Use `$goal-to-delivery <goal-or-selected-issue>` to stop at tested working-tree changes by default.
- [Linear Delivery Loop](src/skills/linear-delivery-loop/SKILL.md) selects or resumes one eligible Linear issue and runs Goal to Delivery for it. Invoke `$linear-delivery-loop` from a scheduled task or an attended pilot.

Plan the work, clarify decisions, break it into tasks, audit when required, and implement. Run applicable QA before code review, then publish to the authorized boundary. For the full sequence and when each stage applies, see the [delivery stages](src/skills/spec-driven-delivery/references/delivery-stages.md).

Use the shared [artifact contract](src/tool-instructions/shared/artifact-contract.md) for plans and evidence and the [worktree policy](src/tool-instructions/shared/worktrees.md) for linked Git worktrees.

## Project documentation

Use [`$project-docs`](src/skills/project-docs/SKILL.md) to create or refine a repository's product brief, design system, architecture, and root `AGENTS.md`. It includes templates, checks the actual repository, and works through open decisions with you. Use [`$project-docs-review`](src/skills/project-docs-review/SKILL.md) for coverage, placement, and consistency findings without edits. Existing equivalent documents are reused; projects without a UI can mark the design system not applicable.

Templates provide populated examples and minimum coverage requirements. For UI projects, the skill also defines a working component catalogue using the real tokens/components, with its source and startup/access instructions linked from the project docs map. Implement the catalogue within authorized UI work, or record a concrete proposal during docs-only work.

Sync adds a shared docs-discovery rule to user instructions and generated project/specialist instructions. Agents suggest the specific missing documentation when relevant, honor earlier declines, and keep applicable docs current within the active task. Codex and Claude Code share `AGENTS.md`. See [Project documentation](docs/project-documentation.md) for examples, placement, and installation.

## Product and engineering specialists

| Agent | Use it for |
|---|---|
| [`product-manager`](src/agents/product-manager.md) | Product and acceptance-criteria clarifications, evaluating implementation against customer outcomes and AC, benchmark work with PD, and PRDs on request. |
| [`staff-engineer`](src/agents/staff-engineer.md) | Technical clarification for the team, feasibility with PM/PD, code review, simplification and duplication analysis, and requested RFCs, ADRs, diagrams, and implementation guidance. Writes documents; implementers write code. |

Goal to Delivery can consult the product manager for goals and product behavior, the product designer for UI and user experience, and the staff engineer for technical choices. A staff engineer can also perform the independent code review when they meet the review requirements. See the [clarification policy](src/skills/spec-driven-delivery/references/clarification-policy.md) and [quality gates](src/skills/spec-driven-delivery/references/quality-gates.md).

Examples: ask PM to evaluate a named implementation against its approved AC or draft a PRD; ask Staff Engineer to compare simpler implementation options, review a named diff, or document an architectural decision. Both use the repository's canonical agent metadata; regenerate and sync after changing their configuration.

## MVP autonomous loop

The MVP deliberately uses existing systems instead of a separate orchestration service:

- Linear stores queue state, checkpoints, decisions, and completion.
- `.ai/loop.json` stores the repository-specific team, labels, states, Git policy, and budgets.
- A deterministic user-local lease prevents overlapping invocations from working the same Linear queue.
- A Codex scheduled task invokes `$linear-delivery-loop` every 15 minutes from one dedicated chat/project context.
- Git branches and pull requests store implementation history and review.
- Linear comments are the authoritative human-decision channel; listed choices and explicit custom suggestions are supported, while ntfy is optional best-effort attention that links directly to the issue.

The loop resumes eligible active work before selecting a labeled backlog issue. An active attended issue pauses intake. The loop moves an issue to Done after it verifies the boundary reported by Goal to Delivery. See the [loop guide](docs/mvp-linear-delivery-loop.md) for checkpoints, continuations, and quiet runs.

Linear labels have separate responsibilities:

- `autonomous` grants the scheduled loop permission to select a refined backlog issue.
- `needs-decision` marks backlog work that needs one owner choice before it can be refined or made autonomous. It is a lightweight curation label, not another delivery workflow.
- `needs-human` pauses an issue that is already active in the autonomous loop.

Unlabeled backlog issues may be reviewed and refined collaboratively without starting a full delivery workflow. Record any material owner decision in Linear, remove `needs-decision` when resolved, and add `autonomous` only after the goal and acceptance criteria are bounded and locally testable.

See [MVP Linear delivery loop](docs/mvp-linear-delivery-loop.md) for setup and operation.

## Harness coverage

A useful engineering harness needs seven capabilities. The MVP covers all seven without turning each one into a service:

| Component | MVP coverage |
|---|---|
| System prompt | Repository instructions plus the three explicit entry skills define behavior and authority. |
| Tools | Codex local tools, Linear, Git/GitHub, and optional browser/HTTP checks provide only the needed capabilities. |
| Context management | Skills load progressively; `.ai/loop.json`, the selected issue, repository instructions, and relevant code form the working set. |
| Verification | Focused tests, applicable UI design conformance and runtime QA, independent code review, and the repository's local validation command check the work. |
| Memory | Linear comments/issues, Git/PR history, curated docs, and optional concise notes in the exact registered `artifactFolder` persist useful knowledge. |
| Sandboxes | Codex repository/worktree isolation and repository-owned disposable test data constrain execution. |
| Human hooks | `needs-decision` marks pre-work owner choices; `needs-human`, a structured Linear choice or custom suggestion, the Codex task inbox, and an optional issue-linked ntfy notification pause active work safely. |

Memory curation and observability are intentionally modest: persist decisions and useful documentation, and rely on scheduled-task history plus Linear/Git records. Add more machinery only after the MVP exposes a concrete gap.

## Repository layout

- `src/agents/`: canonical specialist agent definitions
- `src/skills/`: canonical reusable skills and references
- `src/tool-instructions/`: shared workflow rules and project-local instructions for each supported tool
- `scripts/build.py`: generate tool adapters into `dist/`
- `scripts/sync.py`: install generated output and selected external skills into user homes and optional projects
- `external-skills.toml`: selected upstream skill directories, pinned revisions, and compatible tools
- `scripts/external_skills.py`: preview or install external skill imports independently
- `scripts/validate.py`: local repository validation
- `scripts/platform_info.py`: read-only execution-host and tool availability probe
- `dist/tool-instructions/`: generated project-local projections for each supported tool
- `dist/`: generated projections; never edit directly

Save delivery notes in `.ai/work` and use the exact registered `artifactFolder` when a workflow has one. See the [artifact contract](src/tool-instructions/shared/artifact-contract.md) for registration and legacy folders.

## Build, validate, and install

Start with [platform support](docs/platform-support.md): detect the execution host and shell, then choose a Python **3.11+** executable. Use the same verified interpreter throughout. The probe also runs on older Python 3.9+ so it can report an upgrade requirement.

Windows / PowerShell:

```powershell
py -3 scripts/platform_info.py
py -3 scripts/build.py
py -3 scripts/validate.py
py -3 scripts/sync.py --tool all
```

macOS / zsh:

```sh
python3 scripts/platform_info.py
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/sync.py --tool all
```

Install project-local tool instructions too (use the actual target path):

```powershell
py -3 scripts/sync.py --tool all --project "C:/path/to/repo"
```

```sh
python3 scripts/sync.py --tool all --project "$HOME/path/to/repo"
```

Use `--tool codex` or `--tool claude` to install for one tool. Use `--tool all` for both. `LUCHDOM_AI_TOOLKIT_DOCS` can override the shared curated-docs path rendered into tool instructions; the legacy `LUCHDOM_AI_CONFIG_DOCS` name remains supported.

User sync installs the shared delivery references next to the skills in each tool's home. Project instructions link to the toolkit checkout. Sync the project instructions again if that checkout moves.

Normal sync includes the compatible external imports selected in [external-skills.toml](external-skills.toml). Preview them with `python3 scripts/external_skills.py --tool all --dry-run` on macOS or `py -3 scripts/external_skills.py --tool all --dry-run` on Windows. Use `--skip-external` on `scripts/sync.py` for repository-generated content only. Imports preserve unmanaged or locally modified skill directories; `--force` does not bypass their ownership checks. See [External Skills](EXTERNAL-SKILLS.md) for selection, updates, and recovery.

Normal sync updates only marker-managed blocks in existing project instruction files and preserves content outside them. Use `--force` to adopt an unmarked project instruction file. Repository-generated user-level agents and skills are refreshed on every sync; back up intentional local preferences first. See [sync verification and recovery](docs/platform-support.md#sync-verification-and-recovery).

For a fresh Codex environment, start with [External Skills](EXTERNAL-SKILLS.md) for selected imports and native plugins. The [additional skill restore checklist](docs/codex-skill-restore.md) is a historical Windows inventory for system and plugin skills beyond the active manifest; follow current platform paths and package instructions when restoring it.

## Maintenance

Markdown edits must pass the [Markdown linting workflow](docs/markdown-linting.md). Install with `npm ci`, then run `npm run lint:md:files -- ":path/to/changed.md"`; use `npm run lint:md` for an all-file audit. The Python gate remains dependency-free. Toolkit sync installs a dedicated Markdown rule in user-level Codex and Claude Code instructions and includes it in generated specialist agents and project routers. Install the global CLI separately for use outside this repository.

- Change `src/`, regenerate `dist/`, and validate; do not edit generated output.
- Keep tool instructions as concise routers rather than copies of the canonical protocol.
- Keep legacy artifact-root literals limited to the validator's reviewed path-and-purpose allowlist.
- Keep credentials in environment variables, never repository files.
- Use [External Tools](EXTERNAL-TOOLS.md) for companion CLIs, [External Skills](EXTERNAL-SKILLS.md) for imports and plugins, and [MCP Servers](MCP-SERVERS.md) for explicit server setup.
- Preserve unrelated user changes and historical artifact evidence.
