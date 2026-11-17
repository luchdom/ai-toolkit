# Architecture

- **Status:** [Draft or ready for use; separate implemented structure and proposals]
- **Scope:** [Application, package, service, or monorepo boundary]
- **Owner:** [Known accountable role, or decision needed]
- **Evidence:** [Entry points, manifests, configuration, tests, and approved decisions]

> The following is a proposed architecture for the fictional Taskboard example. Paths and technologies illustrate the required detail; replace them with inspected repository facts or clearly identified proposals. Use each **Minimum** note as an authoring checklist and remove it once covered.

## 01 System Overview

```text
User -> Task page -> Reusable UI components -> Task state/store -> Browser storage
                         ^
                         |
                 Internal design-system page
                 (same components and tokens)
```

**Example boundary:** version one is a single-browser app. There is no server account or external data provider in this proposal; future sync would require a separate decision.

**Minimum:** name the actual entry points, major components, external systems, and boundaries. Distinguish planned components from implemented ones.

## 02 Tech Stack

| Area | Technology and responsibility | Evidence |
|---|---|---|
| UI / routing | Example proposal: Next.js, React, TypeScript | Verify the actual manifest, routing convention, and material versions |
| Styling | Shared CSS custom properties and reusable component styles | Example source: `src/styles/tokens.css` |
| Persistence | Example proposal: browser `localStorage` behind a task-store module | Example source: `src/lib/task-store.ts`; owner must accept local-only data |
| UI examples | Internal route importing the same UI components | Example source: `src/app/design-system/page.tsx` |
| Testing | Repository-owned unit and browser checks | Replace with actual test configuration and commands |

**Minimum:** give one row per actual technical concern with its responsibility and source evidence. Check versions from manifests/lockfiles when material. Reuse the existing stack rather than adopting this sample.

## 03 Project Structure

```text
src/
├── app/
│   ├── page.tsx                 # Task page in this example
│   └── design-system/page.tsx   # Internal working component catalogue
├── components/                 # Actual shared Button, TextField, Badge, Card
├── lib/task-store.ts           # Task persistence boundary
└── styles/tokens.css           # Shared design values
tests/                          # Store/interaction coverage
docs/                           # Curated project documentation
AGENTS.md                       # Links to actual docs and project commands
```

**Minimum:** map actual directories and representative files, identify owners/boundaries, and say where new work belongs. A library, service, monorepo, or vanilla site should use its own layout instead of this framework example.

## 04 Data Flow

**Example: add a task.**

1. The user enters a title in the shared text field and submits the form.
2. The task action validates a nonempty trimmed title; invalid input returns a field error.
3. The task-store boundary creates the task and persists the next task list.
4. The page displays the updated list and an accessible result message.
5. A persistence failure is reported distinctly; the UI does not claim that unsaved data was stored.

**Minimum:** trace at least one representative path end to end, naming actual entry points, state/data owners, validation, persistence/external calls, and failure handling. Link source paths beside significant claims.

## 05 Scalability

**Example limits:** local browser storage provides no cross-device access and may be cleared by the browser. The safe task count and supported storage behavior are unmeasured. A remote store is a future option only if product scope requires it.

**Minimum:** document known constraints and measured limits separately from assumptions. Avoid introducing services to solve an unconfirmed scale requirement.

## 06 Boundaries, Data, and Security

| Boundary | Example responsibility / rule | Evidence or open decision |
|---|---|---|
| Task store | Owns persistence and reports write failures | Inspect the actual store implementation |
| Browser data | Local to the browser; not a suitable home for secrets | Confirm privacy and retention expectations |
| Identity / tenancy | Not part of this proposed version | Revisit before introducing accounts or shared data |
| Internal catalogue | Synthetic examples, shared components, existing development/access boundary | Verify it is exposed only as intended |

**Minimum:** explain applicable contracts, authentication/authorization/tenancy, trust boundaries, sensitive-data lifecycle, and secret handling. Mark a concern not applicable with its reason; link dedicated security/data guides when present.

## 07 Reliability and Operations

| Concern | Example documentation | Verification needed |
|---|---|---|
| Local startup | Run the repository's dev script; open the task page and catalogue | Record the exact command, URL, and observed result |
| Configuration | Name required variables and their purpose; use synthetic values | Check the actual environment template; include no secrets |
| Data recovery | Explain browser-local storage loss and any export/backup feature | Owner decision; do not claim recovery exists |
| Delivery / rollback | Link the repository's build/deploy/release instructions | Distinguish locally run checks from provider-only validation |

**Minimum:** document relevant startup/configuration, failure handling, delivery, and recovery/rollback behavior. Identify unverified external operations rather than implying they were tested.

## 08 Decisions and Extension Points

**Example decision:** a task-store boundary keeps the page independent of persistence details. The current proposal uses local storage; changing that boundary requires revisiting privacy, offline behavior, and product scope. Link an ADR if the tradeoff warrants one.

**Minimum:** link material decisions and consequences, describe approved extension points, and keep per-feature work evidence in its registered workflow folder.

## 09 Open Decisions

| Question | Technical impact | Owner or next evidence |
|---|---|---|
| Is browser-local data sufficient for version one? | Persistence, recovery, future identity | Product owner; confirm against the PRD |
| Which existing route/workshop should host the working design system? | UI examples and access boundary | Inspect the project's routes/workshop; use the existing convention |

**Minimum:** name unresolved decisions and their impact, or state "None" when resolved.
