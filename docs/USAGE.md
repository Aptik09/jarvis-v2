# JARVIS v2.0 Usage Guide

Complete guide to using JARVIS v2.0 features.

## Getting Started

### Starting JARVIS

**CLI Mode (Default):**
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

**With Custom Port:**
```bash
python main.py --web --port 8080
```

**Debug Mode:**
```bash
python main.py --debug
```

## CLI Interface

### Basic Usage

```
You: Hello JARVIS
JARVIS: Hello! How can I assist you today?

You: What's 25 * 4?
JARVIS: 25 * 4 = 100

You: Search for latest AI news
JARVIS: Here are the latest AI news...
```

### Special Commands

- `/help` - Show help information
- `/clear` - Clear conversation history
- `/save` - Save current conversation
- `/stats` - Show statistics
- `/skills` - List available skills
- `exit` or `quit` - Exit JARVIS

### Examples

**Web Search:**
```
You: Search for Python tutorials
You: What is quantum computing?
You: Find information about climate change
```

**Memory Operations:**
```
You: Remember that my favorite color is blue
You: What's my favorite color?
You: Remember my birthday is January 15th
```

**Scheduling:**
```
You: Remind me to call mom at 5 PM
You: Set a reminder for tomorrow at 9 AM
You: Remind me in 30 minutes to check email
```

**Calculations:**
```
You: Calculate 15% of 200
You: What is the square root of 144?
You: Calculate compound interest on $1000 at 5% for 3 years
```

**File Operations:**
```
You: Create a text file with my notes
You: Generate a PDF report
```

**Image Generation:**
```
You: Generate an image of a sunset over mountains
You: Create a picture of a futuristic city
```

**Weather:**
```
You: What's the weather like?
You: Weather in New York
```

**News:**
```
You: Show me the latest news
You: What's happening in technology?
```

## Voice Interface

### Activation

1. Start voice mode: `python main.py --voice`
2. Wait for "Listening for wake word"
3. Say: **"Hey JARVIS"**
4. Give your command
5. JARVIS will respond with voice

### Voice Commands

Same as CLI commands, but spoken naturally:
- "Hey JARVIS, what's the weather?"
- "Hey JARVIS, remind me to call John at 3 PM"
- "Hey JARVIS, search for Python tutorials"

### Voice Tips

- Speak clearly and at normal pace
- Wait for JARVIS to finish responding
- Say "exit" or "goodbye" to quit
- If not understood, JARVIS will ask you to repeat

## Web Dashboard

### Accessing

1. Start web mode: `python main.py --web`
2. Open browser to: `http://localhost:5000`
3. Start chatting!

### Features

- **Real-time Chat**: Instant messaging with JARVIS
- **Quick Actions**: One-click common tasks
- **Statistics**: View memory and session stats
- **Clear History**: Reset conversation
- **Responsive Design**: Works on mobile and desktop

### Quick Actions

- 🔍 **Web Search**: Start a search query
- 🌤️ **Weather**: Get weather information
- 📰 **News**: View latest headlines
- 🔢 **Calculate**: Perform calculations
- 💾 **Remember**: Store information

## Skills Guide

### Search Skill

**Purpose**: Web search and information retrieval

**Usage:**
```
Search for [query]
What is [topic]?
Find information about [subject]
```

**Examples:**
- "Search for Python best practices"
- "What is machine learning?"
- "Find the latest news about AI"

### Memory Skill

**Purpose**: Store and retrieve information

**Store:**
```
Remember that [information]
Save this: [information]
Note that [information]
```

**Retrieve:**
```
What do you remember about [topic]?
Recall [information]
What did I tell you about [topic]?
```

**Examples:**
- "Remember that my favorite food is pizza"
- "What's my favorite food?"
- "Remember my meeting is at 3 PM tomorrow"

### Schedule Skill

**Purpose**: Create reminders and scheduled tasks

**Usage:**
```
Remind me to [task] at [time]
Set a reminder for [time]
Schedule [task] for [date/time]
```

**Time Formats:**
- "in 5 minutes"
- "at 3 PM"
- "tomorrow at 9 AM"
- "in 2 hours"

**Examples:**
- "Remind me to call mom at 5 PM"
- "Set a reminder for tomorrow at 9 AM"
- "Remind me in 30 minutes to check email"

### Calculator Skill

**Purpose**: Mathematical calculations

**Usage:**
```
Calculate [expression]
What is [math problem]?
[number] [operation] [number]
```

**Supported:**
- Basic: +, -, *, /
- Advanced: sqrt, sin, cos, tan, log
- Constants: pi, e

**Examples:**
- "Calculate 25 * 4 + 10"
- "What is the square root of 144?"
- "Calculate 15% of 200"

### File Skill

**Purpose**: Create and manage files

**Text Files:**
```
Create a text file with [content]
Save this to a file: [content]
```

**PDF Files:**
```
Create a PDF with [content]
Generate a PDF report
```

### Image Skill

**Purpose**: AI image generation

**Usage:**
```
Generate an image of [description]
Create a picture of [description]
Draw [description]
```

**Examples:**
- "Generate an image of a sunset over mountains"
- "Create a picture of a futuristic city"
- "Draw a cute robot"

### Weather Skill

**Purpose**: Weather information

**Usage:**
```
What's the weather?
Weather in [location]
How's the weather in [location]?
```

**Examples:**
- "What's the weather like?"
- "Weather in New York"
- "How's the weather in London?"

### News Skill

**Purpose**: Latest news headlines

**Usage:**
```
Show me the news
What's the latest news?
News about [topic]
```

**Examples:**
- "Show me the latest news"
- "What's happening in technology?"
- "News about climate change"

## Advanced Features

### Conversation Context

JARVIS maintains conversation context:
```
You: What's the capital of France?
JARVIS: The capital of France is Paris.

You: What's the population?
JARVIS: Paris has a population of approximately 2.2 million...
```

### Multi-turn Conversations

JARVIS remembers previous exchanges:
```
You: Remember my name is John
JARVIS: I'll remember that your name is John.

You: What's my name?
JARVIS: Your name is John.
```

### Intent Detection

JARVIS automatically detects what you want:
- Questions → Search or answer
- "Remember" → Store in memory
- "Remind" → Create schedule
- Math → Calculate
- "Generate image" → Image creation

## Tips & Best Practices

1. **Be Specific**: Clear requests get better responses
2. **Use Context**: Reference previous messages
3. **Try Commands**: Use `/help` to see all commands
4. **Save Important**: Use `/save` for important conversations
5. **Clear When Needed**: Use `/clear` to start fresh

## Troubleshooting

### JARVIS not responding
- Check internet connection
- Verify API keys in `.env`
- Check logs in `data/logs/`

### Voice not working
- Check microphone permissions
- Verify PyAudio is installed
- Try adjusting microphone volume

### Web dashboard not loading
- Check if port 5000 is available
- Try different port: `--port 8080`
- Check browser console for errors

## Getting Help

- Type `/help` in CLI
- Check documentation in `docs/`
- Report issues on GitHub
- Email: aptikpandey9@gmail.com
