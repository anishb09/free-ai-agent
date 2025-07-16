import asyncio
import aiohttp
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Your HuggingFace token
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

# Test different model types and URLs
MODELS_TO_TEST = [
    # Text generation models
    "gpt2",
    "microsoft/DialoGPT-medium",
    "EleutherAI/gpt-neo-125m",
    "bigscience/bloom-560m",
    "huggingface/CodeBERTa-small-v1",
    
    # Conversational models
    "facebook/blenderbot-400M-distill",
    "microsoft/DialoGPT-small",
    
    # Small models for testing
    "distilgpt2",
    "openai-gpt",
]

async def test_model(session, model_name):
    """Test a single model with the HuggingFace API."""
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Simple test payload
    payload = {
        "inputs": "Hello, how are you?",
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.7,
            "return_full_text": False
        },
        "options": {
            "wait_for_model": True
        }
    }
    
    try:
        async with session.post(url, json=payload, headers=headers) as response:
            status = response.status
            text = await response.text()
            
            print(f"\n{'='*50}")
            print(f"Model: {model_name}")
            print(f"Status: {status}")
            print(f"Response: {text[:200]}...")
            
            if status == 200:
                try:
                    result = json.loads(text)
                    print(f"✅ SUCCESS: {result}")
                    return True
                except json.JSONDecodeError:
                    print(f"⚠️  SUCCESS but non-JSON response: {text}")
                    return True
            elif status == 503:
                print("⏳ Model loading...")
                return False
            else:
                print(f"❌ ERROR: {status} - {text}")
                return False
                
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

async def test_model_info(session, model_name):
    """Test model info endpoint."""
    url = f"https://huggingface.co/api/models/{model_name}"
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                info = await response.json()
                print(f"📊 Model info for {model_name}:")
                print(f"   Pipeline tag: {info.get('pipeline_tag', 'N/A')}")
                print(f"   Downloads: {info.get('downloads', 'N/A')}")
                return True
            else:
                print(f"❌ Model info not available: {response.status}")
                return False
    except Exception as e:
        print(f"❌ Exception getting model info: {e}")
        return False

async def main():
    """Test all models."""
    if not HF_TOKEN:
        print("❌ No HuggingFace token found in environment!")
        return
    
    print(f"🔑 Using HuggingFace token: {HF_TOKEN[:20]}...")
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
        print("\n" + "="*60)
        print("TESTING HUGGINGFACE INFERENCE API")
        print("="*60)
        
        working_models = []
        
        for model in MODELS_TO_TEST:
            # Test model info first
            await test_model_info(session, model)
            
            # Test actual inference
            success = await test_model(session, model)
            if success:
                working_models.append(model)
            
            # Small delay between requests
            await asyncio.sleep(1)
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Working models: {working_models}")
        print(f"Total working: {len(working_models)}/{len(MODELS_TO_TEST)}")

if __name__ == "__main__":
    asyncio.run(main())
