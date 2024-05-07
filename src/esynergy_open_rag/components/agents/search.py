import logging
import os

from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper


class GoogleSeachOpenRag:
    """
    Initializes a tool for searching Google and retrieving top search results.

    This class provides functionality to search Google for recent results using the Google Search API Wrapper.

    Args:
        None

    Attributes:
        search (GoogleSearchAPIWrapper): An instance of GoogleSearchAPIWrapper used for making Google search queries.
        tool (Tool): An instance of Tool configured for searching Google.

    :raises ValueError: If the GOOGLE_CSE_ID environment variable is not set.
    """

    def __init__(self):
        """
        Initializes a GoogleSeachOpenRag instance.

        Raises:
            ValueError: If the GOOGLE_CSE_ID environment variable is not set.
        """
        if not os.getenv("GOOGLE_CSE_ID"):
            logging.error("GOOGLE_CSE_ID environment variable is not set")
            raise ValueError("GOOGLE_CSE_ID environment variable is not set")
        self.search = GoogleSearchAPIWrapper()
        self.tool = Tool(
            name="Google Search Snippets",
            description="Search Google for recent results.",
            func=self._top5_results,
        )

    def _top5_results(self, query: str) -> list[dict]:
        """
        Retrieves the top 5 search results from Google for the given query.

        :param query: The search query.
        :type query: str
        :return: A list of top 5 search results.
        :rtype: list[dict]
        """
        return self.search.results(query, 5)

    def init_tool(self) -> Tool:
        """
        Initializes the tool for searching Google.

        :return: An instance of Tool configured for Google search.
        :rtype: Tool
        """
        return self.tool


# print(tool.run("best grammar schools in UK?"))
