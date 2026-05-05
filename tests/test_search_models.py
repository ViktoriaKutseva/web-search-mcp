import unittest

from pydantic import ValidationError

from web_search_mcp.domains.search.models import SearchResponse, SearchResult


class SearchResultModelTests(unittest.TestCase):
    def test_search_result_accepts_required_fields(self) -> None:
        result = SearchResult(
            title="Example Title",
            url="https://example.com",
        )

        self.assertEqual(result.title, "Example Title")
        self.assertEqual(result.url, "https://example.com")
        self.assertIsNone(result.content)
        self.assertIsNone(result.engine)

    def test_search_result_rejects_missing_required_fields(self) -> None:
        with self.assertRaises(ValidationError):
            SearchResult(url="https://example.com")

        with self.assertRaises(ValidationError):
            SearchResult(title="Example Title")


class SearchResponseModelTests(unittest.TestCase):
    def test_search_response_defaults(self) -> None:
        response = SearchResponse(query="unit testing")

        self.assertEqual(response.query, "unit testing")
        self.assertEqual(response.results, [])
        self.assertEqual(response.number_of_results, 0)
        self.assertIsNone(response.error)

    def test_search_response_parses_nested_result_dicts(self) -> None:
        response = SearchResponse(
            query="python",
            results=[
                {
                    "title": "Python Official",
                    "url": "https://python.org",
                    "content": "Python programming language",
                    "engine": "searxng",
                }
            ],
            number_of_results=1,
        )

        self.assertEqual(response.number_of_results, 1)
        self.assertEqual(len(response.results), 1)
        self.assertIsInstance(response.results[0], SearchResult)
        self.assertEqual(response.results[0].title, "Python Official")
        self.assertEqual(response.results[0].url, "https://python.org")
        self.assertEqual(response.results[0].content, "Python programming language")
        self.assertEqual(response.results[0].engine, "searxng")

    def test_search_response_rejects_invalid_result_item(self) -> None:
        with self.assertRaises(ValidationError):
            SearchResponse(
                query="python",
                results=[{"title": "missing url"}],
            )


if __name__ == "__main__":
    unittest.main()
