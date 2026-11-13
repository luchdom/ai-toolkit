# MCP Servers

Use this document to configure Model Context Protocol (MCP) servers for a selected agent environment. [External Tools](EXTERNAL-TOOLS.md) covers companion executables; [External Skills](EXTERNAL-SKILLS.md) covers imported instructions and native plugins.

Toolkit and external skill sync do not register MCP servers, change agent configuration, run login flows, or initialize a memory store. Configure only the servers needed for the current environment. Keep credentials in the environment or the agent's supported credential store, never in this repository.

## Setup and Verification

1. Follow [platform support](docs/platform-support.md), then install the required runtime or binary.
2. Inspect the linked official documentation and existing agent registration before adding a server. Plugin-managed servers should stay managed by that plugin.
3. Apply the chosen agent's configuration and complete its authentication flow when needed.
4. Restart the agent session when required, verify the server registration, and exercise a read-only operation through its actual tools. A skill file or a configured URL alone does not prove connectivity.

These examples document manual setup. A shared MCP setup script is intentionally deferred until repeated configuration steps justify one; credentials, login, indexing, and mining remain explicit operations.

## Servers

### CodeGraph

Install the [CodeGraph CLI](EXTERNAL-TOOLS.md#codegraph) and initialize only the selected repository. Print its Codex configuration for review:

```text
codegraph install --print-config codex
```

Apply the reviewed configuration using the [upstream instructions](https://github.com/colbymchenry/codegraph). Keep `.codegraph/` indexes outside tracked source. Existing toolkit instruction markers preserve unrelated content, but configuration or instruction changes still require the selected setup scope.

### Playwright

Link:

- [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)

Use when:

- You explicitly want MCP-based browser automation rather than Playwright CLI skills.

Official examples:

```powershell
claude mcp add playwright npx @playwright/mcp@latest
codex mcp add playwright npx "@playwright/mcp@latest"
```

Codex config alternative from the repository README:

```toml
[mcp_servers.playwright]
command = "npx"
args = ["@playwright/mcp@latest"]
```

### MemPalace

The [native MemPalace plugin](EXTERNAL-SKILLS.md#mempalace) provides its MCP server and writable memory skills. Verify the CLI and registration after installing the plugin:

```text
mempalace --version
codex plugin list
codex mcp get mempalace
mempalace status
```

The server runtime is supplied by the executable on `PATH`. Restart Codex after runtime upgrades. Plugin registration and initialization are separate: follow [the approved-source mining procedure](EXTERNAL-TOOLS.md#mempalace) before creating or mining a palace. MemPalace returns mined text verbatim; only approved source content belongs in it.

See the [official MCP integration guide](https://mempalaceofficial.com/guide/mcp-integration.html) for agent-specific setup and the [getting-started guide](https://mempalaceofficial.com/guide/getting-started.html) for initialization.

### PostHog

Use the [PostHog MCP server or AI plugin](https://github.com/PostHog/ai-plugin) when remote product tools or the [hosted skills store](https://posthog.com/docs/prompt-management/skills-store) are needed. Prefer the [CLI](EXTERNAL-TOOLS.md#posthog-cli) for local command workflows.

The hosted skills store keeps versioned Agent Skills-style `SKILL.md` bodies and optional bundled files in PostHog Prompt Management. Its remote workflow uses tools such as `skill-list`, `skill-get`, `skill-file-get`, `skill-create`, and `skill-update`; the native plugin supplies a `skills-store` bridge. This is separate from the Git-directory imports selected in `external-skills.toml`.

For a self-hosted instance, set the supported endpoint before configuring the plugin. Windows PowerShell:

```powershell
$env:POSTHOG_MCP_URL = "https://mcp.your-posthog-instance.com/mcp"
```

macOS / zsh:

```sh
export POSTHOG_MCP_URL="https://mcp.your-posthog-instance.com/mcp"
```

Use the official authentication flow. Do not store tokens in the endpoint example or commit environment files.

### Linear

Link:

- [Linear MCP server docs](https://linear.app/docs/mcp)

Recommended for:

- issue intake and status updates in repos that use Linear as the autonomous work queue

Official Codex setup from the Linear docs:

```powershell
codex mcp add linear --url https://mcp.linear.app/mcp
codex mcp login linear
```

The Linear docs also note that some Codex versions require the remote MCP feature to be enabled in `~/.codex/config.toml`.

Verify the registration after login:

```text
codex mcp get linear
```

The [Linear skill](EXTERNAL-SKILLS.md#openai-curated-linear-skill) supplies workflow instructions; the server supplies issue access. Older installed skill instructions may mention `rmcp_client` or `codex --enable rmcp_client`. Treat those as version-specific guidance and check the current agent documentation before changing feature settings.

## Recovery

If a server fails, inspect its configured command or URL, required environment variable names, local runtime version, and authentication status. Preserve unrelated server registrations. Remove or restore only the exact registration changed by the selected setup, using the agent or plugin's supported command. Do not delete the whole agent configuration or copy cached credentials between machines.
