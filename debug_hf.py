"""
Debug Hugging Face API connection
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_agent.models.huggingface_model import HuggingFaceModel

async def test_hf_token():
    """Test Hugging Face token"""
    
    # Load environment variables
    load_dotenv()
    
    # Get the token
    hf_token = os.getenv("HUGGINGFACE_API_KEY")
    
    print(f"🔑 Token loaded: {hf_token[:10]}..." if hf_token else "❌ No token found")
    
    # Test with a simple model
    model = HuggingFaceModel(
        model_name="microsoft/DialoGPT-medium",
        api_key=hf_token
    )
    
    print(f"🤖 Model API key: {model.api_key[:10]}..." if model.api_key else "❌ No API key in model")
    
    # Test a simple request
    try:
        messages = [{"role": "user", "content": "Hello"}]
        print("🚀 Testing API call...")
        response = await model.generate(messages)
        print(f"✅ Success! Response: {response.content}")
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Try without token
        print("\n🔄 Trying without token...")
        model_no_token = HuggingFaceModel(
            model_name="microsoft/DialoGPT-medium",
            api_key=""
        )
        try:
            response = await model_no_token.generate(messages)
            print(f"✅ Success without token! Response: {response.content}")
        except Exception as e2:
            print(f"❌ Also failed without token: {e2}")

if __name__ == "__main__":
    asyncio.run(test_hf_token())
