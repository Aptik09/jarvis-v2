"""
Tests for Memory System
"""

import pytest
from config.settings import Settings
from core.memory import MemorySystem


@pytest.fixture
def settings():
    """Create test settings"""
    return Settings()


@pytest.fixture
def memory(settings):
    """Create memory system instance"""
    return MemorySystem(settings)


def test_memory_initialization(memory):
    """Test memory system initialization"""
    assert memory is not None
    assert memory.collection is not None


def test_store_memory(memory):
    """Test storing a memory"""
    memory_id = memory.store(
        content="Test memory content",
        memory_type="test"
    )
    
    assert memory_id is not None
    assert isinstance(memory_id, str)


def test_retrieve_memory(memory):
    """Test retrieving memories"""
    # Store a memory first
    memory.store(
        content="Python is a programming language",
        memory_type="fact"
    )
    
    # Retrieve it
    results = memory.retrieve(
        query="Python programming",
        n_results=5
    )
    
    assert results is not None
    assert isinstance(results, list)


def test_store_conversation(memory):
    """Test storing conversation"""
    memory_id = memory.store_conversation(
        user_message="Hello",
        assistant_message="Hi! How can I help?"
    )
    
    assert memory_id is not None


def test_store_fact(memory):
    """Test storing a fact"""
    memory_id = memory.store_fact(
        fact="The Earth orbits the Sun",
        category="astronomy"
    )
    
    assert memory_id is not None


def test_store_preference(memory):
    """Test storing a preference"""
    memory_id = memory.store_preference(
        preference="Favorite color is blue",
        key="color"
    )
    
    assert memory_id is not None


def test_get_memory_stats(memory):
    """Test getting memory statistics"""
    stats = memory.get_memory_stats()
    
    assert stats is not None
    assert isinstance(stats, dict)
    assert "total_memories" in stats


def test_memory_repr(memory):
    """Test memory string representation"""
    repr_str = repr(memory)
    assert "MemorySystem" in repr_str
