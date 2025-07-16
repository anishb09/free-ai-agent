"""
Hugging Face Inference API model implementation
"""

from typing import List, Dict, Any, Optional, AsyncIterator
import aiohttp
import json
from .base import BaseModel, ModelResponse


class HuggingFaceModel(BaseModel):
    """Hugging Face Inference API model implementation"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium", api_key: str = "", **kwargs):
        super().__init__(model_name, api_key, **kwargs)
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # Default parameters
        self.default_params = {
            "max_new_tokens": 100,
            "temperature": 0.7,
            "top_p": 0.95,
            "do_sample": True,
            "return_full_text": False,
        }
        self.default_params.update(kwargs)
    
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Generate a response using Hugging Face Inference API"""
        prepared_messages = self.prepare_messages(messages)
        
        # Convert messages to text format
        prompt = self._messages_to_prompt(prepared_messages)
        
        # Merge parameters
        params = {**self.default_params, **kwargs}
        
        payload = {
            "inputs": prompt,
            "parameters": params,
            "options": {
                "wait_for_model": True,
                "use_cache": False
            }
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/{self.model_name}",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    response_text = await response.text()
                    
                    if response.status == 503:
                        # Model is loading, wait and retry
                        import time
                        time.sleep(2)
                        return await self.generate(messages, **kwargs)
                    
                    if response.status != 200:
                        raise Exception(f"Hugging Face API error: {response.status} - {response_text}")
                    
                    try:
                        result = await response.json()
                    except:
                        result = response_text
                    
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "")
                        # Remove the prompt from the generated text
                        if generated_text.startswith(prompt):
                            generated_text = generated_text[len(prompt):].strip()
                    else:
                        generated_text = str(result)
                    
                    return ModelResponse(
                        content=generated_text,
                        model=self.model_name,
                        usage={
                            "prompt_length": len(prompt),
                            "completion_length": len(generated_text),
                        },
                        finish_reason="stop",
                        metadata={
                            "provider": "huggingface",
                            "raw_response": result,
                        }
                    )
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Hugging Face connection error: {str(e)}")
        except Exception as e:
            raise Exception(f"Hugging Face API error: {str(e)}")
    
    async def generate_stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """Generate a streaming response (simulated for HF API)"""
        # Hugging Face Inference API doesn't support streaming, so we simulate it
        response = await self.generate(messages, **kwargs)
        
        # Simulate streaming by yielding chunks
        content = response.content
        chunk_size = 5  # Characters per chunk
        
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            yield chunk
            # Add a small delay to simulate streaming
            import asyncio
            await asyncio.sleep(0.05)
    
    def is_available(self) -> bool:
        """Check if Hugging Face API is available"""
        # For HuggingFace, we assume it's available if we have internet
        # The actual availability is checked during the first API call
        return True
    
    async def _check_hf_health(self) -> bool:
        """Check if Hugging Face API is available"""
        try:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/{self.model_name}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status in [200, 503]  # 503 means model is loading
        except:
            return False
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to a single prompt for Hugging Face"""
        prompt_parts = []
        
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        return "\n".join(prompt_parts) + "\nAssistant:"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get Hugging Face model information"""
        info = super().get_model_info()
        info.update({
            "provider": "Hugging Face",
            "base_url": self.base_url,
            "supported_models": [
                "microsoft/DialoGPT-medium",
                "microsoft/DialoGPT-large",
                "facebook/blenderbot-400M-distill",
                "facebook/blenderbot-1B-distill",
                "google/flan-t5-base",
                "google/flan-t5-large",
                "bigscience/bloom-560m",
                "EleutherAI/gpt-neo-1.3B",
                "EleutherAI/gpt-neo-2.7B",
            ],
            "features": ["chat", "text_generation", "free_tier"],
            "requirements": "Optional: HF API token for better rate limits"
        })
        return info
