<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# AI Agent Project Instructions

This is a modern, extensible AI agent framework built from scratch in Python. The project follows these architectural principles:

## Architecture Overview

- **Core Components**: Agent orchestration, conversation management, configuration
- **Model Integration**: Support for OpenAI and Anthropic models with a unified interface
- **Plugin System**: Extensible architecture for adding new capabilities
- **CLI Interface**: Rich command-line interface for user interaction

## Code Style Guidelines

- Use type hints throughout the codebase
- Follow async/await patterns for API calls
- Implement proper error handling with informative messages
- Use dataclasses for structured data
- Follow the plugin pattern for extensibility

## Key Components

- `ai_agent/core/agent.py`: Main AI agent orchestrator
- `ai_agent/core/conversation.py`: Conversation state management
- `ai_agent/core/config.py`: Configuration management
- `ai_agent/models/`: Language model implementations
- `ai_agent/plugins/`: Plugin system and examples
- `ai_agent/utils/`: Utility functions and logging

## Development Practices

- Write comprehensive tests for all components
- Use rich console output for better user experience
- Implement proper logging throughout the application
- Follow the BaseModel and BasePlugin patterns for consistency
- Handle API rate limits and errors gracefully

## Dependencies

- Core: openai, anthropic, pydantic, python-dotenv
- UI: rich, click for CLI
- Testing: pytest, pytest-asyncio
- Optional: tiktoken for token counting

When working on this project, prioritize:
1. Type safety and proper error handling
2. Extensibility through the plugin system
3. User experience with rich console output
4. Proper async/await usage for API calls
5. Comprehensive testing coverage
