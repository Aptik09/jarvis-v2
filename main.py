#!/usr/bin/env python3
"""
JARVIS v2.0 - Personal AI Assistant
Main entry point for the application
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel
from config.settings import Settings
from utils.logger import setup_logger
from interfaces.cli import CLIInterface
from interfaces.voice import VoiceInterface
from interfaces.web.app import create_app

console = Console()
logger = setup_logger(__name__)


def print_banner():
    """Display JARVIS startup banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║        🤖  J A R V I S   v 2 . 0                     ║
    ║                                                       ║
    ║        Just A Rather Very Intelligent System         ║
    ║                                                       ║
    ║        Your Personal AI Assistant                    ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    console.print(Panel(banner, style="bold cyan"))


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="JARVIS v2.0 - Your Personal AI Assistant"
    )
    parser.add_argument(
        "--mode",
        choices=["cli", "voice", "web"],
        default="cli",
        help="Interface mode (default: cli)"
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Start in voice mode"
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Start web dashboard"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Web dashboard port (default: 5000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to custom config file"
    )

    args = parser.parse_args()

    # Load settings
    try:
        settings = Settings(config_path=args.config)
        if args.debug:
            settings.DEBUG_MODE = True
    except Exception as e:
        console.print(f"[red]Error loading settings: {e}[/red]")
        return 1

    # Print banner
    print_banner()

    # Determine mode
    if args.web:
        mode = "web"
    elif args.voice:
        mode = "voice"
    else:
        mode = args.mode

    try:
        if mode == "cli":
            logger.info("Starting CLI interface")
            console.print("[green]Starting CLI mode...[/green]")
            interface = CLIInterface(settings)
            interface.run()

        elif mode == "voice":
            logger.info("Starting voice interface")
            console.print("[green]Starting voice mode...[/green]")
            if not settings.ENABLE_VOICE:
                console.print("[yellow]Voice mode is disabled in settings[/yellow]")
                return 1
            interface = VoiceInterface(settings)
            interface.run()

        elif mode == "web":
            logger.info("Starting web dashboard")
            console.print(f"[green]Starting web dashboard on port {args.port}...[/green]")
            app = create_app(settings)
            app.run(
                host=settings.WEB_HOST,
                port=args.port,
                debug=args.debug
            )

    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down JARVIS...[/yellow]")
        logger.info("JARVIS shutdown by user")
        return 0
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        logger.exception("Fatal error in main")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
