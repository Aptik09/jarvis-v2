"""
Vector Memory System for JARVIS v2.0
Uses ChromaDB for semantic memory storage and retrieval
"""

import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional
from datetime import datetime
import json
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MemorySystem:
    """Vector-based memory system using ChromaDB"""

    def __init__(self, settings: Settings):
        """Initialize memory system"""
        self.settings = settings

        # Initialize ChromaDB
        self.client = chromadb.Client(ChromaSettings(
            persist_directory=settings.CHROMA_PERSIST_DIR,
            anonymized_telemetry=False
        ))

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"description": "JARVIS memory storage"}
        )

        logger.info(f"Memory system initialized with {self.collection.count()} memories")

    def store(
        self,
        content: str,
        metadata: Optional[Dict] = None,
        memory_type: str = "conversation"
    ) -> str:
        """
        Store a memory
        
        Args:
            content: Memory content
            metadata: Additional metadata
            memory_type: Type of memory (conversation, fact, preference, etc.)
            
        Returns:
            Memory ID
        """
        try:
            # Generate unique ID
            memory_id = f"{memory_type}_{datetime.now().timestamp()}"

            # Prepare metadata
            meta = {
                "type": memory_type,
                "timestamp": datetime.now().isoformat(),
                **(metadata or {})
            }

            # Store in ChromaDB
            self.collection.add(
                documents=[content],
                metadatas=[meta],
                ids=[memory_id]
            )

            logger.debug(f"Stored memory: {memory_id}")
            return memory_id

        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            raise

    def retrieve(
        self,
        query: str,
        n_results: int = 5,
        memory_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve relevant memories
        
        Args:
            query: Search query
            n_results: Number of results to return
            memory_type: Filter by memory type
            
        Returns:
            List of relevant memories
        """
        try:
            # Build where clause
            where = {"type": memory_type} if memory_type else None

            # Query ChromaDB
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where
            )

            # Format results
            memories = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    memories.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0,
                        "id": results['ids'][0][i] if results['ids'] else None
                    })

            logger.debug(f"Retrieved {len(memories)} memories for query: {query}")
            return memories

        except Exception as e:
            logger.error(f"Error retrieving memories: {e}")
            return []

    def store_conversation(self, user_message: str, assistant_message: str) -> str:
        """
        Store a conversation exchange
        
        Args:
            user_message: User's message
            assistant_message: Assistant's response
            
        Returns:
            Memory ID
        """
        content = f"User: {user_message}\nAssistant: {assistant_message}"
        metadata = {
            "user_message": user_message,
            "assistant_message": assistant_message
        }
        return self.store(content, metadata, memory_type="conversation")

    def store_fact(self, fact: str, category: Optional[str] = None) -> str:
        """
        Store a fact
        
        Args:
            fact: Fact to store
            category: Fact category
            
        Returns:
            Memory ID
        """
        metadata = {"category": category} if category else {}
        return self.store(fact, metadata, memory_type="fact")

    def store_preference(self, preference: str, key: Optional[str] = None) -> str:
        """
        Store a user preference
        
        Args:
            preference: Preference description
            key: Preference key
            
        Returns:
            Memory ID
        """
        metadata = {"key": key} if key else {}
        return self.store(preference, metadata, memory_type="preference")

    def get_recent_conversations(self, count: int = 10) -> List[Dict]:
        """
        Get recent conversations
        
        Args:
            count: Number of conversations to retrieve
            
        Returns:
            List of recent conversations
        """
        try:
            results = self.collection.get(
                where={"type": "conversation"},
                limit=count
            )

            conversations = []
            if results['documents']:
                for i, doc in enumerate(results['documents']):
                    conversations.append({
                        "content": doc,
                        "metadata": results['metadatas'][i] if results['metadatas'] else {},
                        "id": results['ids'][i] if results['ids'] else None
                    })

            # Sort by timestamp (most recent first)
            conversations.sort(
                key=lambda x: x['metadata'].get('timestamp', ''),
                reverse=True
            )

            return conversations[:count]

        except Exception as e:
            logger.error(f"Error getting recent conversations: {e}")
            return []

    def search_facts(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for facts"""
        return self.retrieve(query, n_results, memory_type="fact")

    def search_preferences(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for preferences"""
        return self.retrieve(query, n_results, memory_type="preference")

    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory
        
        Args:
            memory_id: ID of memory to delete
            
        Returns:
            Success status
        """
        try:
            self.collection.delete(ids=[memory_id])
            logger.debug(f"Deleted memory: {memory_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting memory: {e}")
            return False

    def clear_old_memories(self, days: int = 30) -> int:
        """
        Clear memories older than specified days
        
        Args:
            days: Age threshold in days
            
        Returns:
            Number of memories deleted
        """
        try:
            from datetime import timedelta
            cutoff_date = datetime.now() - timedelta(days=days)

            # Get all memories
            all_memories = self.collection.get()
            deleted_count = 0

            if all_memories['metadatas']:
                for i, metadata in enumerate(all_memories['metadatas']):
                    timestamp_str = metadata.get('timestamp', '')
                    if timestamp_str:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        if timestamp < cutoff_date:
                            memory_id = all_memories['ids'][i]
                            self.delete_memory(memory_id)
                            deleted_count += 1

            logger.info(f"Cleared {deleted_count} old memories")
            return deleted_count

        except Exception as e:
            logger.error(f"Error clearing old memories: {e}")
            return 0

    def get_memory_stats(self) -> Dict:
        """Get memory statistics"""
        try:
            total_count = self.collection.count()

            # Count by type
            type_counts = {}
            all_memories = self.collection.get()

            if all_memories['metadatas']:
                for metadata in all_memories['metadatas']:
                    mem_type = metadata.get('type', 'unknown')
                    type_counts[mem_type] = type_counts.get(mem_type, 0) + 1

            return {
                "total_memories": total_count,
                "by_type": type_counts,
                "collection_name": self.settings.CHROMA_COLLECTION_NAME
            }

        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {"total_memories": 0, "by_type": {}}

    def __repr__(self) -> str:
        return f"<MemorySystem memories={self.collection.count()}>"
