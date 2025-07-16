"""
Working free AI agent without external dependencies
"""

import asyncio
import os
from ai_agent.core.conversation import ConversationManager
from ai_agent.core.config import Config


class WorkingFreeAgent:
    """A working free AI agent that doesn't require external APIs"""
    
    def __init__(self):
        self.config = Config()
        self.conversation = ConversationManager(
            max_history=10,
            system_prompt="You are a helpful AI assistant created with the free AI agent framework."
        )
        
        # Simple response patterns
        self.knowledge_base = {
            "programming": {
                "python": "Python is a high-level programming language known for its simplicity and readability. It's great for beginners and widely used in web development, data science, and AI.",
                "javascript": "JavaScript is a programming language primarily used for web development. It runs in browsers and can also be used server-side with Node.js.",
                "ai": "Artificial Intelligence is the simulation of human intelligence in machines. It includes machine learning, natural language processing, and computer vision."
            },
            "general": {
                "weather": "I don't have access to real-time weather data, but I can suggest checking a weather app or website for current conditions.",
                "time": "I don't have access to real-time information, but you can check your system clock for the current time.",
                "help": "I'm here to help! I can answer questions about programming, provide general information, have conversations, and assist with various topics."
            }
        }
    
    async def chat(self, message: str) -> str:
        """Process a chat message and return a response"""
        # Add user message to conversation
        self.conversation.add_user_message(message)
        
        # Generate response
        response = await self._generate_response(message)
        
        # Add assistant response to conversation
        self.conversation.add_assistant_message(response)
        
        return response
    
    async def _generate_response(self, message: str) -> str:
        """Generate a response based on the message"""
        message_lower = message.lower()
        
        # Check for specific topics
        if any(word in message_lower for word in ["python", "programming", "code"]):
            return self._get_programming_response(message_lower)
        
        elif any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return "Hello! I'm your AI assistant. I'm here to help with questions, conversations, and various tasks. What would you like to know?"
        
        elif any(word in message_lower for word in ["how are you", "how do you feel"]):
            return "I'm doing well, thank you for asking! I'm functioning properly and ready to help you with anything you need."
        
        elif any(word in message_lower for word in ["what are you", "who are you", "about yourself"]):
            return "I'm an AI assistant built with a free AI agent framework. I can help answer questions, have conversations, and assist with various tasks. I'm designed to be helpful, harmless, and honest."
        
        elif any(word in message_lower for word in ["capabilities", "what can you do", "help with"]):
            return "I can help with: answering questions, having conversations, explaining concepts, helping with problem-solving, providing information on various topics, and assisting with general tasks. What would you like help with?"
        
        elif any(word in message_lower for word in ["thank", "thanks", "appreciate"]):
            return "You're very welcome! I'm happy to help. Feel free to ask if you need anything else."
        
        elif any(word in message_lower for word in ["goodbye", "bye", "see you", "farewell"]):
            return "Goodbye! It was nice talking with you. Feel free to come back anytime you need help!"
        
        elif "weather" in message_lower:
            return self.knowledge_base["general"]["weather"]
        
        elif "time" in message_lower:
            return self.knowledge_base["general"]["time"]
        
        elif any(word in message_lower for word in ["ai", "artificial intelligence", "machine learning"]):
            return self.knowledge_base["programming"]["ai"]
        
        else:
            return self._generate_general_response(message)
    
    def _get_programming_response(self, message: str) -> str:
        """Get a programming-related response"""
        if "python" in message:
            return self.knowledge_base["programming"]["python"]
        elif "javascript" in message:
            return self.knowledge_base["programming"]["javascript"]
        else:
            return "I'd be happy to help with programming questions! I can assist with Python, JavaScript, general programming concepts, and more. What specifically would you like to know?"
    
    def _generate_general_response(self, message: str) -> str:
        """Generate a general response"""
        responses = [
            "That's an interesting question! While I have limited knowledge as a simple AI, I'll do my best to help based on what I know.",
            "I understand you're asking about that topic. Let me share what I can tell you.",
            "That's a good question! I'll try to provide a helpful response based on my knowledge.",
            "I see what you're asking about. Let me think about that and give you the best answer I can.",
            "Thanks for your question! I'll do my best to provide useful information."
        ]
        
        import random
        return random.choice(responses) + f" You asked: '{message}'. Could you provide more context or ask something more specific?"
    
    def get_conversation_summary(self) -> dict:
        """Get conversation summary"""
        return self.conversation.get_conversation_summary()
    
    def clear_conversation(self) -> None:
        """Clear conversation history"""
        self.conversation.clear_history()


async def main():
    """Demo the working free AI agent"""
    print("🤖 Free AI Agent (No External Dependencies)")
    print("=" * 60)
    print("This AI agent works completely offline and doesn't require")
    print("any external APIs, installations, or tokens!")
    print("=" * 60)
    
    # Initialize agent
    agent = WorkingFreeAgent()
    
    print("\n💬 Interactive Chat")
    print("Type 'quit' to exit, 'clear' to clear history, 'summary' for info")
    print("-" * 40)
    
    try:
        while True:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                response = await agent.chat("goodbye")
                print(f"🤖 Assistant: {response}")
                break
            
            if user_input.lower() == 'clear':
                agent.clear_conversation()
                print("🧹 Conversation cleared!")
                continue
            
            if user_input.lower() == 'summary':
                summary = agent.get_conversation_summary()
                print(f"📊 Conversation Summary:")
                print(f"   Total messages: {summary['total_messages']}")
                print(f"   User messages: {summary['user_messages']}")
                print(f"   Assistant messages: {summary['assistant_messages']}")
                continue
            
            if not user_input:
                continue
            
            # Get response
            print("🤔 Thinking...")
            response = await agent.chat(user_input)
            
            print(f"🤖 Assistant: {response}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Chat interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n✨ Demo completed!")
    print("\n🎉 This demonstrates a working AI agent without external dependencies!")
    print("💡 You can extend this with real AI models when available.")


if __name__ == "__main__":
    asyncio.run(main())
