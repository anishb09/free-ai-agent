"""
Local transformers model implementation
"""

from typing import List, Dict, Any, Optional, AsyncIterator
import asyncio
from .base import BaseModel, ModelResponse


class LocalTransformersModel(BaseModel):
    """Local transformers model implementation"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium", **kwargs):
        super().__init__(model_name, "", **kwargs)  # No API key needed for local models
        self.tokenizer = None
        self.model = None
        self.device = "cpu"  # Default to CPU
        
        # Default parameters
        self.default_params = {
            "temperature": 0.7,
            "max_new_tokens": 200,
            "top_p": 0.95,
            "do_sample": True,
            "pad_token_id": 50256,  # GPT-2 pad token
        }
        self.default_params.update(kwargs)
    
    def _load_model(self):
        """Load the model and tokenizer"""
        if self.model is None:
            try:
                from transformers import AutoTokenizer, AutoModelForCausalLM
                import torch
                
                # Check for GPU availability
                if torch.cuda.is_available():
                    self.device = "cuda"
                elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                    self.device = "mps"  # Apple Silicon
                
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if self.device != "cpu" else torch.float32,
                    low_cpu_mem_usage=True
                ).to(self.device)
                
                # Set pad token if not exists
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
            except ImportError:
                raise Exception("transformers and torch are required for local models. Install with: pip install transformers torch")
            except Exception as e:
                raise Exception(f"Failed to load model {self.model_name}: {str(e)}")
    
    async def generate(self, messages: List[Dict[str, str]], **kwargs) -> ModelResponse:
        """Generate a response using local transformers"""
        self._load_model()
        prepared_messages = self.prepare_messages(messages)
        
        # Convert messages to text format
        prompt = self._messages_to_prompt(prepared_messages)
        
        # Merge parameters
        params = {**self.default_params, **kwargs}
        
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self._generate_sync, prompt, params)
            
            return ModelResponse(
                content=result,
                model=self.model_name,
                usage={
                    "prompt_length": len(prompt),
                    "completion_length": len(result),
                },
                finish_reason="stop",
                metadata={
                    "provider": "local_transformers",
                    "device": self.device,
                }
            )
            
        except Exception as e:
            raise Exception(f"Local model generation error: {str(e)}")
    
    def _generate_sync(self, prompt: str, params: Dict[str, Any]) -> str:
        """Synchronous generation function"""
        import torch
        
        # Tokenize input
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_new_tokens=params.get("max_new_tokens", 200),
                temperature=params.get("temperature", 0.7),
                top_p=params.get("top_p", 0.95),
                do_sample=params.get("do_sample", True),
                pad_token_id=params.get("pad_token_id", self.tokenizer.eos_token_id),
            )
        
        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the prompt from the response
        if response.startswith(prompt):
            response = response[len(prompt):].strip()
        
        return response
    
    async def generate_stream(self, messages: List[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """Generate a streaming response (simulated)"""
        # For now, simulate streaming by generating full response and yielding chunks
        response = await self.generate(messages, **kwargs)
        
        # Simulate streaming by yielding chunks
        content = response.content
        chunk_size = 3  # Characters per chunk
        
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            yield chunk
            # Add a small delay to simulate streaming
            await asyncio.sleep(0.1)
    
    def is_available(self) -> bool:
        """Check if transformers library is available"""
        try:
            import transformers
            import torch
            return True
        except ImportError:
            return False
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to a single prompt"""
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
        """Get local transformers model information"""
        info = super().get_model_info()
        info.update({
            "provider": "Local Transformers",
            "device": self.device,
            "supported_models": [
                "microsoft/DialoGPT-medium",
                "microsoft/DialoGPT-large",
                "facebook/blenderbot-400M-distill",
                "gpt2",
                "gpt2-medium",
                "gpt2-large",
                "EleutherAI/gpt-neo-125M",
                "EleutherAI/gpt-neo-1.3B",
            ],
            "features": ["chat", "local_processing", "no_api_required"],
            "requirements": "transformers, torch libraries"
        })
        return info
