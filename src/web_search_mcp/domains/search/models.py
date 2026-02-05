from typing import List, Optional
from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    """
    Represents a single search result from a search engine.
    """
    title: str = Field(..., description="Title of the search result")
    url: str = Field(..., description="URL of the search result")
    content: Optional[str] = Field(None, description="Snippet or content of the result")
    engine: Optional[str] = Field(None, description="Source engine (e.g. google, bing)")

class SearchResponse(BaseModel):
    """
    Represents a response containing a list of search results.
    """
    query: str = Field(..., description="The original search query")
    results: List[SearchResult] = Field(default_factory=list, description="List of search results")
    number_of_results: int = Field(0, description="Total number of results returned")
