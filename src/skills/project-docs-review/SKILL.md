---
name: project-docs-review
description: Assess a repository's project documentation for missing foundations, unclear placement, stale claims, and contradictions. Use for docs health checks or gaps found during project work; return targeted suggestions without editing files.
---

# Project Docs Review

Assess the selected repository against [the project documentation standard](../project-docs/references/documentation-standard.md). Keep the review proportional to the task: a gap noticed during a small fix needs a small assessment, while an explicit repository-wide review covers each applicable foundation.

```text
$project-docs-review
$project-docs-review check whether the UI docs match the current tokens
```

1. Read root/scoped `AGENTS.md`, README or the docs index, and existing product, design, and architecture references. Follow the documented equivalents rather than judging filenames alone.
2. Map the four concerns to their actual owners and check the standard's minimum coverage. Follow each relevant tool instruction through root `AGENTS.md` to its actual docs; identify missing/broken pointers, duplicate ownership, and misplaced files. For a project without a UI, a design system may be not applicable.
3. Inspect relevant source/configuration and approved decisions to verify significant claims. For UI projects, assess an existing or proposed working catalogue, its shared tokens/components, and recorded source/URL/startup/access instructions. Exercise interactions only when runtime review is in scope; otherwise report them unverified. Sample representative boundaries for a broad review and state the sample; headings, copied example values, or screenshots alone do not prove coverage or behavior. Distinguish approved intent from current implementation before declaring drift.
4. Report actionable gaps with exact paths, evidence, effect on the current task, and the smallest remedy. Identify which decisions need owner input. Return the assessment in the reply unless a report file was explicitly requested.

Use a concise map when it helps:

| Concern | Existing path or owner | Assessment | Evidence or next action |
|---|---|---|---|
| Product intent | [Actual path or missing] | [Covered, partial, conflicting, or missing] | [Specific finding and source] |
| UI design | [Actual path or not applicable] | [Assessment] | [Evidence or applicability reason] |
| Architecture | [Actual path or missing] | [Assessment] | [Specific finding and source] |
| Agent routing | [Root/scoped instructions] | [Assessment] | [Specific finding and source] |

Suggest `$project-docs` with the exact document/scope needed when creation or refinement would help. Honor earlier suggestions and declines in this project context. Recommend optional sections/pages only for demonstrated needs; name equivalent existing documents that should be reused.

This review leaves files in place. A separate create/refine request or active docs-editing scope supplies editing authority; when invoked from `$project-docs`, return findings to that authoring pass. Missing files alone do not block unrelated authorized work. Surface a blocking decision only when the requested work cannot safely proceed without it.

Return coverage, prioritized findings, checked evidence, and verification limits. Documentation review does not establish runtime QA, visual conformance, or owner approval of proposals.
