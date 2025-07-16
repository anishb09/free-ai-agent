# 🆓 Free AI Agent Setup Guide

This guide shows you how to use the AI Agent with completely free and open-source models!

## 🚀 Quick Start (No API Keys Required!)

### Option 1: Ollama (Recommended - Local Models)

1. **Install Ollama** (Free local AI models):
   ```bash
   # Visit https://ollama.ai/ and download for your OS
   # Or use these commands:
   
   # Windows (PowerShell)
   iwr -useb https://ollama.ai/install.ps1 | iex
   
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Start Ollama and download a model**:
   ```bash
   # Start Ollama service
   ollama serve
   
   # In another terminal, download a model
   ollama pull llama2        # 7B parameters, good balance
   ollama pull mistral       # 7B parameters, very capable
   ollama pull codellama     # Great for coding
   ollama pull orca-mini     # Smaller, faster
   ```

3. **Run your AI Agent**:
   ```bash
   python -m ai_agent chat --model ollama-llama2
   ```

### Option 2: Hugging Face (Free API)

1. **Get a free Hugging Face account** (optional but recommended):
   - Visit https://huggingface.co/join
   - Go to https://huggingface.co/settings/tokens
   - Create a new token
   - Add to `.env`: `HUGGINGFACE_API_KEY=your_token_here`

2. **Run with Hugging Face models**:
   ```bash
   python -m ai_agent chat --model hf-DialoGPT-medium
   ```

### Option 3: Local Transformers (Completely Offline)

1. **Install additional dependencies**:
   ```bash
   pip install transformers torch
   ```

2. **Run with local models**:
   ```bash
   python -m ai_agent chat --model local-gpt2
   ```

## 🔧 Installation Steps

### 1. Install Core Dependencies

```bash
# Install required packages
pip install python-dotenv pydantic rich click aiohttp

# Optional: Install for local models
pip install transformers torch

# Optional: Install for better development
pip install pytest black mypy
```

### 2. Configuration

Create a `.env` file (copy from `.env.example`):

```bash
# For Ollama (free, local)
DEFAULT_MODEL=ollama-llama2
OLLAMA_BASE_URL=http://localhost:11434

# For Hugging Face (free, cloud)
# HUGGINGFACE_API_KEY=your_token_here
# DEFAULT_MODEL=hf-DialoGPT-medium

# For local transformers (free, offline)
# DEFAULT_MODEL=local-gpt2

LOG_LEVEL=INFO
MAX_CONVERSATION_HISTORY=10
```

## 🎯 Available Free Models

### Ollama Models (Local, Private)
- `ollama-llama2` - Meta's Llama 2 (7B) - Great general model
- `ollama-mistral` - Mistral 7B - Very capable and fast
- `ollama-codellama` - Code-specialized Llama model
- `ollama-neural-chat` - Intel's neural chat model
- `ollama-orca-mini` - Smaller, faster model

### Hugging Face Models (Cloud, Free tier)
- `hf-DialoGPT-medium` - Microsoft's conversational model
- `hf-DialoGPT-large` - Larger version of DialoGPT
- `hf-blenderbot-400M-distill` - Facebook's chatbot
- `hf-flan-t5-base` - Google's instruction-tuned model
- `hf-gpt-neo-1.3B` - EleutherAI's GPT-like model

### Local Transformers (Offline, Private)
- `local-gpt2` - OpenAI's GPT-2 model
- `local-gpt2-medium` - Larger GPT-2 model
- `local-DialoGPT-medium` - Microsoft's conversational model
- `local-blenderbot-400M-distill` - Facebook's chatbot

## 🛠️ Usage Examples

### Basic Chat
```bash
# With Ollama
python -m ai_agent chat --model ollama-llama2

# With Hugging Face
python -m ai_agent chat --model hf-DialoGPT-medium

# With local model
python -m ai_agent chat --model local-gpt2
```

### Single Question
```bash
python -m ai_agent ask --model ollama-mistral "Explain quantum computing"
```

### Check Available Models
```bash
python -m ai_agent models
```

### Run Example Script
```bash
python example.py
```

## 🔍 Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# List downloaded models
ollama list

# Download a model if missing
ollama pull llama2
```

### Hugging Face Issues
- Models might take time to load (cold start)
- Rate limits apply without API token
- Some models may be temporarily unavailable

### Local Transformers Issues
```bash
# Install missing dependencies
pip install transformers torch

# For Apple Silicon Macs
pip install torch torchvision torchaudio

# For CUDA GPU support
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
```

## 🚀 Performance Tips

### For Ollama:
- Use smaller models (orca-mini) for faster responses
- Ensure sufficient RAM (8GB+ recommended for 7B models)
- Use SSD storage for better model loading

### For Hugging Face:
- Get a free API token for better rate limits
- Use smaller models for faster responses
- Cache is enabled by default

### For Local Models:
- Use GPU if available (CUDA/Metal)
- Smaller models are faster but less capable
- First run downloads model files

## 📊 Model Comparison

| Model | Speed | Quality | Privacy | Requirements |
|-------|-------|---------|---------|-------------|
| Ollama | Fast | High | Complete | Local install |
| Hugging Face | Medium | Good | Partial | Internet |
| Local Transformers | Slow | Good | Complete | Python libs |

## 🎉 You're All Set!

You now have a completely free AI agent setup! Try different models to find what works best for your needs.

### Next Steps:
1. **Try different models** to see which you prefer
2. **Experiment with plugins** for extended functionality
3. **Customize the system prompt** for your use case
4. **Build your own plugins** for specific tasks

Happy chatting with your free AI agent! 🤖✨
