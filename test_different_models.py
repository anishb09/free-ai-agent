"""
Test with different Hugging Face models
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_agent.models.huggingface_model import HuggingFaceModel

async def test_different_models():
    """Test different Hugging Face models"""
    
    # Load environment variables
    load_dotenv()
    hf_token = os.getenv("HUGGINGFACE_API_KEY")
    
    print(f"🔑 Using token: {hf_token[:10]}..." if hf_token else "❌ No token")
    
    # Test different models
    models_to_test = [
        "gpt2",
        "microsoft/DialoGPT-medium",
        "facebook/blenderbot-400M-distill",
        "google/flan-t5-small",
        "distilgpt2"
    ]
    
    for model_name in models_to_test:
        print(f"\n🧪 Testing model: {model_name}")
        
        try:
            model = HuggingFaceModel(
                model_name=model_name,
                api_key=hf_token
            )
            
            messages = [{"role": "user", "content": "Hello"}]
            response = await model.generate(messages)
            
            print(f"✅ Success with {model_name}!")
            print(f"   Response: {response.content[:100]}...")
            break  # Stop at first successful model
            
        except Exception as e:
            print(f"❌ Failed with {model_name}: {str(e)[:100]}...")
            continue
    
    else:
        print("\n❌ All models failed. Let's try a simple text generation model...")
        
        # Try a simple text generation model
        try:
            import aiohttp
            
            headers = {"Content-Type": "application/json"}
            if hf_token:
                headers["Authorization"] = f"Bearer {hf_token}"
            
            payload = {
                "inputs": "Hello, how are you?",
                "parameters": {
                    "max_new_tokens": 50,
                    "temperature": 0.7
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api-inference.huggingface.co/models/gpt2",
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"✅ Direct API success!")
                        print(f"   Response: {result}")
                    else:
                        error_text = await response.text()
                        print(f"❌ Direct API failed: {response.status} - {error_text}")
                        
        except Exception as e:
            print(f"❌ Direct API error: {e}")

if __name__ == "__main__":
    asyncio.run(test_different_models())
