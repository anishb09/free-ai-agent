"""
Quick test of the enhanced agent's specific responses
"""

import asyncio
from enhanced_free_agent import EnhancedFreeAgent


async def test_responses():
    agent = EnhancedFreeAgent()
    
    test_questions = [
        "What is the largest planet in the solar system?",
        "Which is the biggest planet?",
        "What is the smallest planet?",
        "Tell me about gravity",
        "What is the speed of light?",
        "What is the tallest mountain?",
        "Which is the largest country?",
        "What is the deepest ocean?",
        "Tell me about photosynthesis",
        "Hello how are you?",
        "Thank you for helping",
        "What can you do?",
        "Who are you?",
    ]
    
    print("🧪 Testing Enhanced Agent Responses")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        response = await agent.chat(question)
        print(f"🤖 Response: {response}")
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(test_responses())
