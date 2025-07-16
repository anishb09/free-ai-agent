"""
Test script for free AI models
"""

import asyncio
import sys
from ai_agent.models.ollama_model import OllamaModel
from ai_agent.models.huggingface_model import HuggingFaceModel
from ai_agent.models.local_transformers_model import LocalTransformersModel


async def test_ollama():
    """Test Ollama model"""
    print("🔍 Testing Ollama...")
    
    model = OllamaModel(model_name="llama2")
    
    if model.is_available():
        print("✅ Ollama is available!")
        try:
            # Test with available models
            available_models = await model.get_available_models()
            print(f"📋 Available Ollama models: {available_models}")
            
            if available_models:
                # Test generation with first available model
                model.model_name = available_models[0]
                messages = [{"role": "user", "content": "Hello! Say hi back."}]
                response = await model.generate(messages)
                print(f"🤖 Ollama response: {response.content}")
            else:
                print("⚠️  No Ollama models downloaded. Run: ollama pull llama2")
        except Exception as e:
            print(f"❌ Ollama error: {e}")
    else:
        print("❌ Ollama is not available. Install from https://ollama.ai/")


async def test_huggingface():
    """Test Hugging Face model"""
    print("\n🔍 Testing Hugging Face...")
    
    model = HuggingFaceModel(model_name="microsoft/DialoGPT-medium")
    
    if model.is_available():
        print("✅ Hugging Face API is available!")
        try:
            messages = [{"role": "user", "content": "Hello! Say hi back."}]
            response = await model.generate(messages)
            print(f"🤖 Hugging Face response: {response.content}")
        except Exception as e:
            print(f"❌ Hugging Face error: {e}")
    else:
        print("❌ Hugging Face API is not available. Check internet connection.")


async def test_local_transformers():
    """Test local transformers model"""
    print("\n🔍 Testing Local Transformers...")
    
    model = LocalTransformersModel(model_name="gpt2")
    
    if model.is_available():
        print("✅ Transformers library is available!")
        try:
            messages = [{"role": "user", "content": "Hello! Say hi back."}]
            response = await model.generate(messages)
            print(f"🤖 Local model response: {response.content}")
        except Exception as e:
            print(f"❌ Local transformers error: {e}")
    else:
        print("❌ Transformers library is not available. Install with: pip install transformers torch")


async def main():
    """Main test function"""
    print("🧪 Testing Free AI Models\n")
    print("=" * 50)
    
    await test_ollama()
    await test_huggingface()
    await test_local_transformers()
    
    print("\n" + "=" * 50)
    print("🎉 Test complete!")
    print("\nℹ️  To get started:")
    print("1. For Ollama: Install from https://ollama.ai/ and run 'ollama pull llama2'")
    print("2. For Hugging Face: No setup needed, just use!")
    print("3. For local models: Run 'pip install transformers torch'")


if __name__ == "__main__":
    asyncio.run(main())
