"""
API Keys management for JARVIS v2.0
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class APIKeys:
    """Centralized API key management"""

    @staticmethod
    def get_openai_key() -> Optional[str]:
        """Get OpenAI API key"""
        return os.getenv("OPENAI_API_KEY")

    @staticmethod
    def get_anthropic_key() -> Optional[str]:
        """Get Anthropic API key"""
        return os.getenv("ANTHROPIC_API_KEY")

    @staticmethod
    def get_perplexity_key() -> Optional[str]:
        """Get Perplexity API key"""
        return os.getenv("PERPLEXITY_API_KEY")

    @staticmethod
    def get_google_key() -> Optional[str]:
        """Get Google API key"""
        return os.getenv("GOOGLE_API_KEY")

    @staticmethod
    def get_elevenlabs_key() -> Optional[str]:
        """Get ElevenLabs API key"""
        return os.getenv("ELEVENLABS_API_KEY")

    @staticmethod
    def validate_keys(provider: str) -> bool:
        """Validate required API keys for a provider"""
        if provider == "openai":
            return bool(APIKeys.get_openai_key())
        elif provider == "anthropic":
            return bool(APIKeys.get_anthropic_key())
        return True

    @staticmethod
    def mask_key(key: str) -> str:
        """Mask API key for display"""
        if not key or len(key) < 8:
            return "****"
        return f"{key[:4]}...{key[-4:]}"
