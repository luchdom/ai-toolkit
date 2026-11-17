# Working Design System

For a project with a UI, pair the written design rules with a runnable catalogue when practical. The catalogue demonstrates the project's real typography, tokens, components, states, and interactions. Reuse an existing workshop, component library, or internal examples page first.

## Choose the natural home

| Project shape | Preferred approach | Example home to adapt |
|---|---|---|
| Framework app, including a Next.js/React app | An internal/development route importing the existing shared components and themes | `/design-system` under the repository's actual routing convention |
| Vanilla HTML/CSS/JavaScript | A page served by the existing dev server, importing the real shared styles and behavior | `docs/design-system/index.html` or the established examples directory |
| Reusable component package | Its existing component workshop or runnable examples app | Existing stories/examples alongside the component source |
| Monorepo | A shared catalogue with package-specific examples and links | Existing UI package/workshop, without copying its tokens into every app |

These locations are examples, not mandatory paths. Keep the repository's stack and build conventions; a new workshop dependency is unnecessary when a small existing route/page can demonstrate the components.

## Minimum runnable coverage

| Area | Demonstrate | Observable check |
|---|---|---|
| Foundations | Shared colour/token swatches, headings/body/captions, spacing/radius examples, actual icons | Values and rendered styles match the authoritative token/theme sources |
| Actions | Actual primary and secondary actions, disabled/loading variants | Pointer and keyboard activation produce visible local feedback; repeated submission behaves as specified |
| Forms | Actual text input, helper/error feedback, and selection controls used by the product | Typing, validation, correction, focus, and selection work with accessible labels/state |
| Product components | Existing cards, badges, navigation, or other components relevant to the UI | Variants and interaction states use the same implementation as the app |
| Layout and themes | Small and large viewports, long labels/content, supported themes | Content remains usable, controls reachable, and focus visible |

Use synthetic fixtures and local state for demos. For example, an Add task form can reject an empty title, add a local preview item, and toggle its completion. It demonstrates behavior without contacting a live API. Static screenshots, decorative button shapes, or copied CSS that diverges from production do not establish a working catalogue.

## Scope and access

When UI implementation is authorized, implement/reuse the catalogue within that scope and apply the active workflow's UI design and rendered verification requirements. A documentation-only request establishes a concrete proposal: chosen home, reused sources, demonstrations, startup/access plan, and remaining work. It does not by itself authorize application code changes, a new dependency, or publication. Reuse any existing authorization instead of asking again.

Use the existing development, authentication, or access boundary. An internal-looking route name alone does not restrict access. Record how the route/page is kept within its intended audience; preserve production behavior unless changing it is part of the task.

## Connect the documentation

Record these fields in the design-system document and link them from the root agent docs map:

| Field | Concrete example, to replace with verified project values |
|---|---|
| Source | `src/app/design-system/page.tsx`, or `docs/design-system/index.html` for a vanilla site |
| Local address | `/design-system` on the running dev server, or the server's actual HTML-page URL |
| Startup | The exact repository-owned command and working directory |
| Shared sources | Actual token/theme and reusable component paths |
| Access | Existing dev-only availability or authentication rule; what was inspected |
| Verification | Browser/viewport used, interactions exercised, results, and unverified cases |

Also record the catalogue's place in architecture when it introduces a route/package. Existing project-specific tool routers should point to root `AGENTS.md` using a valid relative path; the root map points to the actual written docs and catalogue source/access instructions. Link from the README or existing human docs index too.

## Keep it working

When shared tokens, components, or their behavior change, update the written rules and catalogue as applicable to the authorized work. Use one token/component source. Report any catalogue change that belongs to a later implementation stage instead of claiming it was completed during a docs-only stage.

Before calling the catalogue implemented, run the actual startup/build checks and inspect it in a real browser. Exercise relevant pointer/keyboard controls, validation, loading/disabled states, responsive layouts, and supported themes. Record actual results and limits; a successful build or a rendered screenshot alone does not prove interactions work.
