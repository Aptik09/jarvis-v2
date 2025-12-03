"""
Settings and configuration management for JARVIS v2.0
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize settings"""
        if config_path:
            load_dotenv(config_path)

        # Project paths
        self.BASE_DIR = Path(__file__).parent.parent
        self.DATA_DIR = self.BASE_DIR / "data"
        self.LOGS_DIR = self.DATA_DIR / "logs"
        self.MEMORY_DIR = self.DATA_DIR / "memory"
        self.CONVERSATIONS_DIR = self.DATA_DIR / "conversations"
        self.SCHEDULES_DIR = self.DATA_DIR / "schedules"
        self.FILES_DIR = self.DATA_DIR / "files"

        # Create directories
        for directory in [
            self.DATA_DIR,
            self.LOGS_DIR,
            self.MEMORY_DIR,
            self.CONVERSATIONS_DIR,
            self.SCHEDULES_DIR,
            self.FILES_DIR,
        ]:
            directory.mkdir(parents=True, exist_ok=True)

        # AI Provider
        self.AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
        self.ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")

        # Search
        self.PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
        self.GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "")

        # Voice
        self.ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
        self.ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
        self.USE_LOCAL_TTS = os.getenv("USE_LOCAL_TTS", "true").lower() == "true"

        # Memory & Database
        self.CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(self.MEMORY_DIR))
        self.CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "jarvis_memory")
        self.MAX_MEMORY_ITEMS = int(os.getenv("MAX_MEMORY_ITEMS", "1000"))

        # Web Dashboard
        self.FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change-me-in-production")
        self.WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
        self.WEB_PORT = int(os.getenv("WEB_PORT", "5000"))
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_FILE = os.getenv("LOG_FILE", str(self.LOGS_DIR / "jarvis.log"))

        # Features
        self.ENABLE_VOICE = os.getenv("ENABLE_VOICE", "true").lower() == "true"
        self.ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"
        self.ENABLE_IMAGE_GEN = os.getenv("ENABLE_IMAGE_GEN", "true").lower() == "true"
        self.ENABLE_SCHEDULER = os.getenv("ENABLE_SCHEDULER", "true").lower() == "true"

        # Image Generation
        self.IMAGE_MODEL = os.getenv("IMAGE_MODEL", "dall-e-3")
        self.IMAGE_SIZE = os.getenv("IMAGE_SIZE", "1024x1024")
        self.IMAGE_QUALITY = os.getenv("IMAGE_QUALITY", "standard")

        # Scheduler
        self.SCHEDULER_CHECK_INTERVAL = int(os.getenv("SCHEDULER_CHECK_INTERVAL", "60"))
        self.TIMEZONE = os.getenv("TIMEZONE", "UTC")

        # Security
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))
        self.RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
        self.RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "3600"))

        # Performance
        self.CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
        self.MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))

        # User Preferences
        self.USER_NAME = os.getenv("USER_NAME", "User")
        self.JARVIS_PERSONALITY = os.getenv("JARVIS_PERSONALITY", "professional")
        self.RESPONSE_STYLE = os.getenv("RESPONSE_STYLE", "concise")

        # Notifications
        self.ENABLE_NOTIFICATIONS = os.getenv("ENABLE_NOTIFICATIONS", "true").lower() == "true"
        self.NOTIFICATION_SOUND = os.getenv("NOTIFICATION_SOUND", "true").lower() == "true"

        # Data Retention
        self.CONVERSATION_RETENTION_DAYS = int(os.getenv("CONVERSATION_RETENTION_DAYS", "30"))
        self.MEMORY_CLEANUP_ENABLED = os.getenv("MEMORY_CLEANUP_ENABLED", "true").lower() == "true"
        self.MEMORY_CLEANUP_INTERVAL = int(os.getenv("MEMORY_CLEANUP_INTERVAL", "86400"))

    def validate(self) -> bool:
        """Validate required settings"""
        errors = []

        # Check AI provider keys
        if self.AI_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when using OpenAI")
        elif self.AI_PROVIDER == "anthropic" and not self.ANTHROPIC_API_KEY:
            errors.append("ANTHROPIC_API_KEY is required when using Anthropic")

        if errors:
            for error in errors:
                print(f"Configuration Error: {error}")
            return False

        return True

    def __repr__(self) -> str:
        return f"<Settings provider={self.AI_PROVIDER} model={self.OPENAI_MODEL if self.AI_PROVIDER == 'openai' else self.ANTHROPIC_MODEL}>"
