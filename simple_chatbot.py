"""
Alternative free AI models that work without external installations
"""

import asyncio
import random
from typing import List, Dict, Any
from ai_agent.core.conversation import ConversationManager


class SimpleChatbotModel:
    """A simple rule-based chatbot that works offline"""
    
    def __init__(self, name="SimpleChatbot"):
        self.name = name
        self.responses = {
            "greeting": [
                "Hello! I'm a simple AI assistant. How can I help you today?",
                "Hi there! I'm here to help you with your questions.",
                "Hey! Nice to meet you. What would you like to know?",
                "Hello! I'm ready to assist you with anything you need."
            ],
            "how_are_you": [
                "I'm doing well, thank you for asking! I'm here and ready to help.",
                "I'm functioning perfectly and happy to assist you!",
                "All systems are running smoothly. How are you doing?",
                "I'm great! Thanks for asking. How can I help you today?"
            ],
            "what_are_you": [
                "I'm a simple AI assistant built with Python. I can help answer questions and have conversations.",
                "I'm an AI chatbot created to demonstrate the AI agent framework you're using.",
                "I'm a conversational AI that can help with various tasks and questions.",
                "I'm your AI assistant, built to be helpful, harmless, and honest."
            ],
            "capabilities": [
                "I can have conversations, answer questions, help with problem-solving, and provide information on various topics.",
                "I'm designed to be helpful with general questions, creative tasks, and problem-solving.",
                "I can assist with writing, answering questions, brainstorming ideas, and general conversation.",
                "My capabilities include conversation, question answering, and helping with various tasks."
            ],
            "thanks": [
                "You're welcome! I'm happy to help.",
                "No problem! That's what I'm here for.",
                "My pleasure! Feel free to ask if you need anything else.",
                "Glad I could help! Let me know if you have more questions."
            ],
            "goodbye": [
                "Goodbye! It was nice talking with you.",
                "See you later! Have a great day!",
                "Take care! Feel free to come back anytime.",
                "Farewell! Hope to chat again soon."
            ],
            "help": [
                "I can help with questions, conversations, creative writing, problem-solving, and more. What do you need help with?",
                "I'm here to assist! You can ask me questions, have a conversation, or get help with various tasks.",
                "I can help with a wide range of topics. Just ask me anything you'd like to know!",
                "I'm ready to help! Whether you need information, want to chat, or need assistance with something."
            ],
            "default": [
                "That's an interesting question! While I'm a simple AI, I can try to help based on my knowledge.",
                "I understand you're asking about that topic. Let me share what I know.",
                "That's a good question! I'll do my best to provide a helpful response.",
                "I see what you're asking about. Let me think about that for you.",
                "Thanks for your question! I'll try to give you a useful answer."
            ]
        }
    
    def _classify_intent(self, message: str) -> str:
        """Classify the user's intent based on keywords"""
        message = message.lower()
        
        # Greeting patterns
        if any(word in message for word in ["hello", "hi", "hey", "good morning", "good evening"]):
            return "greeting"
        
        # How are you patterns
        if any(phrase in message for phrase in ["how are you", "how do you feel", "are you okay"]):
            return "how_are_you"
        
        # What are you patterns
        if any(phrase in message for phrase in ["what are you", "who are you", "what is this", "about yourself"]):
            return "what_are_you"
        
        # Capabilities patterns
        if any(word in message for word in ["can you", "what can", "capabilities", "able to", "help with"]):
            return "capabilities"
        
        # Thanks patterns
        if any(word in message for word in ["thank", "thanks", "appreciate", "grateful"]):
            return "thanks"
        
        # Goodbye patterns
        if any(word in message for word in ["goodbye", "bye", "see you", "farewell", "exit"]):
            return "goodbye"
        
        # Help patterns
        if any(word in message for word in ["help", "assist", "support", "guide"]):
            return "help"
        
        return "default"
    
    async def generate(self, messages: List[Dict[str, str]]) -> 'SimpleResponse':
        """Generate a response based on the last user message"""
        # Get the last user message
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        # Simulate thinking time
        await asyncio.sleep(0.3)
        
        # Classify intent and get response
        intent = self._classify_intent(user_message)
        response_options = self.responses.get(intent, self.responses["default"])
        response = random.choice(response_options)
        
        return SimpleResponse(content=response, model=self.name)
    
    async def generate_stream(self, messages: List[Dict[str, str]]):
        """Generate a streaming response"""
        response = await self.generate(messages)
        
        # Simulate streaming by yielding chunks
        content = response.content
        chunk_size = 3
        
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            yield chunk
            await asyncio.sleep(0.05)  # Small delay to simulate streaming
    
    def is_available(self) -> bool:
        """Always available since it's a simple local model"""
        return True


class SimpleResponse:
    """Simple response object"""
    def __init__(self, content: str, model: str):
        self.content = content
        self.model = model
        self.usage = {"input_length": 0, "output_length": len(content)}
        self.finish_reason = "stop"
        self.metadata = {"provider": "simple_chatbot"}


async def main():
    """Demo the simple chatbot"""
    print("🤖 Simple AI Chatbot Demo")
    print("=" * 50)
    print("This is a simple rule-based chatbot that works offline.")
    print("It demonstrates basic conversational AI without external APIs.")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = SimpleChatbotModel()
    
    # Initialize conversation manager
    conversation = ConversationManager(
        max_history=10,
        system_prompt="You are a helpful AI assistant."
    )
    
    print("\n💬 Interactive Chat")
    print("Type 'quit' to exit")
    print("-" * 30)
    
    try:
        while True:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("🤖 Assistant: Goodbye! Thanks for chatting with me!")
                break
            
            if not user_input:
                continue
            
            # Add user message
            conversation.add_user_message(user_input)
            
            # Get messages for model
            messages = conversation.get_messages_for_api()
            
            # Generate response
            print("🤔 Thinking...")
            response = await chatbot.generate(messages)
            
            # Add assistant response
            conversation.add_assistant_message(response.content)
            
            print(f"🤖 Assistant: {response.content}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Chat interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n✨ Demo completed!")
    print("\n🚀 This simple chatbot shows how the AI agent framework works.")
    print("You can extend it with more sophisticated AI models when available.")


if __name__ == "__main__":
    asyncio.run(main())
