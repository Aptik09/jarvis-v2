# 🤖 JARVIS v2.0 - Your Personal AI Assistant

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**JARVIS v2.0** is a complete personal AI assistant inspired by Iron Man's JARVIS. It features voice interaction, persistent memory, web search, scheduling, image generation, and a beautiful web dashboard.

## ✨ Features

### 🧠 Core Intelligence
- **Advanced AI Brain** - Powered by OpenAI GPT-4 or Anthropic Claude
- **Vector Memory System** - Remembers conversations and learns from interactions using ChromaDB
- **Context-Aware Responses** - Understands conversation flow and maintains context
- **Multi-Provider Support** - Switch between OpenAI, Anthropic, or local models

### 🎤 Voice Interface
- **Speech Recognition** - Powered by OpenAI Whisper
- **Text-to-Speech** - Natural voice responses using pyttsx3 or ElevenLabs
- **Wake Word Detection** - Activate with "Hey JARVIS"
- **Continuous Listening** - Hands-free operation mode

### 🔍 Smart Skills
- **Web Search** - Real-time information using Perplexity or Google
- **Scheduler** - Create reminders and recurring tasks
- **File Operations** - Create PDFs, manage documents
- **Image Generation** - AI-powered image creation
- **Weather Updates** - Current conditions and forecasts
- **News Aggregation** - Latest headlines and summaries
- **Calculator** - Complex mathematical operations

### 💻 Interfaces
- **CLI** - Beautiful command-line interface with colors and formatting
- **Web Dashboard** - Modern web interface with real-time updates
- **Voice Mode** - Fully hands-free operation
- **API** - RESTful API for integrations

### 🔌 Extensible Architecture
- **Plugin System** - Easy to add new skills
- **Webhook Support** - Integrate with external services
- **Custom Prompts** - Personalize JARVIS's personality
- **Multi-User Support** - Separate profiles and memories

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)
- API keys for AI services (OpenAI or Anthropic)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Aptik09/jarvis-v2.git
cd jarvis-v2
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run JARVIS**
```bash
# CLI Mode
python main.py

# Voice Mode
python main.py --voice

# Web Dashboard
python main.py --web
```

## 📖 Usage

### CLI Mode
```bash
$ python main.py
🤖 JARVIS v2.0 initialized
💬 How can I assist you today?

You: What's the weather like?
JARVIS: Let me check the current weather for you...

You: Remember that my favorite color is blue
JARVIS: I'll remember that your favorite color is blue.

You: Remind me to call mom at 5 PM
JARVIS: I've set a reminder to call mom at 5:00 PM today.
```

### Voice Mode
```bash
$ python main.py --voice
🎤 Voice mode activated. Say "Hey JARVIS" to start...

[You speak: "Hey JARVIS, what's on my schedule today?"]
JARVIS: You have 3 tasks scheduled for today...
```

### Web Dashboard
```bash
$ python main.py --web
🌐 Web dashboard running at http://localhost:5000
```

## 🏗️ Project Structure

```
jarvis_v2/
├── config/              # Configuration files
│   ├── settings.py      # App settings
│   ├── api_keys.py      # API key management
│   └── prompts.py       # System prompts
├── core/                # Core AI logic
│   ├── brain.py         # Main AI engine
│   ├── memory.py        # Vector memory system
│   ├── conversation.py  # Conversation management
│   └── intent_detector.py
├── skills/              # Skill modules
│   ├── search_skill.py
│   ├── schedule_skill.py
│   ├── memory_skill.py
│   └── ...
├── interfaces/          # User interfaces
│   ├── cli.py           # Command-line interface
│   ├── voice.py         # Voice interface
│   └── web/             # Web dashboard
├── utils/               # Utility functions
├── data/                # Data storage
├── tests/               # Unit tests
└── main.py              # Entry point
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:

```env
# AI Provider (openai or anthropic)
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Search
PERPLEXITY_API_KEY=your_perplexity_key

# Voice (optional)
ELEVENLABS_API_KEY=your_elevenlabs_key

# Database
CHROMA_PERSIST_DIR=./data/memory

# Web Dashboard
FLASK_SECRET_KEY=your_secret_key
WEB_PORT=5000
```

### Customization
Edit `config/prompts.py` to customize JARVIS's personality:

```python
SYSTEM_PROMPT = """
You are JARVIS, a highly intelligent AI assistant.
You are helpful, witty, and slightly sarcastic.
"""
```

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [Usage Guide](docs/USAGE.md) - How to use all features
- [API Documentation](docs/API.md) - API reference
- [Contributing](docs/CONTRIBUTING.md) - How to contribute

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=jarvis_v2 tests/
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 and Whisper
- Anthropic for Claude
- ChromaDB for vector storage
- All open-source contributors

## 📧 Contact

Aptik Pandey - [@Aptik09](https://github.com/Aptik09)

Project Link: [https://github.com/Aptik09/jarvis-v2](https://github.com/Aptik09/jarvis-v2)

---

**Built with ❤️ by Aptik Pandey**
