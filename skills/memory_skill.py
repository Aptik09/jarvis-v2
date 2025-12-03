"""
Memory Skill for JARVIS v2.0
Handles memory storage and retrieval operations
"""

from typing import Dict, Any
from skills.base_skill import BaseSkill
from core.memory import MemorySystem
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MemorySkill(BaseSkill):
    """Handles memory storage and retrieval"""

    def __init__(self, settings: Settings, memory_system: MemorySystem):
        super().__init__(settings)
        self.memory = memory_system

    def can_handle(self, intent_data: Dict) -> bool:
        """Check if this skill can handle the intent"""
        intents = intent_data.get("all_intents", [])
        return "remember" in intents or "recall" in intents

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute memory action
        
        Args:
            action: Action to perform (store, retrieve, stats)
            **kwargs: Action parameters
            
        Returns:
            Action result
        """
        try:
            if action == "store":
                return self.store_memory(**kwargs)
            elif action == "retrieve":
                return self.retrieve_memory(**kwargs)
            elif action == "stats":
                return self.get_stats()
            else:
                return self.create_response(
                    success=False,
                    error=f"Unknown action: {action}"
                )

        except Exception as e:
            logger.error(f"Memory execution error: {e}")
            return self.create_response(
                success=False,
                error=f"Memory operation failed: {str(e)}"
            )

    def store_memory(
        self,
        content: str,
        memory_type: str = "fact",
        metadata: Dict = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Store a memory
        
        Args:
            content: Memory content
            memory_type: Type of memory (fact, preference, etc.)
            metadata: Additional metadata
            
        Returns:
            Storage result
        """
        try:
            if not content:
                return self.create_response(
                    success=False,
                    error="Memory content is required"
                )

            memory_id = self.memory.store(
                content=content,
                metadata=metadata,
                memory_type=memory_type
            )

            return self.create_response(
                success=True,
                data={"memory_id": memory_id, "content": content},
                message="Memory stored successfully"
            )

        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to store memory: {str(e)}"
            )

    def retrieve_memory(
        self,
        query: str,
        n_results: int = 5,
        memory_type: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Retrieve memories
        
        Args:
            query: Search query
            n_results: Number of results
            memory_type: Filter by memory type
            
        Returns:
            Retrieved memories
        """
        try:
            if not query:
                return self.create_response(
                    success=False,
                    error="Search query is required"
                )

            memories = self.memory.retrieve(
                query=query,
                n_results=n_results,
                memory_type=memory_type
            )

            return self.create_response(
                success=True,
                data={"memories": memories, "count": len(memories)},
                message=f"Found {len(memories)} relevant memory/memories"
            )

        except Exception as e:
            logger.error(f"Error retrieving memories: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to retrieve memories: {str(e)}"
            )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics
        
        Returns:
            Memory stats
        """
        try:
            stats = self.memory.get_memory_stats()

            return self.create_response(
                success=True,
                data=stats,
                message="Memory statistics retrieved"
            )

        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to get memory stats: {str(e)}"
            )
