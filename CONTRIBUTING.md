# Contributing to Free AI Agent Framework

Thank you for your interest in contributing to the Free AI Agent Framework! We welcome contributions from the community.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/free-ai-agent.git
   cd free-ai-agent
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If it exists
   ```

## 🛠️ Development Setup

### Running Tests
```bash
pytest tests/ -v
```

### Code Formatting
```bash
black ai_agent/ tests/ *.py
```

### Type Checking
```bash
mypy ai_agent/
```

### Testing the Agent
```bash
# Test the enhanced agent
python enhanced_free_agent.py

# Test specific responses
python test_responses.py
```

## 📝 How to Contribute

### Bug Reports
- Use the GitHub issue tracker
- Include Python version, OS, and error messages
- Provide steps to reproduce the issue

### Feature Requests
- Open an issue to discuss the feature first
- Explain the use case and benefits
- Consider backward compatibility

### Code Contributions

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   pytest tests/
   python test_responses.py
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## 🎯 Areas for Contribution

### Easy (Good First Issues)
- Add new responses to the knowledge base
- Improve existing responses
- Add more test cases
- Fix typos in documentation

### Medium
- Create new plugins
- Add support for new AI models
- Improve conversation context handling
- Add new conversation commands

### Advanced
- Implement web interface
- Add voice interaction
- Create model benchmarking
- Implement advanced plugin system

## 📋 Code Style Guidelines

### Python Style
- Follow PEP 8
- Use type hints throughout
- Maximum line length: 88 characters
- Use black for code formatting

### Documentation
- Add docstrings to all functions and classes
- Update README.md for new features
- Include examples in docstrings

### Testing
- Write tests for new functionality
- Aim for good test coverage
- Test edge cases and error conditions

## 🔍 Code Review Process

1. **Automated checks** must pass (if configured)
2. **Manual review** by maintainers
3. **Discussion** and feedback
4. **Approval** and merge

## 📖 Documentation

### Adding New Models
```python
from ai_agent.models.base import BaseModel, ModelResponse

class YourModel(BaseModel):
    async def generate(self, messages: list) -> ModelResponse:
        # Implementation
        return ModelResponse(content="response")
```

### Adding New Plugins
```python
from ai_agent.plugins.base import BasePlugin

class YourPlugin(BasePlugin):
    def __init__(self):
        super().__init__("plugin_name", "Plugin Description")
    
    async def execute(self, command: str, args: dict) -> str:
        # Implementation
        return "result"
```

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help newcomers get started
- Share knowledge and experiences
- Follow the code of conduct

## 📞 Getting Help

- **Issues**: GitHub issue tracker
- **Discussions**: GitHub discussions
- **Documentation**: README.md and docs/

## 🎉 Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Contributors list

Thank you for contributing to the Free AI Agent Framework! 🚀
