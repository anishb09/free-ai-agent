"""
Test configuration for the AI Agent
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from ai_agent.core.config import Config
from ai_agent.core.conversation import ConversationManager, Message
from ai_agent.core.agent import AIAgent
from ai_agent.models.base import BaseModel, ModelResponse
from ai_agent.plugins.base import BasePlugin, PluginResult


@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    config = Config()
    config.openai_api_key = "test-key"
    config.anthropic_api_key = "test-key"
    config.default_model = "gpt-4"
    config.max_tokens = 1000
    config.temperature = 0.7
    config.max_conversation_history = 5
    return config


@pytest.fixture
def conversation_manager():
    """Conversation manager for testing"""
    return ConversationManager(max_history=5)


@pytest.fixture
def mock_model():
    """Mock model for testing"""
    model = Mock(spec=BaseModel)
    model.generate = AsyncMock(return_value=ModelResponse(
        content="Test response",
        model="gpt-4",
        usage={"prompt_tokens": 10, "completion_tokens": 20}
    ))
    model.is_available = Mock(return_value=True)
    return model


class TestConfig:
    """Test configuration management"""
    
    def test_config_creation(self):
        """Test config creation"""
        config = Config()
        assert config.default_model == "gpt-4"
        assert config.max_tokens == 4000
        assert config.temperature == 0.7
    
    def test_config_validation(self, mock_config):
        """Test config validation"""
        mock_config.validate()  # Should not raise
        
        # Test invalid config
        invalid_config = Config()
        with pytest.raises(ValueError):
            invalid_config.validate()
    
    def test_model_config(self, mock_config):
        """Test model configuration"""
        model_config = mock_config.get_model_config()
        assert model_config["model"] == "gpt-4"
        assert model_config["max_tokens"] == 1000
        assert model_config["temperature"] == 0.7


class TestConversationManager:
    """Test conversation management"""
    
    def test_add_message(self, conversation_manager):
        """Test adding messages"""
        conversation_manager.add_user_message("Hello")
        conversation_manager.add_assistant_message("Hi there!")
        
        messages = conversation_manager.get_messages()
        assert len(messages) == 3  # system + user + assistant
        assert messages[1].role == "user"
        assert messages[2].role == "assistant"
    
    def test_message_history_limit(self, conversation_manager):
        """Test message history limit"""
        # Add more messages than limit
        for i in range(10):
            conversation_manager.add_user_message(f"Message {i}")
            conversation_manager.add_assistant_message(f"Response {i}")
        
        messages = conversation_manager.get_messages()
        # Should keep system message + max_history messages
        assert len(messages) <= conversation_manager.max_history + 1
    
    def test_clear_history(self, conversation_manager):
        """Test clearing conversation history"""
        conversation_manager.add_user_message("Hello")
        conversation_manager.add_assistant_message("Hi!")
        
        conversation_manager.clear_history()
        messages = conversation_manager.get_messages()
        
        # Should only have system message
        assert len(messages) == 1
        assert messages[0].role == "system"
    
    def test_export_import(self, conversation_manager):
        """Test conversation export/import"""
        conversation_manager.add_user_message("Hello")
        conversation_manager.add_assistant_message("Hi!")
        
        # Export
        exported = conversation_manager.export_conversation()
        assert isinstance(exported, str)
        
        # Import into new manager
        new_manager = ConversationManager()
        new_manager.import_conversation(exported)
        
        # Should have same messages
        original_messages = conversation_manager.get_messages()
        imported_messages = new_manager.get_messages()
        
        assert len(original_messages) == len(imported_messages)
        assert original_messages[0].content == imported_messages[0].content


class TestMessage:
    """Test message handling"""
    
    def test_message_creation(self):
        """Test message creation"""
        message = Message("user", "Hello world")
        assert message.role == "user"
        assert message.content == "Hello world"
        assert message.metadata == {}
    
    def test_message_serialization(self):
        """Test message to/from dict"""
        message = Message("user", "Hello", metadata={"test": "value"})
        message_dict = message.to_dict()
        
        assert message_dict["role"] == "user"
        assert message_dict["content"] == "Hello"
        assert message_dict["metadata"]["test"] == "value"
        
        # Test from dict
        recreated = Message.from_dict(message_dict)
        assert recreated.role == message.role
        assert recreated.content == message.content
        assert recreated.metadata == message.metadata


class TestAIAgent:
    """Test AI Agent functionality"""
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, mock_config):
        """Test agent initialization"""
        # Mock the model initialization to avoid API calls
        with pytest.mock.patch.object(AIAgent, '_initialize_models'):
            agent = AIAgent(mock_config)
            assert agent.config == mock_config
            assert agent.current_model == mock_config.default_model
    
    @pytest.mark.asyncio
    async def test_chat_functionality(self, mock_config, mock_model):
        """Test chat functionality"""
        with pytest.mock.patch.object(AIAgent, '_initialize_models'):
            agent = AIAgent(mock_config)
            agent.models = {"gpt-4": mock_model}
            
            response = await agent.chat("Hello")
            
            assert response == "Test response"
            mock_model.generate.assert_called_once()
    
    def test_model_switching(self, mock_config):
        """Test model switching"""
        with pytest.mock.patch.object(AIAgent, '_initialize_models'):
            agent = AIAgent(mock_config)
            agent.models = {"gpt-4": Mock(), "gpt-3.5-turbo": Mock()}
            
            agent.set_model("gpt-3.5-turbo")
            assert agent.current_model == "gpt-3.5-turbo"
            
            with pytest.raises(ValueError):
                agent.set_model("invalid-model")


class TestPlugins:
    """Test plugin system"""
    
    def test_plugin_result(self):
        """Test plugin result"""
        result = PluginResult(success=True, data="test")
        assert result.success is True
        assert result.data == "test"
        assert result.metadata == {}
    
    def test_base_plugin(self):
        """Test base plugin functionality"""
        class TestPlugin(BasePlugin):
            async def execute(self, *args, **kwargs):
                return PluginResult(success=True, data="test")
            
            def get_capabilities(self):
                return ["test"]
        
        plugin = TestPlugin("test", "Test plugin")
        assert plugin.name == "test"
        assert plugin.description == "Test plugin"
        assert plugin.is_enabled() is True
        assert "test" in plugin.get_capabilities()


if __name__ == "__main__":
    pytest.main([__file__])
