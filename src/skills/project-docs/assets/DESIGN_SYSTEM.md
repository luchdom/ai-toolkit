# Design System

- **Status:** [Draft or ready for use; separate implemented rules and proposals]
- **Scope:** [UI surfaces and supported platforms]
- **Owner:** [Known accountable role, or decision needed]
- **Evidence:** [Approved visual references, components, token/config paths, inspected screens]

> Template examples describe a fictional web UI. They show the expected level of detail, not an approved palette, stack, or library. Replace them with the project's values; for a new project, retain suitable values only as an explicit proposal. Use each **Minimum** note as an authoring checklist and remove it once the document supplies that coverage.

## 01 Brand Identity

**Minimum:** name the audience and describe the visual direction in concrete terms, with an approved reference or proposal status.

**Example proposal:** calm, clear, practical, and welcoming. A personal task board uses readable lists, restrained colour, and one obvious primary action per screen. Decoration must not compete with task titles or status.

## 02 Colour Palette

| Role | Token or exact value | Usage and source |
|---|---|---|
| Primary text | `--color-text: #0A0A0A` | Headings and body; example source `src/styles/tokens.css` |
| Accent / action | `--color-accent: #2563EB` | Primary buttons, links, selected controls |
| On accent | `--color-on-accent: #FFFFFF` | Text/icons on accent backgrounds; check contrast |
| Secondary action | `--color-secondary: #334155` | Secondary emphasis where the component spec calls for it |
| Page background | `--color-background: #FAFAFA` | Main canvas |
| Surface | `--color-surface: #FFFFFF` | Cards, menus, inputs |
| Success | `--color-success: #166534` | Success text/icons; pair colour with text |
| Error | `--color-error: #B91C1C` | Validation messages and error indicators |
| Muted text | `--color-muted: #475569` | Supporting text; check against its actual background |
| Border | `--color-border: #CBD5E1` | Dividers and card outlines |
| Control border | `--color-control-border: #64748B` | Input/control boundaries; check against the actual surface |
| Focus | `--color-focus: #2563EB` | Visible focus outline with separation from the control |

**Minimum:** document text, background, surface, action, border, focus, success, and error roles; their exact values or resolvable tokens; and intended pairings. Add theme variants when supported. Source tokens own values; the table must agree with them.

## 03 Typography

**Example proposal:** use the existing Inter font assets when available, with `system-ui, sans-serif` as fallback. Check availability before naming a font as implemented.

| Role | Token | Size / line height | Small-screen size / line height | Weight | Usage |
|---|---|---|---|---|---|
| H1 | `--type-h1` | `48px / 56px` | `32px / 40px` | `700` | Page title |
| H2 | `--type-h2` | `36px / 44px` | `28px / 36px` | `600` | Section heading |
| H3 | `--type-h3` | `24px / 32px` | `20px / 28px` | `600` | Subsection or card group |
| Body | `--type-body` | `16px / 24px` | `16px / 24px` | `400` | Main reading text |
| Label | `--type-label` | `14px / 20px` | `14px / 20px` | `600` | Form labels and concise controls |
| Caption | `--type-caption` | `14px / 20px` | `14px / 20px` | `400` | Supporting metadata |

**Minimum:** specify family/fallback, size, weight, line height, and usage for headings, body, and supporting text. Link authoritative tokens/font assets and describe responsive changes.

## 04 Spacing

| Token | Example value | Usage |
|---|---|---|
| `--space-1` | `4px` | Icon-to-label adjustment |
| `--space-2` | `8px` | Related inline elements |
| `--space-3` | `16px` | Control gaps and small-screen page gutters |
| `--space-4` | `24px` | Card padding and related groups |
| `--space-5` | `32px` | Section spacing |
| `--space-6` | `48px` | Large section gaps |
| `--space-7` | `64px` | Page-level separation |

**Minimum:** give the actual scale and examples of page gutters, component padding, and group gaps. Reuse existing spacing tokens; this sample scale is optional.

## 05 Border Radius

| Token | Example value | Applies to |
|---|---|---|
| `--radius-small` | `4px` | Small badges |
| `--radius-control` | `8px` | Buttons and inputs |
| `--radius-card` | `12px` | Cards and panels |
| `--radius-pill` | `999px` | Pill badges when part of the chosen style |

**Minimum:** map each used radius to a component. Document border/elevation tokens here when the UI uses them.

## 06 Components

| Component | Example appearance | Behavior / states | Example implementation |
|---|---|---|---|
| Primary button | Accent background, on-accent label, control radius, `12px 16px` padding | Click/keyboard activation; visible focus; disabled; loading keeps its label and width | `src/components/Button.tsx`, primary variant |
| Secondary button | Surface background, text label, border token | Same activation/focus rules; lower emphasis | The same `Button` implementation, secondary variant |
| Text field | Persistent label, surface background, control-border token, control radius | Typing, focus, required/invalid feedback, disabled state; errors linked to the field | `src/components/TextField.tsx` |
| Status badge | Small radius, compact padding, text plus optional icon | Communicates status without relying on colour alone | `src/components/Badge.tsx` |
| Card | Surface background, border, card radius, space-4 padding | Groups related content; actions remain real controls | `src/components/Card.tsx` |

**Minimum:** name the actual library/source paths and specify variants, spacing, typography, relevant states, and behavior for the product's primary action, secondary action, and form controls. Include other components only when used. Reuse the implementation instead of creating a second visual copy for the catalogue.

## 07 Icons

**Example proposal:** use the project's existing line-icon library; Lucide is one possible choice when no library exists. Default icon size `20px`, small size `16px`, stroke `1.5px`. Decorative icons are hidden from assistive technology; icon-only controls have an accessible name.

**Minimum:** identify the actual icon source, size/stroke conventions, and labeling rules. Naming this example does not authorize installing a library.

## 08 Breakpoints

| Range | Example width | Example layout behavior |
|---|---|---|
| Small | Below `640px` | One column, `16px` gutters, actions wrap without hiding labels |
| Medium | `640px` through `1023px` | Two columns where content permits, `24px` gutters |
| Large | `1024px` and above | Constrained `1200px` content width, `32px` gutters |

**Minimum:** specify exact boundaries and observable layout changes, including long text and overflowing content. Match the actual CSS/theme configuration and supported platforms.

## 09 States and Accessibility

| State | Example presentation | Required behavior to document/check |
|---|---|---|
| Loading | Button says "Saving..."; progress status is announced | Repeated submission is prevented without losing the user's input |
| Empty | "No tasks yet" with an Add task action | The next step is available by keyboard |
| Error | "Enter a task title" below the labeled field | Error is linked to the field, described in text, and can be corrected |
| Success | Task appears and a text status confirms the result | The result is perceivable without relying on colour |
| Disabled | Disabled button retains a readable label | Native disabled semantics or the project's equivalent match behavior |
| Focus / selected | Visible focus outline; checked task state is explicit | Keyboard order is predictable and control state is exposed semantically |

**Minimum:** cover applicable loading, empty, error, success, disabled, hover, focus, and selected states. Record keyboard, focus, semantics, contrast, and reduced-motion requirements plus what was actually checked. A populated table is not evidence of passing those checks.

## 10 Sources and Validation

| Item | Example location / check | Verification |
|---|---|---|
| Tokens / themes | `src/styles/tokens.css` | Replace with actual path and inspected values |
| Reusable components | `src/components/` | Replace with actual source links and representative variants |
| Working catalogue | `/design-system`, started with the repository's dev command | Proposed until the real route and behavior are verified |
| Interaction checks | Existing component/browser test command | Record the actual command, result, and limits |

**Minimum:** link authoritative sources and record executed checks, observed conflicts, and unverified work.

## 11 Working Design System

**Example proposal:** reuse an existing component workshop or add an internal `/design-system` page in a framework app. A vanilla site can use `docs/design-system/index.html`, served through its normal development server. These are alternatives; choose the repository's natural home.

| Demonstration | Minimum working coverage |
|---|---|
| Foundations | Colour/token swatches, heading/body/caption samples, spacing, radii, and icons from the shared sources |
| Actions | Actual primary/secondary buttons with click and keyboard feedback, disabled and loading examples |
| Forms | Actual fields with typing, validation/error correction, and applicable selection controls |
| Product components | The real badges/cards/navigation used by the app, with relevant variants and states |
| Layout | Small and large viewports, long content, and supported themes |

Record the actual source path, local URL, startup command, access boundary, and browser checks. Use synthetic data and local state. A working catalogue shares production components/tokens; static pictures do not establish interaction behavior. Use the skill's working-design-system guidance to choose the implementation and verification scope. If implementation is outside the current docs request, record a concrete proposal and offer that follow-up; do not mark the catalogue implemented.

## 12 Open Decisions

| Question | Affected surface | Owner or next evidence |
|---|---|---|
| [Exact unresolved design question, or state that none remain] | [Component or interaction] | [Who decides or what must be inspected] |

## Rules

- Use the agreed semantic tokens and existing components; document additions at their owning source.
- Keep this guide, the working catalogue, and the production UI consistent when shared design rules change.
- Link this document and the working catalogue from the project's agent instructions; include the verified way to open the catalogue.
