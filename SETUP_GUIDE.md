# AI Agent Setup Guide - Free and Open Source

Welcome to your AI Agent! This guide will help you set up the agent using completely free and open-source AI models.

## 🚀 Quick Start (No Installation Required)

You can try the agent right away with the offline demo:

```bash
cd c:\Users\anish\Documents\agent
python demo.py
```

Choose option 2 for the offline demo that works without any external dependencies.

## 🔧 Free AI Model Options

### Option 1: Ollama (Recommended - Local Models)

Ollama runs AI models locally on your computer - completely free and private.

#### Installation:
1. Download Ollama from: https://ollama.com/
2. Install the Windows version
3. Open Command Prompt or PowerShell
4. Install a model: `ollama pull llama3.2:1b` (smaller) or `ollama pull llama3.2:3b` (better)

#### Test Ollama:
```bash
ollama run llama3.2:1b
```

#### Use with the Agent:
```bash
# Update .env file
DEFAULT_MODEL=ollama-llama3.2:1b

# Run the agent
python -m ai_agent.main
```

### Option 2: Local Transformers (Offline)

Run models completely offline using the transformers library.

#### Installation:
```bash
pip install transformers torch
```

#### Test:
```bash
python demo.py
# Choose option 1 for Local Transformers Demo
```

### Option 3: HuggingFace Issues

❌ **HuggingFace Inference API is currently not working** for free tier users. The API returns 404 errors even with valid tokens. This appears to be a service limitation.

## 🛠️ Full Setup Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
The `.env` file is already configured with your HuggingFace token, but since HF API isn't working, we'll use Ollama:

```env
# Default model (change based on what you have installed)
DEFAULT_MODEL=ollama-llama3.2:1b

# Ollama settings
OLLAMA_HOST=http://localhost:11434

# HuggingFace (not working currently)
HUGGINGFACE_API_KEY=hf_your_token_here
```

### 3. Install Ollama (Best Free Option)

1. **Download**: Go to https://ollama.com/download
2. **Install**: Run the installer for Windows
3. **Verify**: Open PowerShell and run: `ollama --version`
4. **Pull a model**: `ollama pull llama3.2:1b`
5. **Test**: `ollama run llama3.2:1b`

### 4. Available Models

#### Ollama Models (Local):
- `llama3.2:1b` - Fast, small model (~1GB)
- `llama3.2:3b` - Better quality (~2GB)
- `llama3.1:8b` - High quality (~5GB)
- `codellama:7b` - Code generation
- `mistral:7b` - Alternative model

#### Local Transformers Models:
- `gpt2` - Classic model, fast
- `distilgpt2` - Smaller, faster
- `microsoft/DialoGPT-small` - Conversational

## 🎯 Recommended Setup

For the best experience, I recommend:

1. **Install Ollama** (gives you access to modern models)
2. **Pull a small model first**: `ollama pull llama3.2:1b`
3. **Update your .env**: Set `DEFAULT_MODEL=ollama-llama3.2:1b`
4. **Run the agent**: `python -m ai_agent.main`

## 📋 Troubleshooting

### Ollama Not Found
- Make sure you downloaded and installed Ollama from https://ollama.com/
- Restart your terminal after installation
- Check that `ollama --version` works

### Model Loading Issues
- Start with smaller models first (`llama3.2:1b`)
- Make sure you have enough disk space
- Check that Ollama service is running

### HuggingFace Issues
- The HuggingFace Inference API is not working for free tier users
- Use local alternatives instead (Ollama or Local Transformers)

## 🔄 Usage Examples

### Basic Chat:
```bash
python -m ai_agent.main
```

### Plugin System:
```bash
python -m ai_agent.main --plugin weather
```

### Different Models:
```bash
# Use Ollama
python -m ai_agent.main --model ollama-llama3.2:1b

# Use Local Transformers  
python -m ai_agent.main --model local-gpt2
```

## 🎮 Demo Modes

Try the different demo modes to see the agent in action:

```bash
python demo.py
```

1. **Local Transformers Demo** - Uses offline AI models
2. **Offline Agent Demo** - Basic functionality without AI models

## 📁 Project Structure

```
ai_agent/
├── core/           # Core agent functionality
├── models/         # AI model implementations
├── plugins/        # Extensible plugin system
├── utils/          # Utility functions
└── main.py         # Main entry point

demo.py             # Interactive demo
requirements.txt    # Dependencies
.env               # Configuration
```

## 🆘 Getting Help

If you run into issues:

1. Try the offline demo first: `python demo.py`
2. Check that all dependencies are installed: `pip install -r requirements.txt`
3. Make sure Ollama is properly installed and running
4. Check the logs in the terminal for error messages

## 🚀 Next Steps

Once you have the basic setup working:

1. **Try different models** - Experiment with various Ollama models
2. **Explore plugins** - Add custom functionality through the plugin system
3. **Customize responses** - Modify the conversation management
4. **Add new model providers** - Extend the base model interface

Your AI agent is ready to go! 🎉
