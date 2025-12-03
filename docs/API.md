# JARVIS v2.0 API Documentation

API reference for developers integrating with JARVIS.

## Core Components

### Brain

Main AI engine for generating responses.

```python
from core.brain import Brain
from config.settings import Settings

# Initialize
settings = Settings()
brain = Brain(settings)

# Generate response
messages = [
    {"role": "user", "content": "Hello!"}
]
response = brain.generate_response(messages)
print(response)

# Streaming response
for chunk in brain.generate_streaming_response(messages):
    print(chunk, end='', flush=True)
```

**Methods:**
- `generate_response(messages, stream=False, max_tokens=None, temperature=0.7)` - Generate AI response
- `generate_streaming_response(messages, max_tokens=None, temperature=0.7)` - Stream response
- `analyze_intent(text)` - Analyze user intent
- `summarize_text(text, max_length=100)` - Summarize text
- `extract_keywords(text, count=5)` - Extract keywords

### Memory System

Vector-based memory storage using ChromaDB.

```python
from core.memory import MemorySystem
from config.settings import Settings

# Initialize
settings = Settings()
memory = MemorySystem(settings)

# Store memory
memory_id = memory.store(
    content="My favorite color is blue",
    memory_type="preference"
)

# Retrieve memories
memories = memory.retrieve(
    query="favorite color",
    n_results=5
)

# Store conversation
memory.store_conversation(
    user_message="What's the weather?",
    assistant_message="It's sunny today!"
)

# Get stats
stats = memory.get_memory_stats()
print(stats)
```

**Methods:**
- `store(content, metadata=None, memory_type="conversation")` - Store memory
- `retrieve(query, n_results=5, memory_type=None)` - Retrieve memories
- `store_conversation(user_message, assistant_message)` - Store conversation
- `store_fact(fact, category=None)` - Store fact
- `store_preference(preference, key=None)` - Store preference
- `get_memory_stats()` - Get statistics
- `delete_memory(memory_id)` - Delete memory
- `clear_old_memories(days=30)` - Clear old memories

### Conversation Manager

Manages conversation history and context.

```python
from core.conversation import ConversationManager
from config.settings import Settings

# Initialize
settings = Settings()
conversation = ConversationManager(settings)

# Add messages
conversation.add_message("user", "Hello!")
conversation.add_message("assistant", "Hi! How can I help?")

# Get messages
messages = conversation.get_messages(limit=10)

# Get context
context = conversation.get_context_messages(max_tokens=2000)

# Save conversation
filepath = conversation.save_conversation()

# Load conversation
conversation.load_conversation("conv_20250101_120000.json")

# Clear conversation
conversation.clear_conversation()
```

**Methods:**
- `add_message(role, content)` - Add message
- `get_messages(limit=None, include_system=False)` - Get messages
- `get_context_messages(max_tokens=2000)` - Get context
- `save_conversation(filename=None)` - Save to file
- `load_conversation(filename)` - Load from file
- `list_conversations()` - List saved conversations
- `clear_conversation()` - Clear history

### Intent Detector

Detects user intent from text.

```python
from core.intent_detector import IntentDetector

# Initialize
detector = IntentDetector()

# Detect intent
intent_data = detector.detect_intent("Search for Python tutorials")

print(intent_data)
# {
#     "primary_intent": "search",
#     "all_intents": ["search"],
#     "entities": {...},
#     "urgency": "low",
#     "requires_action": True
# }

# Check specific intents
if detector.requires_search(intent_data):
    print("Needs web search")

if detector.requires_memory(intent_data):
    print("Needs memory operation")
```

**Methods:**
- `detect_intent(text)` - Detect intent
- `requires_search(intent_data)` - Check if search needed
- `requires_memory(intent_data)` - Check if memory needed
- `requires_scheduling(intent_data)` - Check if scheduling needed

## Skills API

### Base Skill

All skills inherit from BaseSkill.

```python
from skills.base_skill import BaseSkill
from config.settings import Settings

class MySkill(BaseSkill):
    def __init__(self, settings: Settings):
        super().__init__(settings)
    
    def can_handle(self, intent_data):
        return "my_intent" in intent_data.get("all_intents", [])
    
    def execute(self, **kwargs):
        # Implement skill logic
        return self.create_response(
            success=True,
            data={"result": "success"},
            message="Operation completed"
        )
```

**Methods:**
- `execute(**kwargs)` - Execute skill (abstract)
- `can_handle(intent_data)` - Check if can handle (abstract)
- `get_description()` - Get skill description
- `validate_params(required_params, provided_params)` - Validate parameters
- `create_response(success, data=None, message=None, error=None)` - Create response

### Search Skill

```python
from skills.search_skill import SearchSkill

skill = SearchSkill(settings)
result = skill.execute(query="Python tutorials")

if result["success"]:
    print(result["data"])
```

### Memory Skill

```python
from skills.memory_skill import MemorySkill

skill = MemorySkill(settings, memory_system)

# Store
result = skill.execute(
    action="store",
    content="My favorite color is blue",
    memory_type="preference"
)

# Retrieve
result = skill.execute(
    action="retrieve",
    query="favorite color",
    n_results=5
)
```

### Calculator Skill

```python
from skills.calculator_skill import CalculatorSkill

skill = CalculatorSkill(settings)
result = skill.execute(expression="25 * 4 + 10")

print(result["data"]["result"])  # 110
```

## Web API

### REST Endpoints

**Health Check:**
```
GET /api/health

Response:
{
    "status": "healthy",
    "timestamp": "2025-01-01T12:00:00",
    "version": "2.0.0"
}
```

**Statistics:**
```
GET /api/stats

Response:
{
    "success": true,
    "data": {
        "memory": {
            "total_memories": 100,
            "by_type": {...}
        },
        "active_sessions": 5
    }
}
```

### WebSocket Events

**Connect:**
```javascript
socket.on('connect', () => {
    console.log('Connected');
});
```

**Send Message:**
```javascript
socket.emit('message', {
    message: 'Hello JARVIS'
});
```

**Receive Response:**
```javascript
socket.on('response', (data) => {
    console.log(data.message);
    console.log(data.timestamp);
    console.log(data.intent);
});
```

**Clear Conversation:**
```javascript
socket.emit('clear_conversation');
```

**Error Handling:**
```javascript
socket.on('error', (data) => {
    console.error(data.error);
});
```

## Configuration

### Settings

```python
from config.settings import Settings

settings = Settings()

# Access settings
print(settings.AI_PROVIDER)
print(settings.OPENAI_MODEL)
print(settings.MAX_TOKENS)

# Validate settings
if settings.validate():
    print("Settings valid")
```

### Prompts

```python
from config.prompts import SystemPrompts

# Get system prompt
prompt = SystemPrompts.get_system_prompt(
    personality="witty",
    response_style="detailed"
)

# Get conversation starter
starter = SystemPrompts.get_conversation_starter()

# Get error message
error = SystemPrompts.get_error_message()
```

## Utilities

### Logger

```python
from utils.logger import setup_logger

logger = setup_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Helpers

```python
from utils.helpers import *

# Sanitize filename
clean_name = sanitize_filename("my file!.txt")

# Parse time
time = parse_time_string("tomorrow at 3pm")

# Extract URLs
urls = extract_urls("Check https://example.com")

# Estimate tokens
tokens = estimate_tokens("Some text here")
```

## Error Handling

All API methods return standardized responses:

```python
{
    "success": True/False,
    "data": {...},  # On success
    "message": "...",  # Success message
    "error": "..."  # Error message
}
```

Example error handling:

```python
result = skill.execute(query="test")

if result["success"]:
    data = result["data"]
    # Process data
else:
    error = result["error"]
    # Handle error
```

## Examples

### Complete Integration

```python
from config.settings import Settings
from core.brain import Brain
from core.memory import MemorySystem
from core.conversation import ConversationManager
from skills import SearchSkill

# Initialize
settings = Settings()
brain = Brain(settings)
memory = MemorySystem(settings)
conversation = ConversationManager(settings)
search = SearchSkill(settings)

# Process user input
user_input = "Search for Python tutorials"

# Add to conversation
conversation.add_message("user", user_input)

# Execute search
search_result = search.execute(query=user_input)

# Generate AI response
messages = conversation.get_context_messages()
response = brain.generate_response(messages)

# Add response
conversation.add_message("assistant", response)

# Store in memory
memory.store_conversation(user_input, response)

print(response)
```

## Best Practices

1. **Always validate settings** before using components
2. **Handle errors gracefully** with try-except blocks
3. **Use context managers** for resource management
4. **Log important events** for debugging
5. **Clean up resources** when done
6. **Use type hints** for better code clarity
7. **Follow response format** for consistency

## Support

- **Documentation**: Check `docs/` folder
- **Issues**: [GitHub Issues](https://github.com/Aptik09/jarvis-v2/issues)
- **Email**: aptikpandey9@gmail.com
