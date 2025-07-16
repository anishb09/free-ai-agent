"""
Logging utilities with rich formatting
"""

import logging
import sys
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Setup logging with rich formatting"""
    # Install rich traceback handler
    install(show_locals=True)
    
    # Create console
    console = Console()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )
    
    logger = logging.getLogger("ai_agent")
    logger.setLevel(getattr(logging, level.upper()))
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(f"ai_agent.{name}")


class LoggerMixin:
    """Mixin class to add logging functionality"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for the class"""
        return get_logger(self.__class__.__name__)
