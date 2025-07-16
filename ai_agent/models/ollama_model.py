"""
Ollama model implementation for local LLMs
"""

from typing import List, Dict, Any, Optional, AsyncIterator
import aiohttp
import json
from .base import BaseModel, ModelResponse


class OllamaModel(BaseModel):
    """Ollama model implementation for local LLMs"""
    
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model_name, "", **kwargs)  # No API key needed for Ollama
        self.base_url = base_url.rstrip('/')
        
        # Default parameters
        self.default_params = {
            "temperature": 0.7,
            "top_p": 1.0,
            "top_k": 40,
            "repeat_penalty": 1.1,
        }
        self.default_params.update(kwargs)
    
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Generate a response using Ollama API"""
        prepared_messages = self.prepare_messages(messages)
        
        # Convert messages to Ollama format
        prompt = self._messages_to_prompt(prepared_messages)
        
        # Merge parameters
        params = {**self.default_params, **kwargs}
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": params
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Ollama API error: {response.status}")
                    
                    result = await response.json()
                    
                    return ModelResponse(
                        content=result.get("response", ""),
                        model=self.model_name,
                        usage={
                            "prompt_eval_count": result.get("prompt_eval_count", 0),
                            "eval_count": result.get("eval_count", 0),
                            "total_duration": result.get("total_duration", 0),
                        },
                        finish_reason="stop" if result.get("done", False) else "length",
                        metadata={
                            "load_duration": result.get("load_duration", 0),
                            "prompt_eval_duration": result.get("prompt_eval_duration", 0),
                            "eval_duration": result.get("eval_duration", 0),
                        }
                    )
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Ollama connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    async def generate_stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """Generate a streaming response using Ollama API"""
        prepared_messages = self.prepare_messages(messages)
        
        # Convert messages to Ollama format
        prompt = self._messages_to_prompt(prepared_messages)
        
        # Merge parameters
        params = {**self.default_params, **kwargs}
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "options": params
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Ollama API error: {response.status}")
                    
                    async for line in response.content:
                        if line:
                            try:
                                chunk = json.loads(line.decode())
                                if "response" in chunk:
                                    yield chunk["response"]
                                if chunk.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
                                
        except aiohttp.ClientError as e:
            raise Exception(f"Ollama connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        # For now, assume Ollama is available if the user wants to use it
        # The actual availability is checked during the first API call
        return True
    
    async def _check_ollama_health(self) -> bool:
        """Check if Ollama server is running"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    return response.status == 200
        except:
            return False
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to a single prompt for Ollama"""
        prompt_parts = []
        
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get Ollama model information"""
        info = super().get_model_info()
        info.update({
            "provider": "Ollama",
            "base_url": self.base_url,
            "supported_models": [
                "llama2", "codellama", "mistral", "neural-chat", 
                "starcode", "orca-mini", "vicuna", "llama2-uncensored"
            ],
            "features": ["chat", "streaming", "local_processing"],
            "requirements": "Ollama server running locally"
        })
        return info
    
    async def get_available_models(self) -> List[str]:
        """Get list of available models from Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        return [model["name"] for model in data.get("models", [])]
                    return []
        except:
            return []
