"""
Calculator Skill for JARVIS v2.0
Performs mathematical calculations
"""

import math
import re
from typing import Dict, Any
from skills.base_skill import BaseSkill
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class CalculatorSkill(BaseSkill):
    """Performs mathematical calculations"""

    def __init__(self, settings: Settings):
        super().__init__(settings)

    def can_handle(self, intent_data: Dict) -> bool:
        """Check if this skill can handle the intent"""
        return "calculate" in intent_data.get("all_intents", [])

    def execute(self, expression: str, **kwargs) -> Dict[str, Any]:
        """
        Execute calculation
        
        Args:
            expression: Mathematical expression
            **kwargs: Additional parameters
            
        Returns:
            Calculation result
        """
        try:
            if not expression:
                return self.create_response(
                    success=False,
                    error="Expression is required"
                )

            # Clean expression
            expression = expression.strip()

            # Try to evaluate
            result = self._evaluate_expression(expression)

            if result is not None:
                return self.create_response(
                    success=True,
                    data={
                        "expression": expression,
                        "result": result
                    },
                    message=f"{expression} = {result}"
                )
            else:
                return self.create_response(
                    success=False,
                    error="Could not evaluate expression"
                )

        except Exception as e:
            logger.error(f"Calculation error: {e}")
            return self.create_response(
                success=False,
                error=f"Calculation failed: {str(e)}"
            )

    def _evaluate_expression(self, expression: str) -> float:
        """
        Safely evaluate mathematical expression
        
        Args:
            expression: Expression to evaluate
            
        Returns:
            Result or None
        """
        try:
            # Replace common words with operators
            expression = expression.lower()
            expression = expression.replace("plus", "+")
            expression = expression.replace("minus", "-")
            expression = expression.replace("times", "*")
            expression = expression.replace("multiplied by", "*")
            expression = expression.replace("divided by", "/")
            expression = expression.replace("to the power of", "**")
            expression = expression.replace("squared", "**2")
            expression = expression.replace("cubed", "**3")

            # Remove "what is" and similar phrases
            expression = re.sub(r'^(what is|calculate|compute)\s+', '', expression)

            # Create safe namespace with math functions
            safe_dict = {
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
                "sum": sum,
                "pow": pow,
                "sqrt": math.sqrt,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "log10": math.log10,
                "exp": math.exp,
                "pi": math.pi,
                "e": math.e,
            }

            # Evaluate expression
            result = eval(expression, {"__builtins__": {}}, safe_dict)

            # Round to reasonable precision
            if isinstance(result, float):
                result = round(result, 10)

            return result

        except Exception as e:
            logger.error(f"Expression evaluation error: {e}")
            return None

    def calculate_percentage(self, value: float, percentage: float) -> float:
        """Calculate percentage of a value"""
        return (value * percentage) / 100

    def calculate_compound_interest(
        self,
        principal: float,
        rate: float,
        time: float,
        n: int = 1
    ) -> float:
        """
        Calculate compound interest
        
        Args:
            principal: Principal amount
            rate: Interest rate (as percentage)
            time: Time period in years
            n: Number of times interest is compounded per year
            
        Returns:
            Final amount
        """
        rate = rate / 100  # Convert percentage to decimal
        amount = principal * (1 + rate / n) ** (n * time)
        return round(amount, 2)

    def calculate_bmi(self, weight_kg: float, height_m: float) -> Dict[str, Any]:
        """
        Calculate BMI (Body Mass Index)
        
        Args:
            weight_kg: Weight in kilograms
            height_m: Height in meters
            
        Returns:
            BMI and category
        """
        bmi = weight_kg / (height_m ** 2)
        bmi = round(bmi, 2)

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        return {
            "bmi": bmi,
            "category": category
        }
