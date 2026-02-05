from typing import List, Protocol
from loguru import logger
from web_search_mcp.domains.search.models import SearchResponse, SearchResult

class SearchClient(Protocol):
    """Protocol for search clients."""
    def search(self, query: str, limit: int) -> List[SearchResult]:
        ...

class SearchService:
    """
    Service for performing web searches.
    """
    def __init__(self, search_client: SearchClient):
        self._search_client = search_client

    def perform_search(self, query: str, limit: int = 10) -> SearchResponse:
        """
        Execute a search query and return formatted results.
        """
        logger.info(f"Performing search for query: '{query}' with limit: {limit}")
        
        try:
            results = self._search_client.search(query, limit)
            logger.debug(f"Search returned {len(results)} results")
            
            response = SearchResponse(
                query=query,
                results=results,
                number_of_results=len(results)
            )
            return response
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
