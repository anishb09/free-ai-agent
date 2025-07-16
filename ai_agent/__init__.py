"""
AI Agent - Main package initialization
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "A modern, extensible AI agent framework"

from .core.agent import AIAgent
from .core.config import Config
from .core.conversation import ConversationManager

__all__ = ["AIAgent", "Config", "ConversationManager"]
