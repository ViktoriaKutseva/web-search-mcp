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
        clean_query = query.strip()
        if not clean_query:
            return []

        if limit <= 0:
            return []

        # Keep request defaults conservative because instance-specific params can trigger upstream errors.
        primary_params: Dict[str, Any] = {
            "q": clean_query,
            "format": "json",
            "categories": "general",
            "language": "en-US",
            "pageno": 1,
        }
        fallback_params: Dict[str, Any] = {
            "q": clean_query,
            "format": "json",
        }

        data = self._request_json_with_fallback(primary_params, fallback_params)
        return self._parse_results(data, limit)

    def _request_json_with_fallback(self, primary_params: Dict[str, Any], fallback_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Try a primary request first, retry once on 5xx, then fallback to minimal params.
        """
        url = f"{self.base_url}/search"

        try:
            return self._request_json_with_retry(url, primary_params)
        except SearchProviderError as primary_error:
            logger.warning(f"Primary SearxNG request failed, retrying with fallback params: {primary_error}")
            try:
                return self._request_json_with_retry(url, fallback_params)
            except SearchProviderError as fallback_error:
                raise SearchProviderError(
                    f"SearxNG request failed after fallback. Primary: {primary_error}. Fallback: {fallback_error}"
                )

    def _request_json_with_retry(self, url: str, params: Dict[str, Any], attempts: int = 2) -> Dict[str, Any]:
        """
        Perform request and retry transient server failures (HTTP 5xx).
        """
        last_error: Exception | None = None

        for attempt in range(1, attempts + 1):
            try:
                logger.debug(f"Requesting {url} with params {params} (attempt {attempt}/{attempts})")
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.get(url, params=params)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                if 500 <= status_code < 600 and attempt < attempts:
                    logger.warning(
                        f"Transient SearxNG HTTP {status_code} on attempt {attempt}; retrying request."
                    )
                    last_error = e
                    continue
                raise SearchProviderError(f"HTTP error from SearxNG: {status_code}")
            except httpx.HTTPError as e:
                if attempt < attempts:
                    logger.warning(f"SearxNG transport error on attempt {attempt}; retrying. Error: {e}")
                    last_error = e
                    continue
                raise SearchProviderError(f"SearxNG communication error: {e}")
            except ValueError as e:
                raise SearchProviderError(f"Invalid JSON response from SearxNG: {e}")
            except Exception as e:
                raise SearchProviderError(f"SearxNG unexpected error: {e}")

        raise SearchProviderError(f"SearxNG request failed after retries: {last_error}")

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
