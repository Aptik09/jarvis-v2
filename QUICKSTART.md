# JARVIS v2.0 - Quick Start Guide

Get up and running with JARVIS in 5 minutes!

## 🚀 Quick Installation

```bash
# 1. Clone the repository
git clone https://github.com/Aptik09/jarvis-v2.git
cd jarvis-v2

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API keys
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 🔑 Get Your API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create new secret key**
5. Copy the key and paste it in `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
```

## 🎯 First Run

### CLI Mode (Recommended for first time)

```bash
python main.py
```

You'll see:
```
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║        🤖  J A R V I S   v 2 . 0                     ║
║                                                       ║
║        Just A Rather Very Intelligent System         ║
║                                                       ║
║        Your Personal AI Assistant                    ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝

💬 How can I assist you today?

You: _
```

## 💬 Try These Commands

```
You: Hello JARVIS
You: What's 25 * 4?
You: Remember that my favorite color is blue
You: What's my favorite color?
You: Search for Python tutorials
You: /help
```

## 🎤 Voice Mode

```bash
python main.py --voice
```

Say: **"Hey JARVIS"** to activate, then speak your command.

## 🌐 Web Dashboard

```bash
python main.py --web
```

Open browser to: **http://localhost:5000**

## 📚 What's Next?

- **Full Documentation**: Check `docs/` folder
- **Installation Guide**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Usage Guide**: [docs/USAGE.md](docs/USAGE.md)
- **API Reference**: [docs/API.md](docs/API.md)

## 🎨 Features to Explore

### 1. Memory System
```
You: Remember that I live in New York
You: What city do I live in?
```

### 2. Web Search
```
You: Search for latest AI news
You: What is quantum computing?
```

### 3. Calculations
```
You: Calculate 15% of 200
You: What is the square root of 144?
```

### 4. Scheduling
```
You: Remind me to call mom at 5 PM
You: Set a reminder for tomorrow at 9 AM
```

### 5. Image Generation
```
You: Generate an image of a sunset over mountains
```

## 🛠️ Troubleshooting

### "API key not found"
- Check `.env` file exists
- Verify `OPENAI_API_KEY` is set
- No extra spaces around the key

### "Module not found"
```bash
pip install --upgrade -r requirements.txt
```

### Voice not working
```bash
# macOS
brew install portaudio

# Linux
sudo apt-get install portaudio19-dev

# Windows
pip install pipwin
pipwin install pyaudio
```

## 🎯 Common Use Cases

### Personal Assistant
- Set reminders
- Store notes and preferences
- Quick calculations
- Weather updates

### Research Helper
- Web search
- Information lookup
- Summarization
- Fact checking

### Development Aid
- Code explanations
- Documentation lookup
- Problem solving
- Learning resources

### Creative Work
- Image generation
- Content ideas
- Writing assistance
- Brainstorming

## 📖 Learn More

- **README**: [README.md](README.md)
- **Installation**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Usage**: [docs/USAGE.md](docs/USAGE.md)
- **API**: [docs/API.md](docs/API.md)
- **Contributing**: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 🤝 Get Help

- **Issues**: [GitHub Issues](https://github.com/Aptik09/jarvis-v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Aptik09/jarvis-v2/discussions)
- **Email**: aptikpandey9@gmail.com

## 🌟 Show Your Support

If you find JARVIS helpful:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code

---

**Built with ❤️ by Aptik Pandey**

Ready to explore? Start with `python main.py` and type `/help`!
