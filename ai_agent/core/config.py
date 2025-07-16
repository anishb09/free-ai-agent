"""
Configuration management for the AI Agent
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration class for the AI Agent"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
    
    # Model Configuration
    default_model: str = "ollama-llama2"  # Default to free model
    max_tokens: int = 4000
    temperature: float = 0.7
    
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    
    # Conversation Configuration
    max_conversation_history: int = 10
    system_prompt: str = "You are a helpful AI assistant."
    
    # Plugin Configuration
    enable_plugins: bool = True
    plugin_directory: str = "plugins"
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Additional settings
    settings: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables"""
        load_dotenv()
        
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY"),
            default_model=os.getenv("DEFAULT_MODEL", "ollama-llama2"),
            max_tokens=int(os.getenv("MAX_TOKENS", "4000")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            max_conversation_history=int(os.getenv("MAX_CONVERSATION_HISTORY", "10")),
            system_prompt=os.getenv("SYSTEM_PROMPT", "You are a helpful AI assistant."),
            enable_plugins=os.getenv("ENABLE_PLUGINS", "true").lower() == "true",
            plugin_directory=os.getenv("PLUGIN_DIRECTORY", "plugins"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )
    
    def validate(self) -> None:
        """Validate the configuration"""
        # Check if at least one model source is available
        has_paid_api = self.openai_api_key or self.anthropic_api_key
        has_free_api = self.huggingface_api_key is not None  # Even empty string is valid for HF
        
        if not has_paid_api and not has_free_api:
            # Try to use local models or Ollama
            try:
                # Check if transformers is available for local models
                import transformers
                self.settings["local_models_available"] = True
            except ImportError:
                self.settings["local_models_available"] = False
            
            # Check if Ollama is available
            import aiohttp
            import asyncio
            try:
                async def check_ollama():
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"{self.ollama_base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=2)) as response:
                            return response.status == 200
                
                self.settings["ollama_available"] = asyncio.run(check_ollama())
            except:
                self.settings["ollama_available"] = False
            
            if not self.settings.get("local_models_available") and not self.settings.get("ollama_available"):
                print("⚠️  Warning: No API keys found and no local models available.")
                print("   You can still use Hugging Face models without an API key (with rate limits).")
                print("   Or install Ollama for local models: https://ollama.ai/")
        
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        
        if not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")
        
        if self.max_conversation_history < 0:
            raise ValueError("max_conversation_history must be non-negative")
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model-specific configuration"""
        return {
            "model": self.default_model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
