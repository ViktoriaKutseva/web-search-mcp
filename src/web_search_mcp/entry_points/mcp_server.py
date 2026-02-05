from fastmcp import FastMCP
from web_search_mcp.infrastructure.clients.searxng import SearxNGClient
from web_search_mcp.domains.search.services import SearchService
from web_search_mcp.config.logging import configure_logging

# Configure logging at module level or startup
configure_logging()

# Initialize MCP Server
mcp = FastMCP("Web Search MCP")

def get_search_service() -> SearchService:
    """Dependency wiring for SearchService."""
    client = SearxNGClient()
    return SearchService(client)

@mcp.tool()
def web_search(query: str, limit: int = 10) -> str:
    """
    Perform a web search using the configured search engine (SearxNG).
    
    Args:
        query: The search query string.
        limit: Maximum number of results to return (default: 10).
        
    Returns:
        A JSON string containing the search results.
    """
    service = get_search_service()
    response = service.perform_search(query, limit)
    return response.model_dump_json(indent=2)
