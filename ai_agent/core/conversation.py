"""
Conversation management for the AI Agent
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class Message:
    """Represents a single message in the conversation"""
    role: str  # "user", "assistant", or "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary format"""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create message from dictionary"""
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {}),
        )


class ConversationManager:
    """Manages conversation history and context"""
    
    def __init__(self, max_history: int = 10, system_prompt: Optional[str] = None):
        self.max_history = max_history
        self.system_prompt = system_prompt or "You are a helpful AI assistant."
        self.messages: List[Message] = []
        self.conversation_id: Optional[str] = None
        
        # Add system message if provided
        if self.system_prompt:
            self.add_message("system", self.system_prompt)
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a new message to the conversation"""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        
        # Trim history if it exceeds max_history (keeping system message)
        if len(self.messages) > self.max_history + 1:  # +1 for system message
            # Keep system message and trim from oldest user/assistant messages
            system_msgs = [msg for msg in self.messages if msg.role == "system"]
            other_msgs = [msg for msg in self.messages if msg.role != "system"]
            
            # Keep only the most recent messages
            if len(other_msgs) > self.max_history:
                other_msgs = other_msgs[-self.max_history:]
            
            self.messages = system_msgs + other_msgs
    
    def add_user_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a user message to the conversation"""
        self.add_message("user", content, metadata)
    
    def add_assistant_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add an assistant message to the conversation"""
        self.add_message("assistant", content, metadata)
    
    def get_messages(self) -> List[Message]:
        """Get all messages in the conversation"""
        return self.messages.copy()
    
    def get_messages_for_api(self) -> List[Dict[str, str]]:
        """Get messages formatted for API calls"""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def get_last_message(self) -> Optional[Message]:
        """Get the last message in the conversation"""
        return self.messages[-1] if self.messages else None
    
    def get_user_messages(self) -> List[Message]:
        """Get all user messages"""
        return [msg for msg in self.messages if msg.role == "user"]
    
    def get_assistant_messages(self) -> List[Message]:
        """Get all assistant messages"""
        return [msg for msg in self.messages if msg.role == "assistant"]
    
    def clear_history(self) -> None:
        """Clear conversation history (keeping system message)"""
        system_msgs = [msg for msg in self.messages if msg.role == "system"]
        self.messages = system_msgs
    
    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt"""
        self.system_prompt = prompt
        
        # Remove old system messages and add new one
        self.messages = [msg for msg in self.messages if msg.role != "system"]
        self.messages.insert(0, Message("system", prompt))
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation"""
        user_count = len(self.get_user_messages())
        assistant_count = len(self.get_assistant_messages())
        
        return {
            "conversation_id": self.conversation_id,
            "total_messages": len(self.messages),
            "user_messages": user_count,
            "assistant_messages": assistant_count,
            "system_prompt": self.system_prompt,
            "last_message_time": self.get_last_message().timestamp.isoformat() if self.get_last_message() else None,
        }
    
    def export_conversation(self) -> str:
        """Export conversation to JSON string"""
        data = {
            "conversation_id": self.conversation_id,
            "system_prompt": self.system_prompt,
            "messages": [msg.to_dict() for msg in self.messages],
            "summary": self.get_conversation_summary(),
        }
        return json.dumps(data, indent=2)
    
    def import_conversation(self, json_data: str) -> None:
        """Import conversation from JSON string"""
        data = json.loads(json_data)
        self.conversation_id = data.get("conversation_id")
        self.system_prompt = data.get("system_prompt", "You are a helpful AI assistant.")
        self.messages = [Message.from_dict(msg_data) for msg_data in data.get("messages", [])]
