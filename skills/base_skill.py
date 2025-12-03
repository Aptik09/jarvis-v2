"""
Base Skill class for JARVIS v2.0
All skills inherit from this base class
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseSkill(ABC):
    """Base class for all JARVIS skills"""

    def __init__(self, settings: Settings):
        """
        Initialize skill
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.name = self.__class__.__name__
        self.enabled = True
        logger.debug(f"Skill initialized: {self.name}")

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the skill
        
        Args:
            **kwargs: Skill-specific parameters
            
        Returns:
            Result dictionary with 'success' and 'data' keys
        """
        pass

    @abstractmethod
    def can_handle(self, intent_data: Dict) -> bool:
        """
        Check if skill can handle the intent
        
        Args:
            intent_data: Intent detection data
            
        Returns:
            True if skill can handle the intent
        """
        pass

    def get_description(self) -> str:
        """
        Get skill description
        
        Returns:
            Skill description
        """
        return self.__doc__ or f"{self.name} skill"

    def validate_params(self, required_params: list, provided_params: Dict) -> bool:
        """
        Validate required parameters
        
        Args:
            required_params: List of required parameter names
            provided_params: Provided parameters dict
            
        Returns:
            True if all required params present
        """
        for param in required_params:
            if param not in provided_params or provided_params[param] is None:
                logger.warning(f"Missing required parameter: {param}")
                return False
        return True

    def create_response(
        self,
        success: bool,
        data: Any = None,
        message: Optional[str] = None,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create standardized response
        
        Args:
            success: Success status
            data: Response data
            message: Success message
            error: Error message
            
        Returns:
            Response dictionary
        """
        response = {
            "success": success,
            "skill": self.name,
        }

        if data is not None:
            response["data"] = data

        if message:
            response["message"] = message

        if error:
            response["error"] = error

        return response

    def __repr__(self) -> str:
        return f"<{self.name} enabled={self.enabled}>"
