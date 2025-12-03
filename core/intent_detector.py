"""
Intent Detection for JARVIS v2.0
Detects user intent and required actions
"""

import re
from typing import Dict, List, Optional
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)


class IntentDetector:
    """Detects user intent from input text"""

    # Intent patterns
    PATTERNS = {
        "search": [
            r"search (for|about|on)",
            r"look up",
            r"find (out|information|info)",
            r"what (is|are|was|were)",
            r"who (is|are|was|were)",
            r"when (is|are|was|were|did)",
            r"where (is|are|was|were)",
            r"how (to|do|does|did)",
            r"tell me about",
        ],
        "remember": [
            r"remember (that|this)",
            r"save (this|that)",
            r"store (this|that)",
            r"keep in mind",
            r"don't forget",
            r"note (that|this)",
            r"my .* is",
        ],
        "recall": [
            r"what (do you|did you) (know|remember)",
            r"recall",
            r"what did i (say|tell)",
            r"do you remember",
        ],
        "schedule": [
            r"remind me",
            r"set (a|an) (reminder|alarm)",
            r"schedule",
            r"at \d+",
            r"(tomorrow|today|tonight)",
            r"in \d+ (minutes|hours|days)",
        ],
        "calculate": [
            r"calculate",
            r"compute",
            r"what is \d+",
            r"\d+\s*[\+\-\*\/]\s*\d+",
        ],
        "image": [
            r"generate (an|a) image",
            r"create (an|a) (picture|image|photo)",
            r"draw",
            r"show me (a|an) image",
        ],
        "weather": [
            r"weather",
            r"temperature",
            r"forecast",
            r"how (hot|cold|warm)",
        ],
        "news": [
            r"news",
            r"headlines",
            r"what's happening",
            r"latest (on|about)",
        ],
        "file": [
            r"create (a|an) (file|document|pdf)",
            r"save (to|as) (file|document)",
            r"write to file",
        ],
    }

    def __init__(self):
        """Initialize intent detector"""
        logger.info("Intent detector initialized")

    def detect_intent(self, text: str) -> Dict:
        """
        Detect intent from text
        
        Args:
            text: User input text
            
        Returns:
            Dict with intent information
        """
        text_lower = text.lower()

        # Check each intent pattern
        detected_intents = []
        for intent, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    detected_intents.append(intent)
                    break

        # Determine primary intent
        primary_intent = detected_intents[0] if detected_intents else "conversation"

        # Extract entities
        entities = self._extract_entities(text)

        # Determine urgency
        urgency = self._determine_urgency(text_lower)

        result = {
            "primary_intent": primary_intent,
            "all_intents": detected_intents,
            "entities": entities,
            "urgency": urgency,
            "requires_action": primary_intent != "conversation",
        }

        logger.debug(f"Detected intent: {result}")
        return result

    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text"""
        entities = {
            "dates": [],
            "times": [],
            "numbers": [],
            "urls": [],
        }

        # Extract dates
        date_patterns = [
            r"(tomorrow|today|tonight|yesterday)",
            r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
            r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}",
        ]
        for pattern in date_patterns:
            matches = re.findall(pattern, text.lower())
            entities["dates"].extend(matches)

        # Extract times
        time_patterns = [
            r"\d{1,2}:\d{2}\s*(am|pm)?",
            r"\d{1,2}\s*(am|pm)",
            r"in \d+ (minutes|hours|days)",
        ]
        for pattern in time_patterns:
            matches = re.findall(pattern, text.lower())
            entities["times"].extend(matches)

        # Extract numbers
        numbers = re.findall(r"\d+(?:\.\d+)?", text)
        entities["numbers"] = numbers

        # Extract URLs
        urls = re.findall(r"https?://\S+", text)
        entities["urls"] = urls

        return entities

    def _determine_urgency(self, text: str) -> str:
        """Determine urgency level"""
        high_urgency_words = ["urgent", "asap", "immediately", "now", "emergency", "critical"]
        medium_urgency_words = ["soon", "today", "tonight", "quickly"]

        if any(word in text for word in high_urgency_words):
            return "high"
        elif any(word in text for word in medium_urgency_words):
            return "medium"
        else:
            return "low"

    def requires_search(self, intent_data: Dict) -> bool:
        """Check if intent requires web search"""
        return "search" in intent_data.get("all_intents", [])

    def requires_memory(self, intent_data: Dict) -> bool:
        """Check if intent requires memory operations"""
        return any(
            intent in intent_data.get("all_intents", [])
            for intent in ["remember", "recall"]
        )

    def requires_scheduling(self, intent_data: Dict) -> bool:
        """Check if intent requires scheduling"""
        return "schedule" in intent_data.get("all_intents", [])

    def __repr__(self) -> str:
        return "<IntentDetector>"
