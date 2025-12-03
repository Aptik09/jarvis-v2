"""
Web Search Skill for JARVIS v2.0
Performs web searches using various search APIs
"""

import requests
from typing import Dict, Any, List
from skills.base_skill import BaseSkill
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SearchSkill(BaseSkill):
    """Performs web searches and returns relevant information"""

    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.perplexity_key = settings.PERPLEXITY_API_KEY
        self.google_key = settings.GOOGLE_API_KEY
        self.google_cse_id = settings.GOOGLE_CSE_ID

    def can_handle(self, intent_data: Dict) -> bool:
        """Check if this skill can handle the intent"""
        return "search" in intent_data.get("all_intents", [])

    def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute web search
        
        Args:
            query: Search query
            **kwargs: Additional parameters
            
        Returns:
            Search results
        """
        try:
            if not query:
                return self.create_response(
                    success=False,
                    error="Search query is required"
                )

            # Try Perplexity first if available
            if self.perplexity_key:
                results = self._search_perplexity(query)
                if results:
                    return self.create_response(
                        success=True,
                        data=results,
                        message="Search completed successfully"
                    )

            # Fallback to Google if available
            if self.google_key and self.google_cse_id:
                results = self._search_google(query)
                if results:
                    return self.create_response(
                        success=True,
                        data=results,
                        message="Search completed successfully"
                    )

            # Fallback to DuckDuckGo (no API key required)
            results = self._search_duckduckgo(query)
            return self.create_response(
                success=True,
                data=results,
                message="Search completed successfully"
            )

        except Exception as e:
            logger.error(f"Search error: {e}")
            return self.create_response(
                success=False,
                error=f"Search failed: {str(e)}"
            )

    def _search_perplexity(self, query: str) -> Dict[str, Any]:
        """Search using Perplexity API"""
        try:
            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.perplexity_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "sonar-small-online",
                "messages": [
                    {"role": "user", "content": query}
                ]
            }

            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()

            result = response.json()
            answer = result["choices"][0]["message"]["content"]

            return {
                "answer": answer,
                "source": "perplexity",
                "query": query
            }

        except Exception as e:
            logger.error(f"Perplexity search error: {e}")
            return None

    def _search_google(self, query: str) -> Dict[str, Any]:
        """Search using Google Custom Search API"""
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.google_key,
                "cx": self.google_cse_id,
                "q": query,
                "num": 5
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            result = response.json()
            items = result.get("items", [])

            results = []
            for item in items:
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                })

            return {
                "results": results,
                "source": "google",
                "query": query
            }

        except Exception as e:
            logger.error(f"Google search error: {e}")
            return None

    def _search_duckduckgo(self, query: str) -> Dict[str, Any]:
        """Search using DuckDuckGo (no API key required)"""
        try:
            from duckduckgo_search import DDGS

            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))

            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.get("title"),
                    "link": result.get("href"),
                    "snippet": result.get("body")
                })

            return {
                "results": formatted_results,
                "source": "duckduckgo",
                "query": query
            }

        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return {
                "results": [],
                "source": "duckduckgo",
                "query": query,
                "note": "Search completed with limited results"
            }
