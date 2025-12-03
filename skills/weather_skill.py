"""
Weather Skill for JARVIS v2.0
Provides weather information
"""

import requests
from typing import Dict, Any
from skills.base_skill import BaseSkill
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class WeatherSkill(BaseSkill):
    """Provides weather information"""

    def __init__(self, settings: Settings):
        super().__init__(settings)
        # Using OpenWeatherMap as example (free tier available)
        self.api_key = "demo"  # Users should get their own key

    def can_handle(self, intent_data: Dict) -> bool:
        """Check if this skill can handle the intent"""
        return "weather" in intent_data.get("all_intents", [])

    def execute(self, location: str = "London", **kwargs) -> Dict[str, Any]:
        """
        Get weather information
        
        Args:
            location: Location name
            **kwargs: Additional parameters
            
        Returns:
            Weather information
        """
        try:
            # Note: This is a demo implementation
            # Users should sign up for OpenWeatherMap API key
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 401:
                return self.create_response(
                    success=False,
                    error="Weather API key not configured. Please add OPENWEATHER_API_KEY to .env"
                )

            response.raise_for_status()
            data = response.json()

            weather_info = {
                "location": data["name"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }

            message = f"Weather in {weather_info['location']}: {weather_info['temperature']}°C, {weather_info['description']}"

            return self.create_response(
                success=True,
                data=weather_info,
                message=message
            )

        except Exception as e:
            logger.error(f"Weather error: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to get weather: {str(e)}"
            )
