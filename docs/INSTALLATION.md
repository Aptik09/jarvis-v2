# JARVIS v2.0 Installation Guide

Complete installation instructions for JARVIS v2.0.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)
- Git

## System Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Internet**: Required for AI APIs and web search

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Aptik09/jarvis-v2.git
cd jarvis-v2
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
# Required
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_key_here

# Optional but recommended
PERPLEXITY_API_KEY=your_perplexity_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

### 5. Get API Keys

#### OpenAI (Required)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create new secret key
5. Copy and paste into `.env`

#### Perplexity (Optional - for web search)
1. Go to [Perplexity AI](https://www.perplexity.ai/)
2. Sign up for API access
3. Get your API key
4. Add to `.env`

#### ElevenLabs (Optional - for voice)
1. Go to [ElevenLabs](https://elevenlabs.io/)
2. Sign up for account
3. Get API key from profile
4. Add to `.env`

### 6. Verify Installation

Run the health check:
```bash
python -c "from config.settings import Settings; s = Settings(); print('✓ Configuration loaded successfully')"
```

### 7. Run JARVIS

**CLI Mode:**
```bash
python main.py
```

**Voice Mode:**
```bash
python main.py --voice
```

**Web Dashboard:**
```bash
python main.py --web
```

## Platform-Specific Instructions

### macOS

Install audio dependencies:
```bash
brew install portaudio
pip install pyaudio
```

### Linux (Ubuntu/Debian)

Install audio dependencies:
```bash
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

### Windows

PyAudio installation:
```bash
pip install pipwin
pipwin install pyaudio
```

## Troubleshooting

### Issue: PyAudio installation fails

**Solution:**
- **macOS**: `brew install portaudio`
- **Linux**: `sudo apt-get install portaudio19-dev`
- **Windows**: Use `pipwin install pyaudio`

### Issue: ChromaDB errors

**Solution:**
```bash
pip install --upgrade chromadb
```

### Issue: OpenAI API errors

**Solution:**
- Verify API key is correct
- Check API key has credits
- Ensure no extra spaces in `.env`

### Issue: Import errors

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

## Optional Components

### PDF Generation
```bash
pip install reportlab
```

### Audio Format Conversion
```bash
pip install pydub
```

### Advanced Search
```bash
pip install selenium webdriver-manager
```

## Verification Tests

Run basic tests:
```bash
# Test configuration
python -c "from config.settings import Settings; Settings().validate()"

# Test AI connection
python -c "from core.brain import Brain; from config.settings import Settings; Brain(Settings())"

# Test memory system
python -c "from core.memory import MemorySystem; from config.settings import Settings; MemorySystem(Settings())"
```

## Next Steps

After installation:
1. Read [USAGE.md](USAGE.md) for usage instructions
2. Check [API.md](API.md) for API documentation
3. See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/Aptik09/jarvis-v2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Aptik09/jarvis-v2/discussions)
- **Email**: aptikpandey9@gmail.com

## Update JARVIS

To update to the latest version:
```bash
git pull origin main
pip install --upgrade -r requirements.txt
```
