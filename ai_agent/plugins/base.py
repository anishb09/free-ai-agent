"""
Base plugin interface
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PluginResult:
    """Result from a plugin execution"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BasePlugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self, name: str, description: str = "", version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.version = version
        self.enabled = True
        self.config = {}
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> PluginResult:
        """Execute the plugin"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Get list of plugin capabilities"""
        pass
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the plugin"""
        self.config.update(config)
    
    def is_enabled(self) -> bool:
        """Check if plugin is enabled"""
        return self.enabled
    
    def enable(self) -> None:
        """Enable the plugin"""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable the plugin"""
        self.enabled = False
    
    def get_info(self) -> Dict[str, Any]:
        """Get plugin information"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "enabled": self.enabled,
            "capabilities": self.get_capabilities(),
            "config": self.config,
        }
    
    def validate_input(self, *args, **kwargs) -> bool:
        """Validate input parameters (can be overridden by subclasses)"""
        return True
    
    async def setup(self) -> None:
        """Setup the plugin (called when plugin is loaded)"""
        pass
    
    async def cleanup(self) -> None:
        """Cleanup the plugin (called when plugin is unloaded)"""
        pass


class PluginManager:
    """Manages plugins for the AI Agent"""
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_order: List[str] = []
    
    def register_plugin(self, plugin: BasePlugin) -> None:
        """Register a plugin"""
        self.plugins[plugin.name] = plugin
        if plugin.name not in self.plugin_order:
            self.plugin_order.append(plugin.name)
    
    def unregister_plugin(self, plugin_name: str) -> None:
        """Unregister a plugin"""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            if plugin_name in self.plugin_order:
                self.plugin_order.remove(plugin_name)
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """Get a plugin by name"""
        return self.plugins.get(plugin_name)
    
    def get_enabled_plugins(self) -> List[BasePlugin]:
        """Get all enabled plugins"""
        return [plugin for plugin in self.plugins.values() if plugin.is_enabled()]
    
    def get_all_plugins(self) -> List[BasePlugin]:
        """Get all plugins"""
        return list(self.plugins.values())
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.enable()
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin:
            plugin.disable()
            return True
        return False
    
    async def execute_plugin(self, plugin_name: str, *args, **kwargs) -> PluginResult:
        """Execute a specific plugin"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return PluginResult(
                success=False,
                error=f"Plugin '{plugin_name}' not found"
            )
        
        if not plugin.is_enabled():
            return PluginResult(
                success=False,
                error=f"Plugin '{plugin_name}' is disabled"
            )
        
        try:
            if not plugin.validate_input(*args, **kwargs):
                return PluginResult(
                    success=False,
                    error=f"Invalid input for plugin '{plugin_name}'"
                )
            
            return await plugin.execute(*args, **kwargs)
        except Exception as e:
            return PluginResult(
                success=False,
                error=f"Plugin '{plugin_name}' execution failed: {str(e)}"
            )
    
    async def setup_all_plugins(self) -> None:
        """Setup all plugins"""
        for plugin in self.plugins.values():
            try:
                await plugin.setup()
            except Exception as e:
                print(f"Failed to setup plugin '{plugin.name}': {str(e)}")
    
    async def cleanup_all_plugins(self) -> None:
        """Cleanup all plugins"""
        for plugin in self.plugins.values():
            try:
                await plugin.cleanup()
            except Exception as e:
                print(f"Failed to cleanup plugin '{plugin.name}': {str(e)}")
    
    def get_plugin_info(self) -> Dict[str, Any]:
        """Get information about all plugins"""
        return {
            "total_plugins": len(self.plugins),
            "enabled_plugins": len(self.get_enabled_plugins()),
            "plugins": [plugin.get_info() for plugin in self.plugins.values()],
        }
