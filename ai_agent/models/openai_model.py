"""
OpenAI model implementation
"""

from typing import List, Dict, Any, Optional, AsyncIterator
import openai
from .base import BaseModel, ModelResponse


class OpenAIModel(BaseModel):
    """OpenAI model implementation"""
    
    def __init__(self, model_name: str = "gpt-4", api_key: str = None, **kwargs):
        super().__init__(model_name, api_key, **kwargs)
        self.client = openai.AsyncOpenAI(api_key=api_key)
        
        # Default parameters
        self.default_params = {
            "temperature": 0.7,
            "max_tokens": 4000,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
        }
        self.default_params.update(kwargs)
    
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Generate a response using OpenAI API"""
        prepared_messages = self.prepare_messages(messages)
        
        # Merge parameters
        params = {**self.default_params, **kwargs}
        params["model"] = self.model_name
        params["messages"] = prepared_messages
        
        try:
            response = await self.client.chat.completions.create(**params)
            
            return ModelResponse(
                content=response.choices[0].message.content,
                model=response.model,
                usage=response.usage.model_dump() if response.usage else None,
                finish_reason=response.choices[0].finish_reason,
                metadata={
                    "response_id": response.id,
                    "created": response.created,
                    "system_fingerprint": getattr(response, 'system_fingerprint', None),
                }
            )
            
        except openai.OpenAIError as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """Generate a streaming response using OpenAI API"""
        prepared_messages = self.prepare_messages(messages)
        
        # Merge parameters
        params = {**self.default_params, **kwargs}
        params["model"] = self.model_name
        params["messages"] = prepared_messages
        params["stream"] = True
        
        try:
            stream = await self.client.chat.completions.create(**params)
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except openai.OpenAIError as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if OpenAI API is available"""
        try:
            # Simple check - try to create a client
            client = openai.OpenAI(api_key=self.api_key)
            return True
        except:
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get OpenAI model information"""
        info = super().get_model_info()
        info.update({
            "provider": "OpenAI",
            "supported_models": [
                "gpt-4",
                "gpt-4-turbo",
                "gpt-3.5-turbo",
                "gpt-4o",
                "gpt-4o-mini"
            ],
            "features": ["chat", "streaming", "function_calling"],
        })
        return info
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate tokens using tiktoken if available, otherwise use approximation"""
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model(self.model_name)
            return len(encoding.encode(text))
        except ImportError:
            # Fallback to approximation
            return super().estimate_tokens(text)
        except Exception:
            # Fallback if tiktoken fails
            return super().estimate_tokens(text)
