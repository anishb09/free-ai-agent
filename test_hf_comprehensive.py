import asyncio
import aiohttp
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Your HuggingFace token
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

async def test_serverless_inference():
    """Test HuggingFace Serverless Inference API."""
    
    # Try the serverless endpoint format
    url = "https://api-inference.huggingface.co/models/gpt2"
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Simple payload
    payload = {
        "inputs": "The quick brown fox"
    }
    
    print(f"Testing serverless inference...")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Payload: {payload}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                status = response.status
                text = await response.text()
                
                print(f"\nResponse Status: {status}")
                print(f"Response Headers: {dict(response.headers)}")
                print(f"Response Text: {text}")
                
                if status == 200:
                    try:
                        result = json.loads(text)
                        print(f"✅ SUCCESS: {result}")
                        return result
                    except json.JSONDecodeError:
                        print(f"⚠️  Non-JSON response: {text}")
                        return text
                else:
                    print(f"❌ ERROR: {status}")
                    return None
                    
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return None

async def test_transformers_api():
    """Test HuggingFace Transformers API directly."""
    
    # Try different endpoint formats
    endpoints = [
        "https://api-inference.huggingface.co/models/gpt2",
        "https://api-inference.huggingface.co/pipeline/text-generation/gpt2",
        "https://huggingface.co/api/models/gpt2",
    ]
    
    for endpoint in endpoints:
        print(f"\n{'='*50}")
        print(f"Testing endpoint: {endpoint}")
        
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        try:
            async with aiohttp.ClientSession() as session:
                # Try GET request first
                print("Trying GET request...")
                async with session.get(endpoint, headers=headers) as response:
                    print(f"GET Status: {response.status}")
                    text = await response.text()
                    print(f"GET Response: {text[:200]}...")
                
                # Try POST request
                print("Trying POST request...")
                payload = {"inputs": "Hello world"}
                async with session.post(endpoint, json=payload, headers=headers) as response:
                    print(f"POST Status: {response.status}")
                    text = await response.text()
                    print(f"POST Response: {text[:200]}...")
                    
        except Exception as e:
            print(f"Exception: {e}")

async def check_hf_status():
    """Check HuggingFace service status."""
    
    status_urls = [
        "https://status.huggingface.co/api/v2/status.json",
        "https://huggingface.co/api/whoami-v2",
    ]
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    for url in status_urls:
        print(f"\n{'='*30}")
        print(f"Checking: {url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    print(f"Status: {response.status}")
                    text = await response.text()
                    print(f"Response: {text[:300]}...")
                    
        except Exception as e:
            print(f"Exception: {e}")

async def main():
    """Run all tests."""
    if not HF_TOKEN:
        print("❌ No HuggingFace token found!")
        return
    
    print(f"🔑 Using token: {HF_TOKEN[:20]}...")
    
    print("\n" + "="*60)
    print("COMPREHENSIVE HUGGINGFACE API TESTING")
    print("="*60)
    
    # Test 1: Check service status
    print("\n1. CHECKING SERVICE STATUS")
    await check_hf_status()
    
    # Test 2: Test serverless inference
    print("\n2. TESTING SERVERLESS INFERENCE")
    await test_serverless_inference()
    
    # Test 3: Test different endpoints
    print("\n3. TESTING DIFFERENT ENDPOINTS")
    await test_transformers_api()

if __name__ == "__main__":
    asyncio.run(main())
