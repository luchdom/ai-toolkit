# Artifact contract

Keep enough evidence for the next stage, reviewer, or run.

## Current layout

When local workflow evidence is useful, use this layout in the target workspace:

```text
.ai/work/<YYYY-MM-DD>--<work-token>--<slug>[--<sequence>]/
  workflow.json                 # optional helper-owned metadata
  <date>-<slug>-delivery.md     # concise plan, decisions, checks, and outcome
```

Use separate files for substantial plans, designs, tasks, audits, reviews, or QA results. For routine Linear work, the issue, commits, and pull request can hold the record when no stage requires a separate file.

Use the same `.ai/work/` layout for a permitted standalone note or plan, including in workspaces without Git.

Before design or implementation, initialize or resume the workflow when [design gates](../../skills/spec-driven-delivery/references/design-gates.md) apply. Save the required design spec and rendered design review in its registered `artifactFolder`.

`<work-token>` is the external issue key or `local-<numeric-workKey>`. If a folder name exists, append `--02`, `--03`, and so on. For a repeated dated artifact, insert the sequence before its type, as in `<date>-<slug>--02-design.md`. Keep existing evidence. Before initializing in a Git repository, verify that Git ignores `.ai/work` and tracks none of its contents. Keep `.ai/loop.json` visible to Git.

Use the exact absolute `artifactFolder` from the descriptor and registry. Resume using an explicit issue, branch or pull request, workflow ID, or exact registered path. Let the workflow helper manage the identity fields in `workflow.json`. See the [descriptor schema](../../skills/goal-to-delivery/references/work-descriptor.schema.json) for field definitions.

Resolve the folder through the registration. Never infer it from a root path, date, or similar slug.

Use the [workflow helper](../../skills/goal-to-delivery/scripts/cli.py) to register local work and resume existing work. For a new Linear-backed registration, pass the observed issue to the helper's [`initialize_provider` API](../../skills/goal-to-delivery/scripts/workflow_init.py). Before allocating a new folder, check for an existing registration for the selected issue.

## Registered legacy compatibility

A workflow registered under `docs-ai/<legacy-folder>/` can continue in that exact folder until completion. Create new workflows under `.ai/work`.

## Historical read-only fallback

Use unregistered or tracked historical evidence as read-only context. This includes numbered folders, `docs-ai/history`, and flat `docs-ai/*` artifacts.

## Workflow-managed handoff

Handoff transfers regular files from the exact registered artifact folder and the explicitly approved working-tree scope. Git status alone misses files under the ignored `.ai/work` directory. Exclude adjacent ignored data and `.ai/worktrees`.

Handoff stops on unsafe paths, case conflicts, traversal, reparse points, hardlinks, destination collisions, concurrent changes, failed hashes, or rollback uncertainty. One transfer allows 512 files, 16 MiB per file, and 64 MiB total. Redact sensitive paths and content hashes. Use the source until the descriptor and registry update together. Apply the same checks to registered legacy work.

## Durable knowledge

Keep reusable setup, architecture, operations, troubleshooting, and product behavior in the repository docs. Link to existing policy and evidence. Keep secrets, tokens, notification topics, and unredacted customer data out of artifacts, Linear comments, commits, and pull requests.
