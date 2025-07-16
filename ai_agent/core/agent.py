"""
Main AI Agent class
"""

from typing import Dict, Any, Optional, List, AsyncIterator
import asyncio
import logging
from .config import Config
from .conversation import ConversationManager
from ..models.base import BaseModel
from ..models.openai_model import OpenAIModel
from ..models.anthropic_model import AnthropicModel
from ..models.ollama_model import OllamaModel
from ..models.huggingface_model import HuggingFaceModel
from ..models.local_transformers_model import LocalTransformersModel
from ..plugins.base import BasePlugin
from ..utils.logging import setup_logging


class AIAgent:
    """Main AI Agent class that orchestrates conversations and plugins"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config.from_env()
        self.config.validate()
        
        # Setup logging
        self.logger = setup_logging(self.config.log_level)
        
        # Initialize conversation manager
        self.conversation = ConversationManager(
            max_history=self.config.max_conversation_history,
            system_prompt=self.config.system_prompt
        )
        
        # Initialize models
        self.models: Dict[str, BaseModel] = {}
        self._initialize_models()
        
        # Initialize plugins
        self.plugins: Dict[str, BasePlugin] = {}
        if self.config.enable_plugins:
            self._initialize_plugins()
        
        # Set current model
        self.current_model = self.config.default_model
        
        self.logger.info(f"AI Agent initialized with model: {self.current_model}")
    
    def _initialize_models(self) -> None:
        """Initialize available language models"""
        # OpenAI models (if API key available)
        if self.config.openai_api_key:
            openai_models = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"]
            for model_name in openai_models:
                self.models[model_name] = OpenAIModel(
                    model_name=model_name,
                    api_key=self.config.openai_api_key,
                    **self.config.get_model_config()
                )
        
        # Anthropic models (if API key available)
        if self.config.anthropic_api_key:
            anthropic_models = [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229", 
                "claude-3-haiku-20240307",
                "claude-3-5-sonnet-20241022"
            ]
            for model_name in anthropic_models:
                self.models[model_name] = AnthropicModel(
                    model_name=model_name,
                    api_key=self.config.anthropic_api_key,
                    **self.config.get_model_config()
                )
        
        # Ollama models (free, local)
        ollama_models = ["llama2", "mistral", "codellama", "neural-chat", "orca-mini"]
        for model_name in ollama_models:
            ollama_model = OllamaModel(
                model_name=model_name,
                **self.config.get_model_config()
            )
            if ollama_model.is_available():
                self.models[f"ollama-{model_name}"] = ollama_model
        
        # Hugging Face models (free API)
        hf_models = [
            "microsoft/DialoGPT-medium",
            "microsoft/DialoGPT-large", 
            "facebook/blenderbot-400M-distill",
            "google/flan-t5-base",
            "EleutherAI/gpt-neo-1.3B"
        ]
        for model_name in hf_models:
            hf_model = HuggingFaceModel(
                model_name=model_name,
                api_key=getattr(self.config, 'huggingface_api_key', ''),
                **self.config.get_model_config()
            )
            if hf_model.is_available():
                display_name = model_name.split('/')[-1]
                self.models[f"hf-{display_name}"] = hf_model
        
        # Local transformers models (completely free)
        local_models = [
            "microsoft/DialoGPT-medium",
            "gpt2",
            "gpt2-medium",
            "facebook/blenderbot-400M-distill"
        ]
        for model_name in local_models:
            local_model = LocalTransformersModel(
                model_name=model_name,
                **self.config.get_model_config()
            )
            if local_model.is_available():
                display_name = model_name.split('/')[-1]
                self.models[f"local-{display_name}"] = local_model
        
        # Set default model to first available free model
        if not self.models:
            self.logger.warning("No models available! Please check your configuration.")
            self.logger.info("To get started with free models:")
            self.logger.info("1. Install Ollama: https://ollama.ai/ and run 'ollama pull llama2'")
            self.logger.info("2. Install transformers: pip install transformers torch")
            self.logger.info("3. Use Hugging Face models (no installation needed)")
            raise Exception("No models available. Please check FREE_SETUP.md for setup instructions.")
        else:
            # Prioritize free models if no paid API keys available
            if not self.config.openai_api_key and not self.config.anthropic_api_key:
                free_models = [k for k in self.models.keys() if k.startswith(('ollama-', 'hf-', 'local-'))]
                if free_models:
                    self.config.default_model = free_models[0]
                    self.logger.info(f"Using free model: {self.config.default_model}")
        
        self.logger.info(f"Initialized {len(self.models)} models")
        if self.models:
            self.logger.info(f"Available models: {', '.join(self.models.keys())}")
    
    def _initialize_plugins(self) -> None:
        """Initialize plugins (placeholder for future implementation)"""
        # This will be implemented when we add specific plugins
        self.logger.info("Plugin system initialized")
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return list(self.models.keys())
    
    def set_model(self, model_name: str) -> None:
        """Set the current model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not available. Available models: {self.get_available_models()}")
        
        self.current_model = model_name
        self.logger.info(f"Switched to model: {model_name}")
    
    def get_current_model(self) -> BaseModel:
        """Get the current model instance"""
        return self.models[self.current_model]
    
    async def chat(self, message: str, **kwargs) -> str:
        """Send a message to the agent and get a response"""
        self.logger.debug(f"Received message: {message}")
        
        # Add user message to conversation
        self.conversation.add_user_message(message)
        
        # Get model response
        try:
            model = self.get_current_model()
            messages = self.conversation.get_messages_for_api()
            
            response = await model.generate(messages, **kwargs)
            
            # Add assistant response to conversation
            self.conversation.add_assistant_message(
                response.content,
                metadata={
                    "model": response.model,
                    "usage": response.usage,
                    "finish_reason": response.finish_reason,
                }
            )
            
            self.logger.debug(f"Generated response: {response.content}")
            return response.content
            
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            error_msg = f"I apologize, but I encountered an error: {str(e)}"
            self.conversation.add_assistant_message(error_msg)
            return error_msg
    
    async def chat_stream(self, message: str, **kwargs) -> AsyncIterator[str]:
        """Send a message to the agent and get a streaming response"""
        self.logger.debug(f"Received streaming message: {message}")
        
        # Add user message to conversation
        self.conversation.add_user_message(message)
        
        try:
            model = self.get_current_model()
            messages = self.conversation.get_messages_for_api()
            
            response_content = ""
            async for chunk in model.generate_stream(messages, **kwargs):
                response_content += chunk
                yield chunk
            
            # Add complete response to conversation
            self.conversation.add_assistant_message(response_content)
            
        except Exception as e:
            self.logger.error(f"Error generating streaming response: {str(e)}")
            error_msg = f"I apologize, but I encountered an error: {str(e)}"
            self.conversation.add_assistant_message(error_msg)
            yield error_msg
    
    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt"""
        self.conversation.set_system_prompt(prompt)
        self.logger.info("System prompt updated")
    
    def clear_conversation(self) -> None:
        """Clear the conversation history"""
        self.conversation.clear_history()
        self.logger.info("Conversation history cleared")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation"""
        return self.conversation.get_conversation_summary()
    
    def export_conversation(self) -> str:
        """Export the conversation to JSON"""
        return self.conversation.export_conversation()
    
    def import_conversation(self, json_data: str) -> None:
        """Import a conversation from JSON"""
        self.conversation.import_conversation(json_data)
        self.logger.info("Conversation imported")
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agent"""
        return {
            "current_model": self.current_model,
            "available_models": self.get_available_models(),
            "plugins_enabled": self.config.enable_plugins,
            "conversation_summary": self.get_conversation_summary(),
            "config": {
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature,
                "max_conversation_history": self.config.max_conversation_history,
            }
        }
    
    async def close(self) -> None:
        """Clean up resources"""
        self.logger.info("AI Agent shutting down")
        # Close any open connections or resources
        pass
