# 🤖 Free AI Agent Framework

A modern, extensible AI agent framework that works completely offline with no external dependencies required! Features rule-based chatbot capabilities and easy integration with real AI models when available.

## 🚀 Quick Start

### Option 1: Enhanced Agent (Recommended)
```bash
python enhanced_free_agent.py
```

### Option 2: Simple Agent
```bash
python working_free_agent.py
```

## ✨ Features

### 🎯 **Works Immediately**
- **No API keys required** - Start chatting right away
- **Completely offline** - No internet connection needed
- **Zero setup** - Just clone and run

### 🧠 **Smart Conversation**
- **Context awareness** - Remembers your name and conversation topics
- **Intent recognition** - Understands common questions and requests
- **Knowledge base** - Built-in responses for science, geography, programming, and more
- **Mood detection** - Adapts responses to conversation tone

### 🏗️ **Professional Architecture**
- **Modular design** - Easy to extend and customize
- **Plugin system** - Add new capabilities easily
- **Multiple model support** - Ready for OpenAI, Anthropic, HuggingFace, Ollama
- **Rich CLI interface** - Beautiful terminal interactions

## 🎬 Demo

```bash
🤖 Enhanced Free AI Agent
==================================================
✨ Features:
• Contextual conversations
• Memory of names and topics
• Mood-aware responses
• Enhanced knowledge base
• Completely offline!
==================================================

👤 You: What is the largest planet in the solar system?
🤖 Assistant: Jupiter is the largest planet in our solar system! It's a gas giant 
that's more than twice as massive as all the other planets combined. It has a 
diameter of about 88,695 miles (142,800 km) and could fit about 1,300 Earths inside it.

👤 You: My name is John
🤖 Assistant: Nice to meet you, John! I'll remember your name for our conversation.

👤 You: What's my name?
🤖 Assistant: Your name is John! I remembered from our conversation.
```

## 📦 Installation

### Prerequisites
- Python 3.8+ (tested with Python 3.13.5)
- pip (Python package manager)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/free-ai-agent.git
cd free-ai-agent

# Install dependencies
pip install -r requirements.txt

# Run the enhanced agent
python enhanced_free_agent.py
```

## 🎯 Usage

### Interactive Chat Commands
- `quit` or `exit` - Exit the chat
- `clear` - Clear conversation history
- `stats` - Show conversation statistics

### What the Agent Can Answer
- **Science**: Planets, gravity, speed of light, photosynthesis
- **Geography**: Countries, mountains, oceans, landmarks
- **Programming**: Python, JavaScript, AI concepts
- **General**: Technology, history, nature facts
- **Conversation**: Greetings, thanks, personal questions

### Example Questions
```bash
"What is the smallest planet?"
"Which is the tallest mountain?"
"Tell me about gravity"
"What can you do?"
"My name is Sarah"
"Explain photosynthesis"
```

## 🔧 Adding Real AI Models

When you want to upgrade to real AI models, the framework is ready:

### Option 1: OpenAI/Anthropic (Paid)
```bash
# Add to .env file
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Use the full framework
python -m ai_agent.main
```

### Option 2: HuggingFace (Free API)
```bash
# Add to .env file
HUGGINGFACE_TOKEN=your_token_here

# The framework will automatically use available models
python -m ai_agent.main
```

### Option 3: Ollama (Free, Local)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama2

# Framework will detect and use it
python -m ai_agent.main
```

## 🏗️ Architecture

```
ai_agent/
├── core/                 # Core functionality
│   ├── agent.py         # Main AI agent orchestrator
│   ├── conversation.py  # Conversation management
│   └── config.py        # Configuration system
├── models/              # AI model implementations
│   ├── base.py          # Abstract model interface
│   ├── openai_model.py  # OpenAI integration
│   ├── anthropic_model.py # Anthropic integration
│   ├── huggingface_model.py # HuggingFace integration
│   └── ollama_model.py  # Ollama integration
├── plugins/             # Plugin system
│   ├── base.py          # Plugin interface
│   └── example_plugin.py # Example implementation
└── utils/               # Utility functions

# Standalone agents
enhanced_free_agent.py   # Advanced offline agent
working_free_agent.py    # Simple offline agent
```

## 🎨 Customization

### Adding New Responses
Edit the knowledge base in `enhanced_free_agent.py`:

```python
self.knowledge_base = {
    "your_topic": {
        "keyword": "Your custom response here"
    }
}
```

### Creating Plugins
```python
from ai_agent.plugins.base import BasePlugin

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__("my_plugin", "My Custom Plugin")
    
    async def execute(self, command: str, args: dict) -> str:
        return f"Executed: {command} with {args}"
```

### Custom Models
```python
from ai_agent.models.base import BaseModel, ModelResponse

class CustomModel(BaseModel):
    async def generate(self, messages: list) -> ModelResponse:
        # Your custom implementation
        return ModelResponse(content="Custom response")
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Test specific responses:
```bash
python test_responses.py
```

## 📚 Documentation

- [Getting Started Guide](GETTING_STARTED.md) - Comprehensive setup guide
- [Architecture Overview](docs/architecture.md) - Technical details
- [Plugin Development](docs/plugins.md) - Creating custom plugins
- [Model Integration](docs/models.md) - Adding new AI models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Why This Project?

- **No barriers to entry** - Works immediately without API keys
- **Educational** - Learn AI agent architecture with working code
- **Extensible** - Easy to add real AI models when ready
- **Professional** - Production-ready architecture and patterns
- **Free** - Completely free and open source

## 🔮 Future Enhancements

- [ ] Web interface (Flask/FastAPI)
- [ ] Voice interaction
- [ ] Document processing
- [ ] Database integration
- [ ] Multi-language support
- [ ] Advanced plugin marketplace

## 🙏 Acknowledgments

- Built with modern Python async/await patterns
- Uses Rich for beautiful terminal output
- Follows clean architecture principles
- Inspired by modern AI assistant frameworks

---

**Start chatting with your AI agent today - no setup required!** 🚀

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
