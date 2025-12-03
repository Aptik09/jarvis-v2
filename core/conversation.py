"""
Conversation Manager for JARVIS v2.0
Handles conversation history and context
"""

from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ConversationManager:
    """Manages conversation history and context"""

    def __init__(self, settings: Settings):
        """Initialize conversation manager"""
        self.settings = settings
        self.conversations_dir = settings.CONVERSATIONS_DIR
        self.current_conversation: List[Dict[str, str]] = []
        self.conversation_id = self._generate_conversation_id()

        logger.info(f"Conversation manager initialized: {self.conversation_id}")

    def _generate_conversation_id(self) -> str:
        """Generate unique conversation ID"""
        return f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def add_message(self, role: str, content: str) -> None:
        """
        Add message to conversation
        
        Args:
            role: Message role (user/assistant)
            content: Message content
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.current_conversation.append(message)
        logger.debug(f"Added {role} message to conversation")

    def get_messages(
        self,
        limit: Optional[int] = None,
        include_system: bool = False
    ) -> List[Dict[str, str]]:
        """
        Get conversation messages
        
        Args:
            limit: Maximum number of messages to return
            include_system: Whether to include system messages
            
        Returns:
            List of messages
        """
        messages = self.current_conversation.copy()

        if not include_system:
            messages = [m for m in messages if m["role"] != "system"]

        if limit:
            messages = messages[-limit:]

        return messages

    def get_context_messages(self, max_tokens: int = 2000) -> List[Dict[str, str]]:
        """
        Get messages that fit within token limit
        
        Args:
            max_tokens: Maximum tokens for context
            
        Returns:
            List of messages within token limit
        """
        # Simple approximation: 4 chars ≈ 1 token
        max_chars = max_tokens * 4
        total_chars = 0
        context_messages = []

        # Add messages from most recent, working backwards
        for message in reversed(self.current_conversation):
            message_chars = len(message["content"])
            if total_chars + message_chars > max_chars:
                break
            context_messages.insert(0, message)
            total_chars += message_chars

        return context_messages

    def clear_conversation(self) -> None:
        """Clear current conversation"""
        self.current_conversation = []
        self.conversation_id = self._generate_conversation_id()
        logger.info("Conversation cleared")

    def save_conversation(self, filename: Optional[str] = None) -> str:
        """
        Save conversation to file
        
        Args:
            filename: Optional custom filename
            
        Returns:
            Path to saved file
        """
        try:
            if not filename:
                filename = f"{self.conversation_id}.json"

            filepath = self.conversations_dir / filename

            conversation_data = {
                "id": self.conversation_id,
                "created_at": self.current_conversation[0]["timestamp"] if self.current_conversation else datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "message_count": len(self.current_conversation),
                "messages": self.current_conversation
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Conversation saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            raise

    def load_conversation(self, filename: str) -> bool:
        """
        Load conversation from file
        
        Args:
            filename: Filename to load
            
        Returns:
            Success status
        """
        try:
            filepath = self.conversations_dir / filename

            if not filepath.exists():
                logger.error(f"Conversation file not found: {filepath}")
                return False

            with open(filepath, 'r', encoding='utf-8') as f:
                conversation_data = json.load(f)

            self.conversation_id = conversation_data.get("id", self._generate_conversation_id())
            self.current_conversation = conversation_data.get("messages", [])

            logger.info(f"Conversation loaded: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error loading conversation: {e}")
            return False

    def list_conversations(self) -> List[Dict]:
        """
        List all saved conversations
        
        Returns:
            List of conversation metadata
        """
        try:
            conversations = []

            for filepath in self.conversations_dir.glob("*.json"):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    conversations.append({
                        "id": data.get("id"),
                        "filename": filepath.name,
                        "created_at": data.get("created_at"),
                        "updated_at": data.get("updated_at"),
                        "message_count": data.get("message_count", 0)
                    })
                except Exception as e:
                    logger.warning(f"Error reading conversation file {filepath}: {e}")

            # Sort by updated_at (most recent first)
            conversations.sort(key=lambda x: x.get("updated_at", ""), reverse=True)

            return conversations

        except Exception as e:
            logger.error(f"Error listing conversations: {e}")
            return []

    def get_conversation_summary(self) -> str:
        """
        Get summary of current conversation
        
        Returns:
            Conversation summary
        """
        if not self.current_conversation:
            return "No messages in current conversation"

        message_count = len(self.current_conversation)
        user_messages = len([m for m in self.current_conversation if m["role"] == "user"])
        assistant_messages = len([m for m in self.current_conversation if m["role"] == "assistant"])

        return f"Conversation {self.conversation_id}: {message_count} messages ({user_messages} user, {assistant_messages} assistant)"

    def __repr__(self) -> str:
        return f"<ConversationManager id={self.conversation_id} messages={len(self.current_conversation)}>"
