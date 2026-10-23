<!-- AI-TOOLKIT-MARKDOWN:START -->
## Markdown linting

Whenever you create or edit `.md` or `.markdown` files, lint the changed files before reporting completion. Use the repository's Markdown lint command and configuration first. Run from the project root and pass explicit file paths so unrelated files stay outside the fix scope.

If the project has no Markdown lint configuration, use the installed fallback:

```sh
markdownlint-cli2 --no-globs --config "$HOME/.config/ai-toolkit/markdownlint-cli2.jsonc" ":path/to/changed-file.md"
```

The same one-line command works in PowerShell. The `:` prefix treats the argument as a literal path, including names containing glob characters. Quote each path separately.

Fix findings in files you changed, use `--fix` only for those files, inspect the diff, and rerun without `--fix`. Preserve prose, front matter, code examples, and unrelated edits. Do not disable rules or add ignores just to obtain a pass. If the linter is unavailable or a finding cannot be resolved within the authorized scope, report the exact limitation instead of claiming validation passed.
<!-- AI-TOOLKIT-MARKDOWN:END -->
