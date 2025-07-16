# 🤖 Free AI Agent - Complete Guide

## 🎯 Quick Start

Your AI agent is ready to use! Run it with:

```bash
python working_free_agent.py
```

## 🚀 What You Have

### ✅ Working Features
- **Interactive Chat**: Full conversation interface
- **Offline Operation**: No external APIs required
- **Conversation Management**: Tracks chat history
- **Intent Recognition**: Understands common requests
- **Knowledge Base**: Built-in responses for common topics
- **Rich CLI**: Beautiful terminal interface

### 🏗️ Architecture Components

1. **Core Framework** (`ai_agent/core/`)
   - `agent.py`: Main orchestrator
   - `conversation.py`: Chat history management
   - `config.py`: Configuration system

2. **Model System** (`ai_agent/models/`)
   - `base.py`: Abstract model interface
   - `huggingface_model.py`: HuggingFace API (configured)
   - `ollama_model.py`: Local Ollama (available)
   - `simple_chatbot.py`: Rule-based chatbot

3. **Plugin System** (`ai_agent/plugins/`)
   - `base.py`: Plugin interface
   - `example_plugin.py`: Example implementation

## 🔧 Adding Real AI Models

When you get access to AI services, you can easily add them:

### Option 1: OpenAI/Anthropic (Paid)
```bash
# Add to .env file
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

### Option 2: Ollama (Free, Local)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama2
```

### Option 3: HuggingFace (Free API)
Your token is already configured! Try different models:
```python
# In ai_agent/models/huggingface_model.py
# Change the model_id to different models
```

## 🎨 Customization

### Adding New Responses
Edit `working_free_agent.py`:

```python
self.knowledge_base = {
    "your_topic": {
        "keyword": "Your response here"
    }
}
```

### Creating Plugins
1. Create new file in `ai_agent/plugins/`
2. Inherit from `BasePlugin`
3. Implement required methods

### Custom Models
1. Create new file in `ai_agent/models/`
2. Inherit from `BaseModel`
3. Implement `generate()` method

## 🚀 Usage Examples

### Basic Chat
```python
from working_free_agent import WorkingFreeAgent

agent = WorkingFreeAgent()
response = await agent.chat("Hello, how are you?")
print(response)
```

### With Conversation History
```python
agent = WorkingFreeAgent()
await agent.chat("My name is John")
await agent.chat("What's my name?")  # Will remember context
```

### Using the Full Framework
```python
from ai_agent.core.agent import Agent
from ai_agent.core.config import Config

config = Config()
agent = Agent(config)
response = await agent.chat("Hello!")
```

## 📊 Available Commands

While running the agent:
- `quit` or `exit`: Exit the chat
- `clear`: Clear conversation history
- `summary`: Show conversation statistics

### Option 2: Interactive Chat

```bash
python -m ai_agent chat
```

This starts an interactive chat session with commands like:
- `help` - Show available commands
- `models` - List available models
- `model <name>` - Switch models
- `clear` - Clear conversation
- `quit` - Exit

### Option 3: Single Questions

```bash
python -m ai_agent ask "What is artificial intelligence?"
```

### Option 4: Show Information

```bash
python -m ai_agent info
python -m ai_agent models
```

## 🛠️ Development Commands

### VS Code Tasks (Ctrl+Shift+P → "Run Task")

- **Install Dependencies** - Install/update Python packages
- **Run Example** - Run the example script
- **Start Chat** - Start interactive chat session
- **Run Tests** - Run the test suite
- **Format Code** - Format code with Black
- **Type Check** - Run MyPy type checking

### VS Code Launch Configurations (F5)

- **Run Example** - Debug the example script
- **Start Chat Session** - Debug interactive chat
- **Ask Single Question** - Debug single question mode
- **Show Agent Info** - Debug info command
- **List Available Models** - Debug models command
- **Run Tests** - Debug test suite

## 📁 Project Structure

```
ai_agent/
├── ai_agent/              # Main package
│   ├── core/             # Core functionality
│   │   ├── agent.py      # Main AI agent class
│   │   ├── conversation.py # Conversation management
│   │   └── config.py     # Configuration management
│   ├── models/           # Language model integrations
│   │   ├── base.py       # Base model interface
│   │   ├── openai_model.py # OpenAI integration
│   │   └── anthropic_model.py # Anthropic integration
│   ├── plugins/          # Plugin system
│   │   ├── base.py       # Base plugin interface
│   │   └── examples/     # Example plugins
│   ├── utils/            # Utility functions
│   └── cli.py            # Command-line interface
├── tests/                # Test suite
├── example.py            # Example usage script
├── requirements.txt      # Dependencies
└── README.md            # Documentation
```

## 🔌 Extending the Agent

### Adding New Models

1. Create a new model class in `ai_agent/models/`
2. Inherit from `BaseModel`
3. Implement required methods: `generate()`, `generate_stream()`, `is_available()`
4. Register in `AIAgent._initialize_models()`

### Adding New Plugins

1. Create a new plugin class in `ai_agent/plugins/`
2. Inherit from `BasePlugin`
3. Implement required methods: `execute()`, `get_capabilities()`
4. Register in `AIAgent._initialize_plugins()`

### Example Plugin

```python
from ai_agent.plugins.base import BasePlugin, PluginResult

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__("my_plugin", "My custom plugin")
    
    async def execute(self, *args, **kwargs):
        # Your plugin logic here
        return PluginResult(success=True, data="result")
    
    def get_capabilities(self):
        return ["capability1", "capability2"]
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

## 🎨 Code Quality

Format code:

```bash
python -m black ai_agent/ tests/ example.py
```

Type checking:

```bash
python -m mypy ai_agent/
```

## 🚀 Next Steps

1. **Set up your API keys** in `.env`
2. **Run the example** to see it in action
3. **Try the interactive chat** for a full experience
4. **Explore the plugin system** to add custom functionality
5. **Read the code** to understand the architecture
6. **Write tests** for any new features you add

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Rich Console Documentation](https://rich.readthedocs.io/)
- [Click CLI Documentation](https://click.palletsprojects.com/)

Happy coding! 🎉
