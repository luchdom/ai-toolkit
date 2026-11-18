# External Tools

Use this document for CLI tools and local runtimes. Follow the [external skill guide](EXTERNAL-SKILLS.md) to manage pinned skill imports and [MCP Servers](MCP-SERVERS.md) to register, configure, or authenticate servers.

## Select the Host Path

Start with [platform support](docs/platform-support.md). Use the current runtime OS, shell, home directory, and available commands; imported machine paths are historical evidence. PowerShell on macOS follows macOS installation and filesystem paths with PowerShell command syntax.

This repo requires Python 3.11 or newer. The examples use `python3` on macOS after checking its version, and `py -3` on Windows after the platform probe confirms that version requirement. A verified `python` at version 3.11 or newer or an absolute interpreter path is also suitable. In PowerShell, prefix a quoted executable path with `&`.

One-line CLI commands without shell-specific syntax work in both PowerShell and zsh/bash; the surrounding text identifies OS-specific steps. Use PowerShell backticks for multiline commands and POSIX backslashes in zsh/bash. The macOS package examples assume Homebrew is available; verify it with `brew --version` and use the linked official installers when it is unavailable. Check existing command versions and skill directories before installing, especially when Codex already provides an agent, skill, or plugin.

## Setup Order

1. Follow the [README](README.md#build-validate-and-install) to build and sync this repository. Normal sync includes the selected imports in [external-skills.toml](external-skills.toml).
2. Install the companion CLI tools required by the skills you use. Skill files and working CLI access are separate checks.
3. Configure the MCP servers you need through [MCP Servers](MCP-SERVERS.md).

## CLI Tools and Runtimes

### Markdownlint CLI2

Use [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) to check Markdown written by agents. Node.js 22 or newer is required for the pinned version. These commands work in macOS zsh and Windows PowerShell:

```sh
npm install --global markdownlint-cli2@0.24.0
markdownlint-cli2 --help
```

For repository-local checks, run `npm ci`. Follow [Markdown linting](docs/markdown-linting.md) for exact-file checks, shared defaults, user-level sync, and recovery. Respect a target project's own Markdown lint configuration.

### .NET SDK 10

Links:

- [Install .NET on Windows](https://learn.microsoft.com/en-us/dotnet/core/install/windows)
- [Install .NET on macOS](https://learn.microsoft.com/en-us/dotnet/core/install/macos)
- [Homebrew .NET 10 formula](https://formulae.brew.sh/formula/dotnet@10)

Recommended for:

- Repos that target `net10.0`, including current Luchdom backend scaffolds.

Windows install from Microsoft Learn:

```powershell
winget install Microsoft.DotNet.SDK.10
```

macOS with Homebrew:

```sh
brew install dotnet@10
```

Follow Homebrew's emitted PATH instructions if `dotnet` is not found. Select an SDK compatible with the target repository's `global.json` when it pins one.

Verify:

```powershell
dotnet --list-sdks
```

### GitHub CLI

Links:

- [GitHub CLI README](https://github.com/cli/cli)
- [GitHub CLI manual](https://cli.github.com/manual/index)
- [GitHub CLI installation on Windows](https://github.com/cli/cli/blob/trunk/docs/install_windows.md)
- [GitHub CLI installation on macOS](https://github.com/cli/cli/blob/trunk/docs/install_macos.md)

Recommended for:

- local PR workflows
- manual repo inspection
- auth verification outside MCP

Repo workflow:

- Use `$github-cli` for safe read-first GitHub CLI workflows.
- Use `$pr-description` before drafting or updating PR titles and bodies.

Install on Windows:

```powershell
winget install --id GitHub.cli --source winget
```

Install on macOS:

```sh
brew install gh
```

After install, check `gh auth status`. Authenticate when the task requires account access and the user has authorized it:

```powershell
gh auth login
gh auth status
```

### yt-dlp

Links:

- [yt-dlp repository](https://github.com/yt-dlp/yt-dlp)
- [Official installation guide](https://github.com/yt-dlp/yt-dlp/wiki/Installation)
- [Official releases](https://github.com/yt-dlp/yt-dlp/releases)
- [Official FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ)

Recommended for:

- downloading public or user-authorized video and audio
- reading video metadata and available formats
- preparing temporary audio for `$transcribe-videos`
- processing direct, non-DRM media streams exposed by an authorized page

Official Windows package-manager install:

```powershell
winget install yt-dlp
```

Windows update:

```powershell
winget upgrade yt-dlp
```

macOS install, including media utilities:

```sh
brew install yt-dlp ffmpeg
```

Use `brew upgrade yt-dlp ffmpeg` when an update is needed. Verify on either OS:

```text
yt-dlp --version
yt-dlp --help
ffmpeg -version
ffprobe -version
```

Notes:

- `ffmpeg` and `ffprobe` are strongly recommended by the yt-dlp project for merging separate audio/video formats and post-processing. Install the binaries, not the unrelated Python package named `ffmpeg`.
- Use yt-dlp only for public content, user-provided files, or content the user is authorized to access. Do not bypass DRM, paywalls, or access controls.
- Do not export cookies by default. `--cookies-from-browser` can read broad browser authentication state; require explicit approval and keep any authentication material out of repositories and logs.
- Treat signed player and HLS URLs as temporary secrets. Never persist them in transcripts, summaries, Git, or PR evidence.
- For text-only work, use a disposable media directory and delete it after validating `summary.md` and `transcript.md`.
- Invoke `$transcribe-videos` for the repository-owned workflow covering YouTube, local media, authorized course pages, batch lesson enumeration, transcription, Markdown output, validation, and cleanup.

### RTK

Links:

- [RTK repository](https://github.com/rtk-ai/rtk)
- [RTK releases](https://github.com/rtk-ai/rtk/releases)
- [Homebrew RTK formula](https://formulae.brew.sh/formula/rtk)

Recommended for:

- reducing noisy command output before it reaches an agent context

Windows setup:

- Download `rtk-x86_64-pc-windows-msvc.zip` from the releases page.
- Put `rtk.exe` on `PATH`, such as `%USERPROFILE%\.local\bin`.
- Use it from PowerShell, Command Prompt, or Windows Terminal; do not launch the executable directly.

macOS setup:

```sh
brew install rtk
```

Enable RTK for a supported agent only after reviewing its telemetry behavior:

```powershell
rtk init -g --codex
rtk --version
rtk gain
```

Restart the agent after initialization. Native Windows supports RTK filtering, though automatic hook rewriting is more limited than WSL.

### CodeGraph

Links:

- [CodeGraph repository](https://github.com/colbymchenry/codegraph)

Recommended for:

- indexed codebase exploration in larger repositories where symbol search, call paths, or impact analysis reduce repeated file searches

Official setup:

```powershell
npx @colbymchenry/codegraph
codegraph init
```

Notes:

- `codegraph init` creates the local `.codegraph/` index; do not commit it.
- Use CodeGraph only for supported, indexed files. Fall back to `rg` and direct reads when indexing is unavailable or incomplete.
- CodeGraph may append its own configuration to instruction files. This repo's marker-managed tool instructions preserve content outside their managed marker block during normal sync.

See [CodeGraph MCP configuration](MCP-SERVERS.md#codegraph) when MCP access is needed.

### Graphify

Links:

- [Graphify repository](https://github.com/Graphify-Labs/graphify)
- [Graphify package on PyPI](https://pypi.org/project/graphifyy/)

Recommended for:

- supplementary local knowledge-graph extraction and queries
- code-only AST indexing that does not require an API key
- a portable JSON graph that can combine multiple repositories

Install the official PyPI package in an isolated environment:

```text
uv tool install graphifyy
graphify --version
```

For each selected repository, keep generated graphs outside the Git
worktrees and use local AST-only extraction. `--code-only` skips docs, PDFs, and
images and does not call an LLM. Replace `<repository-path>` and `<name>` with the current host's checkout and a stable index name; the quoted `$HOME` paths work in both PowerShell and zsh/bash:

```text
graphify extract "<repository-path>" --code-only --out "$HOME/.codex/graphify-indexes/<name>"
graphify global add "$HOME/.codex/graphify-indexes/<name>/graphify-out/graph.json" --as "<name>"
graphify global list
graphify global path
```

Notes:

- The PyPI distribution is `graphifyy`; the installed command is `graphify`.
- Full semantic extraction can process docs and media through an LLM backend.
  Do not omit `--code-only` for private repositories unless the user has
  explicitly approved the selected provider and data boundary.
- A generated graph does not establish exhaustive source coverage; use direct
  source reads for reported gaps.

### AWS CLI

Link:

- [Installing or updating the latest AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

Recommended for:

- repos that eventually provision or inspect AWS resources outside the editor

Official Windows MSI command from the AWS docs:

```powershell
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

macOS with Homebrew:

```sh
brew install awscli
```

The linked AWS guide also provides the official macOS package installer.

Verify:

```powershell
aws --version
```

### Playwright CLI

Use [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) for browser automation through a CLI and agent skills.

```text
npm install -g @playwright/cli@latest
playwright-cli --help
```

Use [Playwright MCP](MCP-SERVERS.md#playwright) for persistent browser sessions.

### UI/UX Pro Max CLI

Use [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) for searchable design guidance and bundled datasets.

```text
npm install -g ui-ux-pro-max-cli
uipro --version
```

### PostHog CLI

Use [@posthog/cli](https://www.npmjs.com/package/@posthog/cli) for analytics setup, source maps, and product instrumentation. See the [official source map CLI documentation](https://posthog.com/docs/error-tracking/upload-source-maps/cli).

Preferred local install:

```powershell
npm install -g @posthog/cli
posthog-cli login
posthog-cli --help
```

PostHog's CLI docs also provide a native Windows installer:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://download.posthog.com/cli | iex"
posthog-cli login
posthog-cli --help
```

Follow [MCP Servers](MCP-SERVERS.md#posthog) for the remote skills store.

### Stripe CLI Sandbox

[Build on Stripe with AI](https://docs.stripe.com/building-with-ai) documents this sandbox bootstrap:

```text
stripe sandbox create
```

This command provisions an anonymous, claimable sandbox with API keys. The [import manifest](external-skills.toml) pins the Stripe skill files separately.

### MCP Server Binaries

Some server installers also provide a local executable. Keep their complete setup together in [MCP Servers](MCP-SERVERS.md). A binary on `PATH` does not establish agent registration or authenticated service access.
