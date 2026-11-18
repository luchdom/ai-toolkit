# Git worktrees

Follow stricter repository rules for linked Git worktrees.

## Before creation

Get a direct owner instruction for the current work or use an explicitly invoked delivery entry or repository policy that grants worktree creation for this work. A plan, branch suggestion, or `working-tree` completion boundary does not grant creation authority.

1. Confirm the Git common directory and main checkout with `git worktree list --porcelain -z`. Use the main checkout even when working from a linked worktree.
2. Use `<main-worktree-root>/.ai/worktrees/<name>`. Normalize a work key or branch slug to one directory name. Reject absolute paths, traversal, separators, empty or dot names, Windows reserved names, and trailing dots or spaces.
3. Check every existing ancestor for reparse traversal and symlink escapes. Reject either. The resolved target's parent must be the main checkout's exact `.ai/worktrees` directory. Confirm the target is ignored with `git check-ignore -v --no-index` on a path below it. The expected rule is `/.ai/worktrees/`. Keep `.ai/loop.json` visible to Git.
4. Fetch the intended remote ref and resolve the authorized base to a full commit ID. Record the repository root, common directory, work key or task, fetched ref, resolved commit, branch, target path, and allowed command. If a branch, path, or registration already exists, follow the resume rules below.

## Create or resume

Before creating, match the current repository, common directory, task, base, branch, path, and command to the recorded authority. Stop if any required value is missing, stale, or mismatched. Use the recorded full commit ID in the command.

```text
git worktree add -b <branch> <exact-path> <resolved-base-commit>
```

Use the fetched ref as provenance only. If it advances, keep the recorded base commit. If stricter repository rules require the latest tip, stop and reconcile authority against the new commit before making changes. Use a non-forcing command.

After creation, verify the registered path, branch, exact HEAD, common directory, containment below the main checkout, ignore rule, and parent repository status. To resume, check that the registration, path, branch, common directory, work identity, and expected base match the authorized worktree. Stop on a mismatch and keep the existing worktree intact.

## Remove a worktree

Get separate removal authority for the exact registered worktree from the owner or an explicitly invoked policy. A disposable QA fixture may remove its own worktree when its test contract authorizes exact cleanup.

Before running `git worktree remove <exact-path>`, verify the resolved path, branch, and common directory. Check that tracked and untracked state is clean, the work is merged or has an explicit disposition, and no active process is using the worktree. If a check fails, leave the worktree intact and report cleanup as pending.

Use only `git worktree remove <exact-path>` for registered worktree cleanup. Warn that parent-level `git clean -x` can delete ignored worktrees.
