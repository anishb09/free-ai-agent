"""
Plugins package initialization
"""

from .base import BasePlugin, PluginResult, PluginManager
from .examples import CalculatorPlugin, TextProcessingPlugin

__all__ = ["BasePlugin", "PluginResult", "PluginManager", "CalculatorPlugin", "TextProcessingPlugin"]
