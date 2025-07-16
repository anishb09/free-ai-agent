"""
Enhanced free AI agent with better conversation abilities
"""

import asyncio
import json
import random
from datetime import datetime
from typing import Dict, List, Optional
from ai_agent.core.conversation import ConversationManager
from ai_agent.core.config import Config


class EnhancedFreeAgent:
    """An enhanced free AI agent with better conversation abilities"""
    
    def __init__(self):
        self.config = Config()
        self.conversation = ConversationManager(
            max_history=20,
            system_prompt="You are a helpful and knowledgeable AI assistant."
        )
        
        # Enhanced knowledge base with more conversational responses
        self.knowledge_base = {
            "greetings": [
                "Hello! I'm your AI assistant. How can I help you today?",
                "Hi there! I'm here to help with questions and conversations. What's on your mind?",
                "Greetings! I'm an AI assistant ready to help. What would you like to know?",
                "Hello! Nice to meet you. I'm here to assist with various topics and questions.",
            ],
            "identity": [
                "I'm an AI assistant built with a free, open-source framework. I can help with conversations, answer questions, and assist with various tasks.",
                "I'm a conversational AI created to be helpful, harmless, and honest. I can discuss topics, help with problems, and provide information.",
                "I'm an AI assistant powered by a custom framework. I'm designed to be helpful and engaging while working completely offline.",
            ],
            "capabilities": [
                "I can help with: answering questions, having conversations, explaining concepts, problem-solving, providing information, and general assistance.",
                "My abilities include: chatting, answering questions, explaining topics, helping with decisions, and providing general information and support.",
                "I can assist with conversations, answer questions about various topics, help explain concepts, and provide general assistance.",
            ],
            "science_facts": {
                "solar_system": {
                    "largest planet": "Jupiter is the largest planet in our solar system! It's a gas giant that's more than twice as massive as all the other planets combined. It has a diameter of about 88,695 miles (142,800 km) and could fit about 1,300 Earths inside it.",
                    "smallest planet": "Mercury is the smallest planet in our solar system, with a diameter of about 3,032 miles (4,879 km). It's also the closest planet to the Sun.",
                    "planets": "Our solar system has 8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. They orbit the Sun in that order from closest to farthest.",
                },
                "general": {
                    "gravity": "Gravity is the force that attracts objects toward each other. On Earth, it pulls everything toward the center of the planet, which is why things fall down rather than up.",
                    "light speed": "Light travels at approximately 186,282 miles per second (299,792,458 meters per second) in a vacuum. This is the fastest speed possible in the universe.",
                    "photosynthesis": "Photosynthesis is the process plants use to convert sunlight, carbon dioxide, and water into glucose (food) and oxygen. It's essential for life on Earth.",
                },
            },
            "general_knowledge": {
                "countries": {
                    "largest": "Russia is the largest country by land area, covering about 6.6 million square miles. It spans 11 time zones!",
                    "smallest": "Vatican City is the smallest country in the world, with an area of just 0.17 square miles (0.44 square kilometers).",
                    "population": "China has the largest population with over 1.4 billion people, followed closely by India.",
                },
                "history": {
                    "world war": "World War II (1939-1945) was the largest conflict in human history, involving most of the world's nations and resulting in significant changes to global politics.",
                    "ancient": "Ancient civilizations like Egypt, Greece, and Rome laid the foundations for modern law, government, architecture, and philosophy.",
                },
                "nature": {
                    "tallest mountain": "Mount Everest is the tallest mountain on Earth, standing at 29,032 feet (8,849 meters) above sea level.",
                    "deepest ocean": "The Mariana Trench in the Pacific Ocean is the deepest known part of Earth's oceans, reaching about 36,200 feet (11,000 meters) deep.",
                    "largest animal": "The blue whale is the largest animal ever known to have lived on Earth, reaching lengths of up to 100 feet and weighing up to 200 tons.",
                },
            },
            "programming": {
                "python": "Python is a versatile, high-level programming language known for its readability and simplicity. It's excellent for beginners and widely used in web development, data science, AI, automation, and more. Would you like to know about specific Python topics?",
                "javascript": "JavaScript is the language of the web! It runs in browsers to create interactive websites and can also run server-side with Node.js. It's essential for modern web development. What aspect of JavaScript interests you?",
                "ai": "Artificial Intelligence involves creating systems that can perform tasks typically requiring human intelligence. This includes machine learning, natural language processing, computer vision, and robotics. It's a fascinating field that's rapidly evolving!",
                "general": "Programming is the art of solving problems through code. It involves breaking down complex tasks into logical steps and implementing them in a programming language. What programming topics would you like to explore?",
            },
            "explanations": {
                "machine_learning": "Machine learning is a subset of AI where systems learn patterns from data without being explicitly programmed. It includes supervised learning (with labeled data), unsupervised learning (finding patterns), and reinforcement learning (learning through rewards).",
                "web_development": "Web development involves creating websites and web applications. Frontend development handles what users see (HTML, CSS, JavaScript), while backend development manages servers, databases, and APIs. Modern web development often uses frameworks like React, Vue, or Angular.",
                "data_science": "Data science combines statistics, programming, and domain knowledge to extract insights from data. It involves collecting, cleaning, analyzing, and visualizing data to solve real-world problems and make data-driven decisions.",
                "technology": "Technology is constantly evolving, from smartphones and computers to AI and quantum computing. It shapes how we communicate, work, and live. What specific technology topics interest you?",
                "science": "Science helps us understand the world through observation, experimentation, and analysis. It spans physics, chemistry, biology, and many other fields. Each discovery builds on previous knowledge to expand our understanding.",
                "history": "History shows us how societies, cultures, and technologies have evolved over time. Learning from the past helps us understand the present and make better decisions for the future.",
            }
        }
        
        # Context tracking for better conversations
        self.context = {
            "user_name": None,
            "topics_discussed": [],
            "user_interests": [],
            "conversation_mood": "neutral"
        }
    
    async def chat(self, message: str) -> str:
        """Process a chat message and return a response"""
        # Add user message to conversation
        self.conversation.add_user_message(message)
        
        # Update context based on message
        self._update_context(message)
        
        # Generate response
        response = await self._generate_response(message)
        
        # Add assistant response to conversation
        self.conversation.add_assistant_message(response)
        
        return response
    
    def _update_context(self, message: str) -> None:
        """Update conversation context"""
        message_lower = message.lower()
        
        # Extract name if mentioned
        if "my name is" in message_lower or "i'm" in message_lower or "i am" in message_lower:
            words = message.split()
            for i, word in enumerate(words):
                if word.lower() in ["is", "am", "i'm"]:
                    if i + 1 < len(words):
                        potential_name = words[i + 1].strip(".,!?")
                        if potential_name.isalpha():
                            self.context["user_name"] = potential_name
        
        # Track topics
        topics = ["python", "javascript", "ai", "programming", "web", "data", "science", "technology"]
        for topic in topics:
            if topic in message_lower and topic not in self.context["topics_discussed"]:
                self.context["topics_discussed"].append(topic)
        
        # Detect mood
        positive_words = ["good", "great", "awesome", "excellent", "happy", "excited", "love", "like"]
        negative_words = ["bad", "terrible", "awful", "sad", "frustrated", "hate", "dislike", "problem"]
        
        if any(word in message_lower for word in positive_words):
            self.context["conversation_mood"] = "positive"
        elif any(word in message_lower for word in negative_words):
            self.context["conversation_mood"] = "negative"
    
    async def _generate_response(self, message: str) -> str:
        """Generate a contextual response"""
        message_lower = message.lower()
        
        # Science questions - Solar System (check these first, more specific)
        if any(phrase in message_lower for phrase in ["largest planet", "biggest planet"]):
            return self.knowledge_base["science_facts"]["solar_system"]["largest planet"]
        
        if any(phrase in message_lower for phrase in ["smallest planet", "tiniest planet"]):
            return self.knowledge_base["science_facts"]["solar_system"]["smallest planet"]
        
        if "planets" in message_lower and "solar system" in message_lower:
            return self.knowledge_base["science_facts"]["solar_system"]["planets"]
        
        # Science questions - General
        if "gravity" in message_lower:
            return self.knowledge_base["science_facts"]["general"]["gravity"]
        
        if any(phrase in message_lower for phrase in ["speed of light", "light speed"]):
            return self.knowledge_base["science_facts"]["general"]["light speed"]
        
        if "photosynthesis" in message_lower:
            return self.knowledge_base["science_facts"]["general"]["photosynthesis"]
        
        # Geography questions
        if any(phrase in message_lower for phrase in ["largest country", "biggest country"]):
            return self.knowledge_base["general_knowledge"]["countries"]["largest"]
        
        if any(phrase in message_lower for phrase in ["smallest country", "tiniest country"]):
            return self.knowledge_base["general_knowledge"]["countries"]["smallest"]
        
        if any(phrase in message_lower for phrase in ["tallest mountain", "highest mountain"]):
            return self.knowledge_base["general_knowledge"]["nature"]["tallest mountain"]
        
        if any(phrase in message_lower for phrase in ["deepest ocean", "deepest point"]):
            return self.knowledge_base["general_knowledge"]["nature"]["deepest ocean"]
        
        if any(phrase in message_lower for phrase in ["largest animal", "biggest animal"]):
            return self.knowledge_base["general_knowledge"]["nature"]["largest animal"]
        
        # Programming questions
        if any(word in message_lower for word in ["python", "programming", "code"]):
            return self._get_programming_response(message_lower)
        
        # Explanation requests
        if any(phrase in message_lower for phrase in ["explain", "what is", "tell me about"]):
            return self._get_explanation_response(message_lower)
        
        # Greeting responses (check after specific questions)
        if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            response = random.choice(self.knowledge_base["greetings"])
            if self.context["user_name"]:
                response = response.replace("Hello!", f"Hello, {self.context['user_name']}!")
            return response
        
        # Identity questions
        if any(phrase in message_lower for phrase in ["who are you", "what are you", "about yourself"]):
            return random.choice(self.knowledge_base["identity"])
        
        # Capability questions
        if any(phrase in message_lower for phrase in ["what can you do", "capabilities", "help with"]):
            return random.choice(self.knowledge_base["capabilities"])
        
        # Personal questions
        if any(phrase in message_lower for phrase in ["how are you", "how do you feel"]):
            responses = [
                "I'm doing well, thank you for asking! I'm here and ready to help.",
                "I'm functioning well and enjoying our conversation! How are you doing?",
                "I'm great! I'm always excited to chat and help with questions.",
            ]
            return random.choice(responses)
        
        # Name usage
        if self.context["user_name"] and any(phrase in message_lower for phrase in ["my name", "who am i"]):
            return f"Your name is {self.context['user_name']}! I remembered from our conversation."
        
        # Thank you responses
        if any(word in message_lower for word in ["thank", "thanks", "appreciate"]):
            responses = [
                "You're very welcome! I'm happy to help anytime.",
                "My pleasure! Feel free to ask anything else.",
                "You're welcome! I'm here whenever you need assistance.",
            ]
            return random.choice(responses)
        
        # Goodbye responses
        if any(word in message_lower for word in ["goodbye", "bye", "see you", "farewell"]):
            responses = [
                "Goodbye! It was great chatting with you. Come back anytime!",
                "Farewell! I enjoyed our conversation. Feel free to return whenever you'd like!",
                "See you later! Thanks for the chat, and don't hesitate to ask if you need help again!",
            ]
            return random.choice(responses)
        
        # Topic-based responses
        if "weather" in message_lower:
            return "I don't have access to real-time weather data, but I'd recommend checking a weather app or website for current conditions in your area!"
        
        if "time" in message_lower:
            return "I don't have access to real-time information, but you can check your system clock or any time-displaying device for the current time!"
        
        # General conversation
        return self._generate_conversational_response(message)
    
    def _get_programming_response(self, message: str) -> str:
        """Get programming-related response"""
        if "python" in message:
            return self.knowledge_base["programming"]["python"]
        elif "javascript" in message:
            return self.knowledge_base["programming"]["javascript"]
        elif "ai" in message or "artificial intelligence" in message:
            return self.knowledge_base["programming"]["ai"]
        else:
            return self.knowledge_base["programming"]["general"]
    
    def _get_explanation_response(self, message: str) -> str:
        """Get explanation-based response"""
        if "machine learning" in message or "ml" in message:
            return self.knowledge_base["explanations"]["machine_learning"]
        elif "web development" in message or "web dev" in message:
            return self.knowledge_base["explanations"]["web_development"]
        elif "data science" in message:
            return self.knowledge_base["explanations"]["data_science"]
        elif "technology" in message:
            return self.knowledge_base["general_knowledge"]["technology"]
        elif "science" in message:
            return self.knowledge_base["general_knowledge"]["science"]
        elif "history" in message:
            return self.knowledge_base["general_knowledge"]["history"]
        else:
            return "I'd be happy to explain that topic! Could you be more specific about what you'd like to know?"
    
    def _generate_conversational_response(self, message: str) -> str:
        """Generate a conversational response"""
        # First, try to find specific keywords and provide focused responses
        message_lower = message.lower()
        
        # Math and numbers
        if any(word in message_lower for word in ["math", "mathematics", "calculate", "number"]):
            return "I can help with basic math concepts! While I can't do complex calculations, I can explain mathematical principles and help with problem-solving approaches."
        
        # Colors
        if "color" in message_lower or "colour" in message_lower:
            return "Colors are fascinating! They're created by different wavelengths of light. The primary colors are red, blue, and yellow, and they can be combined to create all other colors."
        
        # Animals
        if "animal" in message_lower:
            return "Animals are incredibly diverse! From tiny insects to massive whales, the animal kingdom includes millions of species, each adapted to their environment in unique ways."
        
        # Food
        if "food" in message_lower:
            return "Food is essential for life and comes in amazing variety! Different cultures have developed unique cuisines, and nutrition science helps us understand how food affects our health."
        
        # Music
        if "music" in message_lower:
            return "Music is a universal language! It's created through combinations of rhythm, melody, and harmony. Different cultures have developed unique musical traditions and instruments."
        
        # Books/Reading
        if any(word in message_lower for word in ["book", "reading", "literature"]):
            return "Books are wonderful! They allow us to explore new worlds, learn new things, and experience different perspectives. Reading is one of the best ways to expand knowledge and imagination."
        
        # Context-aware responses
        if self.context["topics_discussed"]:
            recent_topics = ", ".join(self.context["topics_discussed"][-3:])
            responses = [
                f"That's interesting! We've been discussing {recent_topics}. Could you tell me more about what you're thinking?",
                f"I see! Building on our conversation about {recent_topics}, what specifically would you like to know?",
                f"Great question! Given our discussion about {recent_topics}, I'd love to help you explore that further.",
            ]
            return random.choice(responses)
        
        # Mood-based responses
        if self.context["conversation_mood"] == "positive":
            responses = [
                "That's wonderful! I'm glad to hear that. What else would you like to discuss?",
                "That sounds great! I'm here to help with anything else you'd like to talk about.",
                "Excellent! I'm enjoying our conversation. What other topics interest you?",
            ]
        elif self.context["conversation_mood"] == "negative":
            responses = [
                "I understand that can be frustrating. Is there anything specific I can help you with?",
                "I hear you. Sometimes things can be challenging. How can I assist you better?",
                "I appreciate you sharing that with me. Let me know how I can help improve things.",
            ]
        else:
            # More helpful default responses
            responses = [
                f"I'd be happy to help with that! Could you tell me more about what specifically you'd like to know?",
                f"That's an interesting topic. What particular aspect would you like to explore?",
                f"I'm here to help! Could you provide a bit more detail about what you're looking for?",
                f"Thanks for asking! What specific information would be most helpful to you?",
            ]
        
        return random.choice(responses)
    
    def get_conversation_stats(self) -> Dict:
        """Get enhanced conversation statistics"""
        summary = self.conversation.get_conversation_summary()
        return {
            **summary,
            "user_name": self.context["user_name"],
            "topics_discussed": self.context["topics_discussed"],
            "conversation_mood": self.context["conversation_mood"],
            "context_available": bool(self.context["user_name"] or self.context["topics_discussed"])
        }
    
    def clear_conversation(self) -> None:
        """Clear conversation history and context"""
        self.conversation.clear_history()
        self.context = {
            "user_name": None,
            "topics_discussed": [],
            "user_interests": [],
            "conversation_mood": "neutral"
        }


async def main():
    """Demo the enhanced free AI agent"""
    print("🤖 Enhanced Free AI Agent")
    print("=" * 50)
    print("✨ Features:")
    print("• Contextual conversations")
    print("• Memory of names and topics")
    print("• Mood-aware responses")
    print("• Enhanced knowledge base")
    print("• Completely offline!")
    print("=" * 50)
    
    # Initialize agent
    agent = EnhancedFreeAgent()
    
    print("\n💬 Interactive Chat")
    print("Type 'quit' to exit, 'clear' to clear history, 'stats' for info")
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
                print("🧹 Conversation and context cleared!")
                continue
            
            if user_input.lower() == 'stats':
                stats = agent.get_conversation_stats()
                print(f"📊 Conversation Stats:")
                print(f"   Messages: {stats['total_messages']}")
                print(f"   User name: {stats['user_name'] or 'Unknown'}")
                print(f"   Topics: {', '.join(stats['topics_discussed']) or 'None'}")
                print(f"   Mood: {stats['conversation_mood']}")
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
    print("🎉 This enhanced agent demonstrates advanced conversation capabilities!")


if __name__ == "__main__":
    asyncio.run(main())
