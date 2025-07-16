"""
Base model interface for language models
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator
from dataclasses import dataclass


@dataclass
class ModelResponse:
    """Response from a language model"""
    content: str
    model: str
    usage: Optional[Dict[str, Any]] = None
    finish_reason: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseModel(ABC):
    """Base class for all language models"""
    
    def __init__(self, model_name: str, api_key: str, **kwargs):
        self.model_name = model_name
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Generate a response from the model"""
        pass
    
    @abstractmethod
    async def generate_stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """Generate a streaming response from the model"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the model is available"""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model"""
        return {
            "model_name": self.model_name,
            "config": self.config,
            "available": self.is_available(),
        }
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in a text (rough approximation)"""
        # Simple approximation: 1 token ≈ 4 characters
        return len(text) // 4
    
    def validate_messages(self, messages: List[Dict[str, str]]) -> None:
        """Validate message format"""
        if not messages:
            raise ValueError("Messages list cannot be empty")
        
        for i, message in enumerate(messages):
            if not isinstance(message, dict):
                raise ValueError(f"Message {i} must be a dictionary")
            
            if "role" not in message:
                raise ValueError(f"Message {i} must have a 'role' field")
            
            if "content" not in message:
                raise ValueError(f"Message {i} must have a 'content' field")
            
            if message["role"] not in ["system", "user", "assistant"]:
                raise ValueError(f"Message {i} has invalid role: {message['role']}")
    
    def prepare_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Prepare messages for the model (can be overridden by subclasses)"""
        self.validate_messages(messages)
        return messages
