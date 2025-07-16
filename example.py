"""
Simple example of using the AI Agent
"""

import asyncio
import os
from ai_agent import AIAgent, Config


async def main():
    """Main example function"""
    print("🤖 AI Agent Example")
    print("=" * 50)
    
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ No API keys found!")
        print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in your environment")
        print("Or create a .env file with your API keys")
        return
    
    try:
        # Initialize the agent
        print("🚀 Initializing AI Agent...")
        config = Config.from_env()
        agent = AIAgent(config)
        
        print(f"✅ Agent initialized with model: {agent.current_model}")
        print(f"📊 Available models: {', '.join(agent.get_available_models())}")
        
        # Example conversation
        print("\n💬 Starting conversation...")
        
        # Ask a simple question
        response = await agent.chat("Hello! Can you tell me what you are?")
        print(f"🤖 Assistant: {response}")
        
        # Ask a follow-up question
        response = await agent.chat("What are your main capabilities?")
        print(f"🤖 Assistant: {response}")
        
        # Ask for a calculation (if we had calculator plugin enabled)
        response = await agent.chat("Can you help me calculate 25 * 67?")
        print(f"🤖 Assistant: {response}")
        
        # Show conversation summary
        summary = agent.get_conversation_summary()
        print(f"\n📊 Conversation Summary:")
        print(f"   Total messages: {summary['total_messages']}")
        print(f"   User messages: {summary['user_messages']}")
        print(f"   Assistant messages: {summary['assistant_messages']}")
        
        # Example of streaming response
        print("\n🌊 Streaming response example...")
        print("🤖 Assistant: ", end="")
        async for chunk in agent.chat_stream("Tell me a short story about a robot"):
            print(chunk, end="")
        print()  # New line after streaming
        
        # Example of model switching (if multiple models available)
        available_models = agent.get_available_models()
        if len(available_models) > 1:
            print(f"\n🔄 Switching models...")
            original_model = agent.current_model
            
            # Switch to a different model
            for model in available_models:
                if model != original_model:
                    agent.set_model(model)
                    print(f"✅ Switched to: {model}")
                    
                    response = await agent.chat("What model are you?")
                    print(f"🤖 Assistant: {response}")
                    break
        
        print("\n✨ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you have valid API keys set up.")


if __name__ == "__main__":
    asyncio.run(main())
