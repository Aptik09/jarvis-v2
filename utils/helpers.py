"""
Helper utilities for JARVIS v2.0
"""

import re
import hashlib
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import json


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    if len(filename) > 200:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:200] + (f'.{ext}' if ext else '')
    return filename


def generate_hash(text: str) -> str:
    """
    Generate SHA256 hash of text
    
    Args:
        text: Input text
        
    Returns:
        Hash string
    """
    return hashlib.sha256(text.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def parse_time_string(time_str: str) -> Optional[datetime]:
    """
    Parse natural language time string
    
    Args:
        time_str: Time string (e.g., "in 5 minutes", "tomorrow at 3pm")
        
    Returns:
        Datetime object or None
    """
    now = datetime.now()
    time_str_lower = time_str.lower()

    # Handle relative times
    if "in" in time_str_lower:
        # Extract number and unit
        match = re.search(r'in (\d+) (minute|hour|day|week)s?', time_str_lower)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)

            if unit == "minute":
                return now + timedelta(minutes=amount)
            elif unit == "hour":
                return now + timedelta(hours=amount)
            elif unit == "day":
                return now + timedelta(days=amount)
            elif unit == "week":
                return now + timedelta(weeks=amount)

    # Handle specific times
    if "tomorrow" in time_str_lower:
        target = now + timedelta(days=1)
        # Extract time if specified
        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?', time_str_lower)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            period = time_match.group(3)

            if period == "pm" and hour < 12:
                hour += 12
            elif period == "am" and hour == 12:
                hour = 0

            return target.replace(hour=hour, minute=minute, second=0, microsecond=0)
        return target.replace(hour=9, minute=0, second=0, microsecond=0)

    if "today" in time_str_lower or "tonight" in time_str_lower:
        target = now
        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?', time_str_lower)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            period = time_match.group(3)

            if period == "pm" and hour < 12:
                hour += 12
            elif period == "am" and hour == 12:
                hour = 0

            return target.replace(hour=hour, minute=minute, second=0, microsecond=0)

    return None


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text
    
    Args:
        text: Input text
        
    Returns:
        List of URLs
    """
    url_pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    return re.findall(url_pattern, text)


def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text
    
    Args:
        text: Input text
        
    Returns:
        List of email addresses
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)


def dict_to_pretty_json(data: Dict) -> str:
    """
    Convert dict to pretty JSON string
    
    Args:
        data: Dictionary to convert
        
    Returns:
        Pretty JSON string
    """
    return json.dumps(data, indent=2, ensure_ascii=False)


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    # Simple approximation: 4 characters ≈ 1 token
    return len(text) // 4


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Input text
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks
