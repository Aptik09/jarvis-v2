"""
News Skill for JARVIS v2.0
Provides news headlines and summaries
"""

import requests
from typing import Dict, Any, List
from skills.base_skill import BaseSkill
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class NewsSkill(BaseSkill):
    """Provides news headlines and summaries"""

    def __init__(self, settings: Settings):
        super().__init__(settings)
        # Using NewsAPI as example (free tier available)
        self.api_key = "demo"  # Users should get their own key

    def can_handle(self, intent_data: Dict) -> bool:
        """Check if this skill can handle the intent"""
        return "news" in intent_data.get("all_intents", [])

    def execute(
        self,
        category: str = "general",
        country: str = "us",
        count: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get news headlines
        
        Args:
            category: News category (general, business, technology, etc.)
            country: Country code (us, gb, etc.)
            count: Number of articles
            **kwargs: Additional parameters
            
        Returns:
            News articles
        """
        try:
            # Note: This is a demo implementation
            # Users should sign up for NewsAPI key
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": self.api_key,
                "category": category,
                "country": country,
                "pageSize": count
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 401:
                return self.create_response(
                    success=False,
                    error="News API key not configured. Please add NEWS_API_KEY to .env"
                )

            response.raise_for_status()
            data = response.json()

            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "source": article.get("source", {}).get("name"),
                    "published_at": article.get("publishedAt")
                })

            return self.create_response(
                success=True,
                data={"articles": articles, "count": len(articles)},
                message=f"Found {len(articles)} news articles"
            )

        except Exception as e:
            logger.error(f"News error: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to get news: {str(e)}"
            )

    def search_news(self, query: str, count: int = 5) -> Dict[str, Any]:
        """
        Search for news articles
        
        Args:
            query: Search query
            count: Number of articles
            
        Returns:
            News articles
        """
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "apiKey": self.api_key,
                "q": query,
                "pageSize": count,
                "sortBy": "publishedAt"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "source": article.get("source", {}).get("name"),
                    "published_at": article.get("publishedAt")
                })

            return self.create_response(
                success=True,
                data={"articles": articles, "count": len(articles)},
                message=f"Found {len(articles)} articles for '{query}'"
            )

        except Exception as e:
            logger.error(f"News search error: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to search news: {str(e)}"
            )
