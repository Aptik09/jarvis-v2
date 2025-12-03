"""
Main AI Brain for JARVIS v2.0
Handles AI provider integration and response generation
"""

import openai
import anthropic
from typing import List, Dict, Optional, Generator
from config.settings import Settings
from config.prompts import SystemPrompts
from utils.logger import setup_logger

logger = setup_logger(__name__)


class Brain:
    """Main AI brain handling all AI operations"""

    def __init__(self, settings: Settings):
        """Initialize the AI brain"""
        self.settings = settings
        self.provider = settings.AI_PROVIDER

        # Initialize AI clients
        if self.provider == "openai":
            openai.api_key = settings.OPENAI_API_KEY
            self.model = settings.OPENAI_MODEL
        elif self.provider == "anthropic":
            self.anthropic_client = anthropic.Anthropic(
                api_key=settings.ANTHROPIC_API_KEY
            )
            self.model = settings.ANTHROPIC_MODEL

        # Get system prompt
        self.system_prompt = SystemPrompts.get_system_prompt(
            personality=settings.JARVIS_PERSONALITY,
            response_style=settings.RESPONSE_STYLE
        )

        logger.info(f"Brain initialized with provider: {self.provider}, model: {self.model}")

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Generate AI response
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            stream: Whether to stream the response
            max_tokens: Maximum tokens in response
            temperature: Response randomness (0-1)
            
        Returns:
            Generated response text
        """
        try:
            # Add system message
            full_messages = [
                {"role": "system", "content": self.system_prompt}
            ] + messages

            if self.provider == "openai":
                return self._generate_openai(
                    full_messages, stream, max_tokens, temperature
                )
            elif self.provider == "anthropic":
                return self._generate_anthropic(
                    full_messages, stream, max_tokens, temperature
                )
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return SystemPrompts.get_error_message()

    def _generate_openai(
        self,
        messages: List[Dict[str, str]],
        stream: bool,
        max_tokens: Optional[int],
        temperature: float
    ) -> str:
        """Generate response using OpenAI"""
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens or self.settings.MAX_TOKENS,
                temperature=temperature,
                stream=stream
            )

            if stream:
                # Handle streaming response
                full_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        yield content
                return full_response
            else:
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def _generate_anthropic(
        self,
        messages: List[Dict[str, str]],
        stream: bool,
        max_tokens: Optional[int],
        temperature: float
    ) -> str:
        """Generate response using Anthropic Claude"""
        try:
            # Extract system message
            system_msg = messages[0]["content"] if messages[0]["role"] == "system" else ""
            user_messages = messages[1:] if system_msg else messages

            response = self.anthropic_client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.settings.MAX_TOKENS,
                temperature=temperature,
                system=system_msg,
                messages=user_messages,
                stream=stream
            )

            if stream:
                # Handle streaming response
                full_response = ""
                for chunk in response:
                    if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                        content = chunk.delta.text
                        full_response += content
                        yield content
                return full_response
            else:
                return response.content[0].text

        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    def generate_streaming_response(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """
        Generate streaming AI response
        
        Args:
            messages: List of message dicts
            max_tokens: Maximum tokens
            temperature: Response randomness
            
        Yields:
            Response chunks
        """
        try:
            full_messages = [
                {"role": "system", "content": self.system_prompt}
            ] + messages

            if self.provider == "openai":
                yield from self._generate_openai(
                    full_messages, stream=True, max_tokens=max_tokens, temperature=temperature
                )
            elif self.provider == "anthropic":
                yield from self._generate_anthropic(
                    full_messages, stream=True, max_tokens=max_tokens, temperature=temperature
                )

        except Exception as e:
            logger.error(f"Error in streaming response: {e}")
            yield SystemPrompts.get_error_message()

    def analyze_intent(self, text: str) -> Dict[str, any]:
        """
        Analyze user intent from text
        
        Args:
            text: User input text
            
        Returns:
            Dict with intent analysis
        """
        try:
            prompt = f"""Analyze the following user input and determine:
1. Primary intent (question, command, conversation, etc.)
2. Required action (search, remember, schedule, calculate, etc.)
3. Entities mentioned (dates, names, locations, etc.)
4. Urgency level (low, medium, high)

User input: "{text}"

Respond in JSON format."""

            messages = [{"role": "user", "content": prompt}]
            response = self.generate_response(messages, temperature=0.3)

            # Parse JSON response
            import json
            return json.loads(response)

        except Exception as e:
            logger.error(f"Error analyzing intent: {e}")
            return {
                "intent": "unknown",
                "action": "respond",
                "entities": [],
                "urgency": "low"
            }

    def summarize_text(self, text: str, max_length: int = 100) -> str:
        """
        Summarize long text
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            
        Returns:
            Summarized text
        """
        try:
            prompt = f"""Summarize the following text in {max_length} words or less:

{text}

Summary:"""

            messages = [{"role": "user", "content": prompt}]
            return self.generate_response(messages, temperature=0.3)

        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return text[:max_length] + "..."

    def extract_keywords(self, text: str, count: int = 5) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            count: Number of keywords to extract
            
        Returns:
            List of keywords
        """
        try:
            prompt = f"""Extract the {count} most important keywords from this text.
Return only the keywords, comma-separated.

Text: {text}

Keywords:"""

            messages = [{"role": "user", "content": prompt}]
            response = self.generate_response(messages, temperature=0.3)
            return [kw.strip() for kw in response.split(",")]

        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []

    def __repr__(self) -> str:
        return f"<Brain provider={self.provider} model={self.model}>"
