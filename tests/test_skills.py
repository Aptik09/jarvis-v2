"""
Tests for Skills
"""

import pytest
from config.settings import Settings
from core.memory import MemorySystem
from skills.calculator_skill import CalculatorSkill
from skills.memory_skill import MemorySkill
from skills.search_skill import SearchSkill


@pytest.fixture
def settings():
    """Create test settings"""
    return Settings()


@pytest.fixture
def memory_system(settings):
    """Create memory system"""
    return MemorySystem(settings)


class TestCalculatorSkill:
    """Tests for Calculator Skill"""
    
    def test_initialization(self, settings):
        """Test skill initialization"""
        skill = CalculatorSkill(settings)
        assert skill is not None
        assert skill.name == "CalculatorSkill"
    
    def test_simple_calculation(self, settings):
        """Test simple calculation"""
        skill = CalculatorSkill(settings)
        result = skill.execute(expression="2 + 2")
        
        assert result["success"] is True
        assert result["data"]["result"] == 4
    
    def test_complex_calculation(self, settings):
        """Test complex calculation"""
        skill = CalculatorSkill(settings)
        result = skill.execute(expression="(10 + 5) * 2")
        
        assert result["success"] is True
        assert result["data"]["result"] == 30
    
    def test_invalid_expression(self, settings):
        """Test invalid expression"""
        skill = CalculatorSkill(settings)
        result = skill.execute(expression="invalid")
        
        assert result["success"] is False
    
    def test_can_handle(self, settings):
        """Test intent handling"""
        skill = CalculatorSkill(settings)
        intent_data = {"all_intents": ["calculate"]}
        
        assert skill.can_handle(intent_data) is True


class TestMemorySkill:
    """Tests for Memory Skill"""
    
    def test_initialization(self, settings, memory_system):
        """Test skill initialization"""
        skill = MemorySkill(settings, memory_system)
        assert skill is not None
    
    def test_store_memory(self, settings, memory_system):
        """Test storing memory"""
        skill = MemorySkill(settings, memory_system)
        result = skill.execute(
            action="store",
            content="Test memory",
            memory_type="test"
        )
        
        assert result["success"] is True
        assert "memory_id" in result["data"]
    
    def test_retrieve_memory(self, settings, memory_system):
        """Test retrieving memory"""
        skill = MemorySkill(settings, memory_system)
        
        # Store first
        skill.execute(
            action="store",
            content="Python is great",
            memory_type="fact"
        )
        
        # Retrieve
        result = skill.execute(
            action="retrieve",
            query="Python",
            n_results=5
        )
        
        assert result["success"] is True
        assert "memories" in result["data"]
    
    def test_get_stats(self, settings, memory_system):
        """Test getting stats"""
        skill = MemorySkill(settings, memory_system)
        result = skill.execute(action="stats")
        
        assert result["success"] is True
        assert "total_memories" in result["data"]


class TestSearchSkill:
    """Tests for Search Skill"""
    
    def test_initialization(self, settings):
        """Test skill initialization"""
        skill = SearchSkill(settings)
        assert skill is not None
    
    def test_can_handle(self, settings):
        """Test intent handling"""
        skill = SearchSkill(settings)
        intent_data = {"all_intents": ["search"]}
        
        assert skill.can_handle(intent_data) is True
    
    def test_empty_query(self, settings):
        """Test empty query"""
        skill = SearchSkill(settings)
        result = skill.execute(query="")
        
        assert result["success"] is False
