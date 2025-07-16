"""
Simple free AI agent example using Hugging Face
"""

import asyncio
from ai_agent.models.huggingface_model import HuggingFaceModel
from ai_agent.core.conversation import ConversationManager


async def main():
    """Simple free AI agent example"""
    print("🤖 Free AI Agent Example")
    print("=" * 40)
    
    # Initialize Hugging Face model (free, no API key required)
    print("🚀 Initializing Hugging Face model...")
    model = HuggingFaceModel(model_name="microsoft/DialoGPT-medium")
    
    # Initialize conversation manager
    conversation = ConversationManager(
        max_history=5,
        system_prompt="You are a helpful AI assistant."
    )
    
    print("✅ Model initialized!")
    print("💬 Starting conversation...\n")
    
    try:
        # Example conversation
        questions = [
            "Hello! How are you?",
            "What is Python programming?",
            "Tell me a fun fact about AI"
        ]
        
        for question in questions:
            print(f"👤 User: {question}")
            
            # Add user message to conversation
            conversation.add_user_message(question)
            
            # Get messages for API
            messages = conversation.get_messages_for_api()
            
            # Generate response
            print("🤔 Thinking...")
            response = await model.generate(messages)
            
            # Add assistant response to conversation
            conversation.add_assistant_message(response.content)
            
            print(f"🤖 Assistant: {response.content}")
            print("-" * 40)
        
        # Show conversation summary
        summary = conversation.get_conversation_summary()
        print(f"\n📊 Conversation Summary:")
        print(f"   Total messages: {summary['total_messages']}")
        print(f"   User messages: {summary['user_messages']}")
        print(f"   Assistant messages: {summary['assistant_messages']}")
        
        print("\n✨ Example completed successfully!")
        print("🎉 You now have a working free AI agent!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. The model might be loading (try again in a moment)")
        print("3. Consider getting a free Hugging Face API token")
        print("4. Try a different model: facebook/blenderbot-400M-distill")


if __name__ == "__main__":
    asyncio.run(main())
