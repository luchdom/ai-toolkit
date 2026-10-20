# Codex skill restore checklist

Snapshot: 2026-10-20. This is the set of skills available in the Codex session on that date **in addition to** the skills maintained in this repository and `C:\dev\social-media\social-media-toolkit`. The two repositories contained 15 and 8 distinct source skills, respectively. This checklist contains 83 additional available skill IDs, counting duplicate installations once.

This is an inventory and a restore target, not a claim that every listed skill lacks a source repository elsewhere. The paths below describe the original Windows installation; use the new environment's home directory when restoring.

## Request for a fresh environment

> Read `docs/codex-skill-restore.md` in `ai-toolkit`. Install this repository's Codex skills using its README, then install the social-media toolkit's Codex skills using that repository's instructions. Ensure every additional skill in the inventory below is available in a **fresh Codex session**. Use the documented or official source for missing user and plugin skills; do not treat a cached `SKILL.md` as proof that Codex has loaded it. Verify any required companion CLI separately. Report each skill that cannot be restored, its source or version uncertainty, and the action needed from me. Do not silently omit or substitute a skill.

The [ai-toolkit README](../README.md) documents this repository's build, validation, and sync commands. [External Tools](../EXTERNAL-TOOLS.md) documents installation and verification for some external skills and plugins. The social-media toolkit has its own install instructions. Check current tool documentation before running install commands, as plugin names and availability may change.

## How to verify

1. Install the two repository-managed skill sets separately. This file covers only the additional skills below.
2. Restore user-level skills to the appropriate user-level location. On the original machine these were under `C:\Users\lucas\.codex\skills` and `C:\Users\lucas\.agents\skills`. Do not assume the same home path in a new environment.
3. Check that the Codex system skills are supplied by the installed Codex version. Install or enable the listed plugin packages through the supported plugin manager.
4. Start a new Codex session and compare its **available skills** with all 83 qualified IDs below. Check the `SKILL.md` files for user-level skills as a secondary file check. A plugin cache directory or an old session's skill list alone is insufficient.
5. Record missing skills and any renamed equivalents explicitly. Confirm external CLI or service access only when a skill actually requires it; skill availability and service authentication are separate checks.

In the tables, a name in package `P` means the qualified skill ID `P:name`. Preserve capitalization in names such as `Presentations` and `Spreadsheets`.

## Codex system skills (4)

| Package | Skills |
| --- | --- |
| `interface-design` | `imagegen`, `openai-docs`, `skill-creator`, `skill-installer` |

## User-level skills (30 unique)

| Original location | Package | Skills |
| --- | --- | --- |
| `C:\Users\lucas\.codex\skills` | `interface-design` | `codebase-memory`, `gpt-taste`, `graphify`, `linear`, `pdf`, `playwright`, `pluggy-doctor`, `pluggy-integration`, `pluggy-open-finance`, `pluggy-payments`, `remotion-captions`, `remotion-docs`, `remotion-markup`, `remotion-render` |
| `C:\Users\lucas\.agents\skills` | `interface-design` | `banner-design`, `brand`, `design`, `design-system`, `firecrawl`, `firecrawl-agent`, `firecrawl-browser`, `firecrawl-crawl`, `firecrawl-download`, `firecrawl-map`, `firecrawl-scrape`, `firecrawl-search`, `reverse-engineer-anything`, `slides`, `ui-styling`, `ui-ux-pro-max` |

`codebase-memory` also had a copy under `C:\Users\lucas\.agents\skills`; it is counted once. Two other local `SKILL.md` files, `napkin` and `review-agent`, were present on disk but were not exposed in that Codex session's available-skills list, so they are not restore targets in the 83.

## Plugin skills (49)

| Package | Skills |
| --- | --- |
| `computer-use` | `computer-use` |
| `documents` | `documents` |
| `google-drive` | `google-docs`, `google-drive`, `google-drive-comments`, `google-sheets`, `google-slides` |
| `mempalace` | `mempalace`, `mempalace-recall`, `mempalace-task`, `source-command-mempalace-audit`, `source-command-mempalace-help`, `source-command-mempalace-init`, `source-command-mempalace-mine`, `source-command-mempalace-search`, `source-command-mempalace-status` |
| `notion` | `notion-database-designer`, `notion-meeting-intelligence`, `notion-research-documentation`, `notion-spec-to-implementation`, `notion-weekly-project-digest` |
| `pages` | `maintain-space`, `manage-schedules`, `organize-space`, `write-page` |
| `pdf` | `pdf` |
| `plugin-management` | `plugin-management` |
| `ponytail` | `ponytail`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`, `ponytail-review` |
| `posthog` | `posthog` |
| `presentations` | `Presentations` |
| `product-design` | `audit`, `ideate`, `image-to-code`, `index`, `url-to-code` |
| `sites` | `sites`, `sites-remix` |
| `spreadsheets` | `Spreadsheets`, `excel-live-control` |
| `template-creator` | `template-creator` |
| `visualize` | `visualize` |
| `work-pets` | `create-pet`, `pets`, `update-pet` |

Some plugin caches contained additional copies or skills that were not exposed in the session. They are not part of this restore target. `interface-design:pdf` and `pdf:pdf` are separate skill IDs and both are included.
