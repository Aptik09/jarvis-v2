"""
CLI Interface for JARVIS v2.0
Beautiful command-line interface with colors and formatting
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from typing import Optional
from config.settings import Settings
from config.prompts import SystemPrompts
from core.brain import Brain
from core.memory import MemorySystem
from core.conversation import ConversationManager
from core.intent_detector import IntentDetector
from core.context_manager import ContextManager
from skills import *
from utils.logger import setup_logger

logger = setup_logger(__name__)
console = Console()


class CLIInterface:
    """Command-line interface for JARVIS"""

    def __init__(self, settings: Settings):
        """Initialize CLI interface"""
        self.settings = settings
        self.console = console

        # Initialize core components
        self.brain = Brain(settings)
        self.memory = MemorySystem(settings)
        self.conversation = ConversationManager(settings)
        self.intent_detector = IntentDetector()
        self.context = ContextManager()

        # Initialize skills
        self.skills = {
            "search": SearchSkill(settings),
            "schedule": ScheduleSkill(settings),
            "memory": MemorySkill(settings, self.memory),
            "file": FileSkill(settings),
            "image": ImageSkill(settings),
            "weather": WeatherSkill(settings),
            "news": NewsSkill(settings),
            "calculator": CalculatorSkill(settings),
        }

        logger.info("CLI interface initialized")

    def run(self):
        """Run the CLI interface"""
        try:
            # Welcome message
            self.console.print(Panel(
                SystemPrompts.get_conversation_starter(),
                title="JARVIS v2.0",
                style="bold cyan"
            ))

            # Main loop
            while True:
                try:
                    # Get user input
                    user_input = Prompt.ask("\n[bold green]You[/bold green]")

                    # Check for exit commands
                    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                        self.console.print("[yellow]Goodbye! Have a great day![/yellow]")
                        break

                    # Check for special commands
                    if user_input.startswith("/"):
                        self.handle_command(user_input)
                        continue

                    # Process input
                    response = self.process_input(user_input)

                    # Display response
                    self.display_response(response)

                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Use 'exit' to quit[/yellow]")
                    continue

        except Exception as e:
            logger.error(f"CLI error: {e}")
            self.console.print(f"[red]Error: {e}[/red]")

    def process_input(self, user_input: str) -> str:
        """
        Process user input
        
        Args:
            user_input: User's message
            
        Returns:
            Response text
        """
        try:
            # Add to conversation
            self.conversation.add_message("user", user_input)

            # Detect intent
            intent_data = self.intent_detector.detect_intent(user_input)
            self.context.update_intent(intent_data["primary_intent"])

            # Check if any skill can handle this
            skill_response = None
            for skill_name, skill in self.skills.items():
                if skill.can_handle(intent_data):
                    logger.info(f"Skill {skill_name} handling request")
                    # Execute skill based on intent
                    if skill_name == "search":
                        skill_response = skill.execute(query=user_input)
                    elif skill_name == "calculator":
                        skill_response = skill.execute(expression=user_input)
                    # Add more skill-specific handling as needed
                    break

            # Get AI response
            messages = self.conversation.get_context_messages()

            # Add skill response to context if available
            if skill_response and skill_response.get("success"):
                skill_context = f"Skill result: {skill_response.get('message', '')}"
                messages.append({"role": "system", "content": skill_context})

            # Generate response
            with Live(Spinner("dots", text="Thinking..."), console=self.console):
                response = self.brain.generate_response(messages)

            # Add to conversation
            self.conversation.add_message("assistant", response)

            # Store in memory
            self.memory.store_conversation(user_input, response)

            return response

        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return SystemPrompts.get_error_message()

    def display_response(self, response: str):
        """
        Display response with formatting
        
        Args:
            response: Response text
        """
        self.console.print(Panel(
            Markdown(response),
            title="JARVIS",
            style="bold blue"
        ))

    def handle_command(self, command: str):
        """
        Handle special commands
        
        Args:
            command: Command string
        """
        cmd = command.lower().strip()

        if cmd == "/help":
            self.show_help()
        elif cmd == "/clear":
            self.conversation.clear_conversation()
            self.console.print("[green]Conversation cleared[/green]")
        elif cmd == "/save":
            filepath = self.conversation.save_conversation()
            self.console.print(f"[green]Conversation saved: {filepath}[/green]")
        elif cmd == "/stats":
            self.show_stats()
        elif cmd == "/skills":
            self.show_skills()
        else:
            self.console.print(f"[red]Unknown command: {command}[/red]")
            self.console.print("[yellow]Type /help for available commands[/yellow]")

    def show_help(self):
        """Show help information"""
        help_text = """
# JARVIS Commands

## Special Commands
- `/help` - Show this help message
- `/clear` - Clear conversation history
- `/save` - Save current conversation
- `/stats` - Show memory and conversation statistics
- `/skills` - List available skills
- `exit` or `quit` - Exit JARVIS

## Usage Examples
- "Search for latest AI news"
- "Remember that my favorite color is blue"
- "Remind me to call mom at 5 PM"
- "Calculate 25 * 4 + 10"
- "What's the weather like?"
- "Generate an image of a sunset"
        """
        self.console.print(Panel(Markdown(help_text), title="Help", style="cyan"))

    def show_stats(self):
        """Show statistics"""
        memory_stats = self.memory.get_memory_stats()
        conv_summary = self.conversation.get_conversation_summary()

        stats_text = f"""
# Statistics

## Memory
- Total memories: {memory_stats['total_memories']}
- By type: {memory_stats['by_type']}

## Conversation
- {conv_summary}
        """
        self.console.print(Panel(Markdown(stats_text), title="Statistics", style="cyan"))

    def show_skills(self):
        """Show available skills"""
        skills_text = "# Available Skills\n\n"
        for name, skill in self.skills.items():
            skills_text += f"- **{name}**: {skill.get_description()}\n"

        self.console.print(Panel(Markdown(skills_text), title="Skills", style="cyan"))
