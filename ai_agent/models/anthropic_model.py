"""
Anthropic model implementation
"""

from typing import List, Dict, Any, Optional, AsyncIterator
import anthropic
from .base import BaseModel, ModelResponse


class AnthropicModel(BaseModel):
    """Anthropic model implementation"""
    
    def __init__(self, model_name: str = "claude-3-sonnet-20240229", api_key: str = None, **kwargs):
        super().__init__(model_name, api_key, **kwargs)
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        
        # Default parameters
        self.default_params = {
            "temperature": 0.7,
            "max_tokens": 4000,
            "top_p": 1.0,
        }
        self.default_params.update(kwargs)
    
    def prepare_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Prepare messages for Anthropic API (handles system messages differently)"""
        prepared_messages = super().prepare_messages(messages)
        
        # Anthropic handles system messages separately
        system_messages = [msg for msg in prepared_messages if msg["role"] == "system"]
        non_system_messages = [msg for msg in prepared_messages if msg["role"] != "system"]
        
        # Combine system messages
        system_content = "\n\n".join([msg["content"] for msg in system_messages])
        
        return non_system_messages, system_content
    
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Generate a response using Anthropic API"""
        prepared_messages, system_content = self.prepare_messages(messages)
        
        # Merge parameters
        params = {**self.default_params, **kwargs}
        params["model"] = self.model_name
        params["messages"] = prepared_messages
        
        if system_content:
            params["system"] = system_content
        
        try:
            response = await self.client.messages.create(**params)
            
            # Extract content from response
            content = ""
            if response.content:
                content = response.content[0].text if response.content[0].type == "text" else ""
            
            return ModelResponse(
                content=content,
                model=response.model,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                } if response.usage else None,
                finish_reason=response.stop_reason,
                metadata={
                    "response_id": response.id,
                    "type": response.type,
                    "role": response.role,
                }
            )
            
        except anthropic.AnthropicError as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    async def generate_stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """Generate a streaming response using Anthropic API"""
        prepared_messages, system_content = self.prepare_messages(messages)
        
        # Merge parameters
        params = {**self.default_params, **kwargs}
        params["model"] = self.model_name
        params["messages"] = prepared_messages
        params["stream"] = True
        
        if system_content:
            params["system"] = system_content
        
        try:
            stream = await self.client.messages.create(**params)
            
            async for chunk in stream:
                if chunk.type == "content_block_delta":
                    if chunk.delta.type == "text_delta":
                        yield chunk.delta.text
                        
        except anthropic.AnthropicError as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Anthropic API is available"""
        try:
            # Simple check - try to create a client
            client = anthropic.Anthropic(api_key=self.api_key)
            return True
        except:
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get Anthropic model information"""
        info = super().get_model_info()
        info.update({
            "provider": "Anthropic",
            "supported_models": [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307",
                "claude-3-5-sonnet-20241022",
            ],
            "features": ["chat", "streaming", "long_context"],
        })
        return info
