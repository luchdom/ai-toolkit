# Project documentation

Use a maintained product brief, design system, architecture guide, and root agent instructions to give people and coding agents the same project context. This toolkit follows the four-file structure from *The 4 Files That Make AI Build Your App Properly* and adds practical sections only when the repository needs them.

## Create or refine docs

In the selected repository, invoke:

```text
$project-docs
```

The skill discovers existing documentation and implementation evidence, then drafts or refines the applicable foundations in this order:

1. Product requirements: users, problem, goal, version scope, exclusions, success, and acceptance criteria.
2. Design system for a UI: visual rules, existing tokens/components, responsive behavior, states, and accessibility.
3. Architecture: system, stack, folders, data flow, boundaries, security, and operations.
4. Root `AGENTS.md`: actual documentation links, task-based reading, verified commands, and concise project rules.

Material decisions are refined with the owner. Implemented facts, approved direction, proposals, and open questions remain distinct. Unsupported goals, palettes, technologies, and commands are not silently filled in from template examples. An incomplete draft identifies the remaining decisions.

The templates include populated examples: semantic colours with hex values, type sizes/weights/line heights, spacing/radius scales, component states, breakpoints, user journeys, acceptance criteria, architecture tables, a directory tree, and a traced data flow. Each section states minimum coverage. Agents replace the fictional Taskboard examples with inspected project values; suitable sample values can be a clearly labeled starting proposal for a new project.

For an existing repository, narrow the request:

```text
$project-docs refine the existing design system using the source tokens and components
$project-docs create only the missing product brief and update its navigation links
$project-docs resolve the architecture questions from our earlier decisions
```

These requests authorize documentation work. They do not authorize redesigning the application or changing its stack. Continue refining the same documents as decisions arrive.

## Working design system

Before building frontend pages, establish a written design system and a runnable component catalogue. Use `$project-docs` if either is missing. Reuse an existing workshop or choose a suitable app route or served HTML page. Demonstrate the required shared components in the catalogue first, then compose pages from those same implementations and tokens.

Show the components the project uses, such as data tables, form labels, buttons, badges, text fields, selects, cards, tabs, and dialogs. Demonstrate relevant variants and states, typography, tokens, and responsive behavior. Exercise interactive controls with pointer and keyboard input. Fixtures can use synthetic data and local state.

The design-system document records the actual source path, local URL, startup command, access boundary, and observed browser checks. Build or refine the catalogue within authorized UI implementation. During docs-only work, record the proposal and remaining implementation. See [the working design-system guide](../src/skills/project-docs/references/working-design-system.md).

## Placement

New projects default to:

```text
project/
├── AGENTS.md
└── docs/
    ├── PRD.md
    ├── DESIGN_SYSTEM.md
    └── ARCHITECTURE.md
```

Existing equivalents keep their locations and become the paths linked from `AGENTS.md` and human-facing navigation. Monorepos can link shared foundations and scoped overrides. A service/library/CLI without a UI can mark design-system coverage not applicable. Root `AGENTS.md` is the shared project entry point; project sync for Codex or Claude Code writes it once and preserves existing custom tool files.

## How agents reach the docs

The route is explicit:

```text
Global/project tool guidance
  -> Root AGENTS.md with a map of actual project links
     -> PRD, design system, architecture (or existing equivalents)
     -> Working catalogue source + URL/startup/access instructions, when present
```

The creation skill maintains that map and existing project-specific router pointers while editing docs. For example, a scoped instruction file can link the root `AGENTS.md`. The root map links `docs/PRD.md` or the repository's equivalent. Scoped instructions use paths relative to their own locations. The review follows these links and reports a missing route even if the documents themselves exist. The global default filenames help discovery; they do not replace project-specific links.

Read [the canonical standard](../src/skills/project-docs/references/documentation-standard.md) for ownership, evidence states, and conditional extensions such as code style, testing, security, operations, ADRs, and a glossary. Templates live under [the skill's assets](../src/skills/project-docs/assets/). Use the [shared artifact contract](../src/tool-instructions/shared/artifact-contract.md) for feature-specific plans and QA evidence.

## Review and ordinary project work

To assess without editing:

```text
$project-docs-review
$project-docs-review check the architecture claims against the service boundaries
```

The review maps each applicable concern to its actual owner, checks relevant source evidence, and reports specific missing coverage, broken links, duplicate ownership, or drift. It states what was sampled and what remains unverified. It recommends the smallest useful creation or refinement request.

The shared instruction rule asks agents to locate relevant foundation docs before substantive planning or implementation. A missing document prompts a targeted suggestion once per project context; earlier declines are respected. Nonblocking gaps do not stop an ordinary task. `$docs-as-code` maintains affected foundations after authorized changes, with `$luchdom-docs` supplying Luchdom-specific owners.

## Install and verify

Follow [platform support](platform-support.md) and use the verified Python 3.11+ executable. Build and validate from the toolkit checkout:

```sh
python3 scripts/build.py
python3 scripts/validate.py
```

Sync to the selected tool, comparing/backing up intentional local customizations first:

```sh
python3 scripts/sync.py --tool codex
```

On Windows use `py -3` or the verified executable. Use `--tool claude` for Claude Code or `--tool all` for both tools. Normal sync includes selected external imports; `--skip-external` limits it to repository-generated content. Add `--project "<actual-repository-path>"` when project-local routing is wanted.

User-level sync adds an `AI-TOOLKIT-PROJECT-DOCS` block to the tool's existing user-instruction location and installs both skills with their resources. The block routes requests for a plan to the default `plan` stage in the [shared delivery workflow](../src/tool-instructions/shared/delivery-workflow.md). Sync preserves content outside the block. The project setup uses root `AGENTS.md`; the existing Claude user-level instruction destination is independent of that project layout. Existing unmarked project instructions remain protected by the normal sync rules.

Verify the two installed `SKILL.md` files, the creation skill's four assets and two references, and the docs rule in the selected user/project instructions. Start a new agent session to discover newly installed skills/instructions. Build and validation alone do not install into live user homes.

To undo an installation, restore the backed-up skills/rules and remove only the `AI-TOOLKIT-PROJECT-DOCS` block if it is no longer wanted. A later toolkit sync reinstalls it from canonical source.
