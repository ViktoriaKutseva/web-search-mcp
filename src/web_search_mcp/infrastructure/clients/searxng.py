import httpx
from typing import List, Any, Dict
from loguru import logger
from web_search_mcp.config.settings import settings
from web_search_mcp.domains.search.models import SearchResult
from web_search_mcp.domains.search.exceptions import SearchProviderError

class SearxNGClient:
    """
    Client for interacting with a SearxNG instance.
    """
    def __init__(self, base_url: str = settings.SEARXNG_BASE_URL, timeout: int = settings.SEARXNG_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """
        Perform a search query against SearxNG.
        """
        url = f"{self.base_url}/search"
        params: Dict[str, Any] = {
            "q": query,
            "format": "json",
            "categories": "general",
            "language": "en-US",
            "pageno": 1,
        }
        
        # SearxNG doesn't strictly support 'limit' in params usually, it returns results per page.
        # We can implement client-side slicing or try using 'time_range' etc if needed.
        # But 'limit' isn't a standard param in all searxng instances, usually controlled by preferences.
        # We will slice the result.

        try:
            logger.debug(f"Requesting {url} with params {params}")
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error communicating with SearxNG: {e}")
            raise SearchProviderError(f"SearxNG communication error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error communicating with SearxNG: {e}")
            raise SearchProviderError(f"SearxNG unexpected error: {e}")

        return self._parse_results(data, limit)

    def _parse_results(self, data: Dict[str, Any], limit: int) -> List[SearchResult]:
        """
        Parse the raw JSON response from SearxNG into domain models.
        """
        raw_results = data.get("results", [])
        parsed_results: List[SearchResult] = []

        for result in raw_results:
            if len(parsed_results) >= limit:
                break
                
            # SearxNG result field mapping
            title = result.get("title", "")
            url = result.get("url", "")
            content = result.get("content", "")
            engine = result.get("engine", "")

            # Basic validation
            if not title or not url:
                continue

            parsed_results.append(SearchResult(
                title=title,
                url=url,
                content=content,
                engine=engine
            ))

        return parsed_results
