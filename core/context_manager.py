"""
Context Manager for JARVIS v2.0
Manages conversation context and state
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContextManager:
    """Manages conversation context and state"""

    def __init__(self):
        """Initialize context manager"""
        self.context: Dict[str, Any] = {
            "user_info": {},
            "session_data": {},
            "temporary_data": {},
            "last_intent": None,
            "last_action": None,
            "conversation_topic": None,
        }
        self.session_start = datetime.now()
        logger.info("Context manager initialized")

    def set_user_info(self, key: str, value: Any) -> None:
        """
        Set user information
        
        Args:
            key: Information key
            value: Information value
        """
        self.context["user_info"][key] = value
        logger.debug(f"Set user info: {key}")

    def get_user_info(self, key: str, default: Any = None) -> Any:
        """
        Get user information
        
        Args:
            key: Information key
            default: Default value if key not found
            
        Returns:
            User information value
        """
        return self.context["user_info"].get(key, default)

    def set_session_data(self, key: str, value: Any) -> None:
        """
        Set session data
        
        Args:
            key: Data key
            value: Data value
        """
        self.context["session_data"][key] = value
        logger.debug(f"Set session data: {key}")

    def get_session_data(self, key: str, default: Any = None) -> Any:
        """
        Get session data
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Session data value
        """
        return self.context["session_data"].get(key, default)

    def set_temporary_data(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set temporary data with optional TTL
        
        Args:
            key: Data key
            value: Data value
            ttl: Time to live in seconds (optional)
        """
        self.context["temporary_data"][key] = {
            "value": value,
            "timestamp": datetime.now(),
            "ttl": ttl
        }
        logger.debug(f"Set temporary data: {key}")

    def get_temporary_data(self, key: str, default: Any = None) -> Any:
        """
        Get temporary data
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Temporary data value
        """
        if key not in self.context["temporary_data"]:
            return default

        data = self.context["temporary_data"][key]

        # Check TTL
        if data.get("ttl"):
            elapsed = (datetime.now() - data["timestamp"]).total_seconds()
            if elapsed > data["ttl"]:
                del self.context["temporary_data"][key]
                return default

        return data["value"]

    def update_intent(self, intent: str) -> None:
        """Update last detected intent"""
        self.context["last_intent"] = intent
        logger.debug(f"Updated intent: {intent}")

    def update_action(self, action: str) -> None:
        """Update last performed action"""
        self.context["last_action"] = action
        logger.debug(f"Updated action: {action}")

    def update_topic(self, topic: str) -> None:
        """Update conversation topic"""
        self.context["conversation_topic"] = topic
        logger.debug(f"Updated topic: {topic}")

    def get_context_summary(self) -> Dict[str, Any]:
        """
        Get context summary
        
        Returns:
            Context summary dict
        """
        session_duration = (datetime.now() - self.session_start).total_seconds()

        return {
            "session_duration_seconds": session_duration,
            "user_info_keys": list(self.context["user_info"].keys()),
            "session_data_keys": list(self.context["session_data"].keys()),
            "temporary_data_keys": list(self.context["temporary_data"].keys()),
            "last_intent": self.context["last_intent"],
            "last_action": self.context["last_action"],
            "conversation_topic": self.context["conversation_topic"],
        }

    def clear_temporary_data(self) -> None:
        """Clear all temporary data"""
        self.context["temporary_data"] = {}
        logger.info("Cleared temporary data")

    def clear_session_data(self) -> None:
        """Clear session data"""
        self.context["session_data"] = {}
        logger.info("Cleared session data")

    def reset_context(self) -> None:
        """Reset entire context"""
        self.context = {
            "user_info": {},
            "session_data": {},
            "temporary_data": {},
            "last_intent": None,
            "last_action": None,
            "conversation_topic": None,
        }
        self.session_start = datetime.now()
        logger.info("Context reset")

    def __repr__(self) -> str:
        return f"<ContextManager session_duration={(datetime.now() - self.session_start).total_seconds()}s>"
