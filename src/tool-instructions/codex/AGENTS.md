<!-- AI-TOOLKIT-LUCHDOM:START -->
# Project AI instructions

## Delivery workflow

Follow the [shared delivery workflow](<{{LUCHDOM_AI_TOOLKIT_ROOT}}/src/tool-instructions/shared/delivery-workflow.md>). It links the delivery stages and the shared rules for artifacts, publication, and worktrees. Use this repository's commands and stricter rules.

## Execution platform

Before setup or runtime commands, follow the [platform guide](<{{LUCHDOM_AI_TOOLKIT_DOCS}}/platform-support.md>). Identify the execution host OS, active shell, actual checkout/home, and available interpreter; never infer the OS from old paths or the shell name. Use macOS/POSIX or Windows/PowerShell commands as appropriate. From the toolkit checkout, run `python3 scripts/platform_info.py` on macOS or `py -3 scripts/platform_info.py` on Windows and retain the verified Python 3.11+ executable. Resolve paths on the current host; model and sandbox preferences are separate from platform selection.

## Markdown linting

Lint every Markdown file you create or edit before reporting completion. Use the repository's command/configuration first and explicit changed-file paths; otherwise use the installed `markdownlint-cli2` fallback described in [Markdown linting](<{{LUCHDOM_AI_TOOLKIT_DOCS}}/markdown-linting.md>). Fix findings in scope, inspect automatic fixes, and rerun the check. Report missing tooling or unresolved findings; never claim an unrun check passed.

{{PROJECT_DOCUMENTATION_GUIDANCE}}

## .NET implementation

For authorized C#/.NET backend implementation, use `$dotnet-implementation`.

<!-- AI-TOOLKIT-LUCHDOM:END -->
