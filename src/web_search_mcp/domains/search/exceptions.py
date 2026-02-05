class SearchError(Exception):
    """Base exception for search domain."""
    pass

class SearchProviderError(SearchError):
    """Raised when the search provider fails."""
    pass
