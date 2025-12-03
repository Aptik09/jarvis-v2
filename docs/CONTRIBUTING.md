# Contributing to JARVIS v2.0

Thank you for your interest in contributing to JARVIS v2.0! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Aptik09/jarvis-v2/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Error messages and logs

### Suggesting Features

1. Check [Issues](https://github.com/Aptik09/jarvis-v2/issues) for existing suggestions
2. Create a new issue with:
   - Clear feature description
   - Use cases and benefits
   - Possible implementation approach
   - Any relevant examples

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test your changes**
5. **Commit with clear messages**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

## Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/jarvis-v2.git
cd jarvis-v2
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 5. Run Tests

```bash
pytest tests/
```

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def calculate_sum(numbers: List[int]) -> int:
    """Calculate sum of numbers."""
    return sum(numbers)

# Bad
def calc(n):
    return sum(n)
```

### Code Formatting

Use **Black** for formatting:

```bash
black .
```

### Type Hints

Always use type hints:

```python
from typing import List, Dict, Optional

def process_data(
    data: List[str],
    options: Optional[Dict] = None
) -> Dict[str, any]:
    """Process data with options."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
    """
    pass
```

### Imports

Organize imports:

```python
# Standard library
import os
import sys
from typing import List, Dict

# Third-party
import requests
from flask import Flask

# Local
from config.settings import Settings
from core.brain import Brain
```

## Project Structure

```
jarvis_v2/
├── config/          # Configuration
├── core/            # Core AI logic
├── skills/          # Skill modules
├── interfaces/      # User interfaces
├── utils/           # Utilities
├── data/            # Data storage
├── tests/           # Tests
└── docs/            # Documentation
```

## Adding New Features

### Adding a New Skill

1. Create skill file in `skills/`:

```python
# skills/my_skill.py
from skills.base_skill import BaseSkill

class MySkill(BaseSkill):
    """Description of skill."""
    
    def can_handle(self, intent_data):
        return "my_intent" in intent_data.get("all_intents", [])
    
    def execute(self, **kwargs):
        # Implementation
        return self.create_response(
            success=True,
            data={"result": "success"}
        )
```

2. Add to `skills/__init__.py`:

```python
from .my_skill import MySkill

__all__ = [..., "MySkill"]
```

3. Add tests in `tests/test_my_skill.py`

4. Update documentation

### Adding Intent Patterns

Add patterns to `core/intent_detector.py`:

```python
PATTERNS = {
    "my_intent": [
        r"pattern1",
        r"pattern2",
    ],
}
```

### Adding Configuration

Add to `config/settings.py`:

```python
self.MY_SETTING = os.getenv("MY_SETTING", "default")
```

Add to `.env.example`:

```env
MY_SETTING=value
```

## Testing

### Writing Tests

Create test files in `tests/`:

```python
# tests/test_my_feature.py
import pytest
from my_module import my_function

def test_my_function():
    """Test my_function."""
    result = my_function("input")
    assert result == "expected"

def test_my_function_error():
    """Test my_function error handling."""
    with pytest.raises(ValueError):
        my_function(None)
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_brain.py

# With coverage
pytest --cov=jarvis_v2 tests/

# Verbose
pytest -v
```

### Test Coverage

Aim for >80% coverage:

```bash
pytest --cov=jarvis_v2 --cov-report=html tests/
```

## Documentation

### Code Documentation

- Add docstrings to all functions/classes
- Keep docstrings up to date
- Include examples in docstrings

### User Documentation

Update relevant docs in `docs/`:
- `INSTALLATION.md` - Installation changes
- `USAGE.md` - Usage changes
- `API.md` - API changes

### README Updates

Update `README.md` for:
- New features
- Changed requirements
- New dependencies

## Commit Messages

Use clear, descriptive commit messages:

```bash
# Good
git commit -m "Add web search skill with DuckDuckGo support"
git commit -m "Fix memory retrieval bug in ChromaDB integration"
git commit -m "Update README with voice mode instructions"

# Bad
git commit -m "fix bug"
git commit -m "update"
git commit -m "changes"
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

**Example:**
```
feat: Add image generation skill

- Integrate with DALL-E API
- Support custom sizes and quality
- Add image saving functionality

Closes #123
```

## Pull Request Process

1. **Update documentation**
2. **Add tests**
3. **Run all tests**
4. **Update CHANGELOG** (if applicable)
5. **Create PR with description**:
   - What changes were made
   - Why changes were needed
   - How to test changes
   - Related issues

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How to test these changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

## Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, PR will be merged
4. Your contribution will be credited

## Getting Help

- **Questions**: Open a [Discussion](https://github.com/Aptik09/jarvis-v2/discussions)
- **Issues**: Report in [Issues](https://github.com/Aptik09/jarvis-v2/issues)
- **Email**: aptikpandey9@gmail.com

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make JARVIS better for everyone. Thank you for taking the time to contribute!
