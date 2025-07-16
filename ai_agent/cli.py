"""
Command-line interface for the AI Agent
"""

import asyncio
import sys
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.table import Table

from .core.agent import AIAgent
from .core.config import Config
from .utils.helpers import format_model_name, format_elapsed_time
import time


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """AI Agent - A modern, extensible AI agent framework"""
    pass


@cli.command()
@click.option('--model', '-m', help='Model to use (default: gpt-4)')
@click.option('--stream', '-s', is_flag=True, help='Enable streaming responses')
@click.option('--config', '-c', help='Path to configuration file')
def chat(model: Optional[str], stream: bool, config: Optional[str]):
    """Start an interactive chat session"""
    asyncio.run(_chat_session(model, stream, config))


@cli.command()
@click.option('--model', '-m', help='Model to use (default: gpt-4)')
@click.option('--config', '-c', help='Path to configuration file')
@click.argument('message')
def ask(model: Optional[str], config: Optional[str], message: str):
    """Ask a single question"""
    asyncio.run(_ask_question(model, config, message))


@cli.command()
def info():
    """Show agent information"""
    asyncio.run(_show_info())


@cli.command()
def models():
    """List available models"""
    asyncio.run(_list_models())


async def _chat_session(model: Optional[str], stream: bool, config_path: Optional[str]):
    """Run interactive chat session"""
    try:
        # Initialize agent
        config = Config.from_env()
        agent = AIAgent(config)
        
        if model:
            agent.set_model(model)
        
        # Display welcome message
        console.print(Panel.fit(
            f"🤖 Welcome to AI Agent!\n"
            f"Model: {format_model_name(agent.current_model)}\n"
            f"Type 'help' for commands, 'quit' to exit",
            title="AI Agent",
            style="bold blue"
        ))
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold green]You[/bold green]")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if user_input.lower() == 'help':
                    _show_help()
                    continue
                
                if user_input.lower() == 'clear':
                    agent.clear_conversation()
                    console.print("[yellow]Conversation cleared![/yellow]")
                    continue
                
                if user_input.lower().startswith('model '):
                    model_name = user_input[6:].strip()
                    try:
                        agent.set_model(model_name)
                        console.print(f"[green]Switched to model: {format_model_name(model_name)}[/green]")
                    except ValueError as e:
                        console.print(f"[red]Error: {e}[/red]")
                    continue
                
                if user_input.lower() == 'models':
                    _display_models(agent.get_available_models())
                    continue
                
                if user_input.lower() == 'info':
                    _display_agent_info(agent.get_agent_info())
                    continue
                
                # Generate response
                start_time = time.time()
                
                if stream:
                    console.print("\n[bold cyan]Assistant[/bold cyan]:")
                    response = ""
                    async for chunk in agent.chat_stream(user_input):
                        console.print(chunk, end="")
                        response += chunk
                    console.print()  # New line after streaming
                else:
                    with console.status("[bold green]Thinking...", spinner="dots"):
                        response = await agent.chat(user_input)
                    
                    console.print(f"\n[bold cyan]Assistant[/bold cyan]:")
                    console.print(Markdown(response))
                
                # Show timing
                elapsed = format_elapsed_time(start_time)
                console.print(f"\n[dim]Response time: {elapsed}[/dim]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'quit' to exit.[/yellow]")
                continue
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue
    
    except Exception as e:
        console.print(f"[red]Failed to initialize agent: {e}[/red]")
        sys.exit(1)


async def _ask_question(model: Optional[str], config_path: Optional[str], message: str):
    """Ask a single question"""
    try:
        # Initialize agent
        config = Config.from_env()
        agent = AIAgent(config)
        
        if model:
            agent.set_model(model)
        
        # Generate response
        start_time = time.time()
        
        with console.status("[bold green]Thinking...", spinner="dots"):
            response = await agent.chat(message)
        
        # Display response
        console.print(f"\n[bold cyan]Assistant ({format_model_name(agent.current_model)})[/bold cyan]:")
        console.print(Markdown(response))
        
        # Show timing
        elapsed = format_elapsed_time(start_time)
        console.print(f"\n[dim]Response time: {elapsed}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


async def _show_info():
    """Show agent information"""
    try:
        config = Config.from_env()
        agent = AIAgent(config)
        
        _display_agent_info(agent.get_agent_info())
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


async def _list_models():
    """List available models"""
    try:
        config = Config.from_env()
        agent = AIAgent(config)
        
        _display_models(agent.get_available_models())
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def _show_help():
    """Show help message"""
    help_text = """
    **Available Commands:**
    
    - `help` - Show this help message
    - `quit` or `exit` - Exit the chat session
    - `clear` - Clear conversation history
    - `model <name>` - Switch to a different model
    - `models` - List available models
    - `info` - Show agent information
    """
    console.print(Panel(help_text, title="Help", style="bold yellow"))


def _display_models(models: list):
    """Display available models"""
    table = Table(title="Available Models")
    table.add_column("Model", style="cyan")
    table.add_column("Display Name", style="green")
    table.add_column("Provider", style="yellow")
    
    for model in models:
        provider = "OpenAI" if model.startswith("gpt") else "Anthropic"
        table.add_row(model, format_model_name(model), provider)
    
    console.print(table)


def _display_agent_info(info: dict):
    """Display agent information"""
    table = Table(title="Agent Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Current Model", format_model_name(info["current_model"]))
    table.add_row("Available Models", str(len(info["available_models"])))
    table.add_row("Plugins Enabled", str(info["plugins_enabled"]))
    table.add_row("Max Tokens", str(info["config"]["max_tokens"]))
    table.add_row("Temperature", str(info["config"]["temperature"]))
    table.add_row("Max History", str(info["config"]["max_conversation_history"]))
    
    # Conversation info
    conv_info = info["conversation_summary"]
    table.add_row("Total Messages", str(conv_info["total_messages"]))
    table.add_row("User Messages", str(conv_info["user_messages"]))
    table.add_row("Assistant Messages", str(conv_info["assistant_messages"]))
    
    console.print(table)


if __name__ == "__main__":
    cli()
