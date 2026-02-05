# Step-by-Step Setup Guide for Web Search MCP

This guide lists the specific steps to set up the Web Search MCP server and integrate it into your development environment or MCP clients (like Claude Desktop).

## Prerequisites

Before starting, ensure you have the following installed:

1.  **Docker & Docker Compose**: For running the local SearxNG instance.
2.  **uv**: An extremely fast Python package installer and resolver.
    - Install instructions: [astral.sh/uv](https://github.com/astral-sh/uv)

## Step 1: Prepare Local SearxNG

You need the configuration files from this repository to run the local search engine instance that the MCP server will connect to.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/ViktoriaKutseva/web-search-mcp.git
    cd web-search-mcp
    ```

## Step 2: Start the Search Engine

The MCP server relies on a local instance of SearxNG.

1.  **Configure SearxNG**
    Copy the example settings file to create the actual configuration.
    ```bash
    cp searxng/settings.yml.example searxng/settings.yml
    ```
    *Note: The `settings.yml` file is git-ignored. You should generate a new `secret_key` inside it.*

2.  **Start Services**
    From the repository root run:
    ```bash
    docker compose up -d
    ```

3.  **Verify SearxNG**
    Open your browser and navigate to `http://localhost:8080`. You should see the SearxNG search interface.

## Step 3: Configure MCP Client

To use this tool in other specific projects or global editors, you need to register it with your MCP Client (e.g., Claude Desktop, VS Code extension).

### Option A: Integration with Claude Desktop

1.  **Locate Config File**
    Find or create the `claude_desktop_config.json` file:
    *   **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2.  **Edit Configuration**
    Add the `web-search` entry to the `mcpServers` object.

    ```json
    {
      "mcpServers": {
        "web-search": {
          "command": "uvx",
          "args": [
            "web-search-mcp"
          ],
          "env": {
            "SEARXNG_BASE_URL": "http://localhost:8080"
          }
        }
      }
    }
    ```

3.  **Restart Claude Desktop**
    Completely quit and restart the application for changes to take effect.

## Step 4: Verification

1.  Open your MCP Client (e.g., Claude Desktop).
2.  Look for the 🔌 icon or installed tools list to verify `web-search` is connected.
3.  Ask a question that requires searching the web:
    > "Search for the latest release of Python and tell me the date."

## Troubleshooting

-   **SearxNG not reachable**: Ensure Docker container is running (`docker ps`) and port 8080 is free.
-   **MCP Error**: Check the logs in your client or run `uvx web-search-mcp` manually in the terminal to see if it starts without crashing (it will wait for stdio input).

## Configuration

Settings are managed via environment variables (or \`.env\` file):

- \`SEARXNG_BASE_URL\`: URL of the SearxNG instance (default: \`http://localhost:8080\`)
- \`SEARXNG_TIMEOUT\`: Request timeout in seconds (default: \`10\`)
- \`LOG_LEVEL\`: Logging level (default: \`INFO\`)

## Development

- **Architecture**: Follows simplified DDD guidelines.
  - \`domains/\`: Business logic
  - \`infrastructure/\`: External implementations (SearxNG client)
  - \`entry_points/\`: MCP server and Main execution
  - \`config/\`: Settings
