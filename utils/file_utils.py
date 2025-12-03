"""
File utilities for JARVIS v2.0
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


def ensure_directory(directory: str) -> Path:
    """
    Ensure directory exists
    
    Args:
        directory: Directory path
        
    Returns:
        Path object
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_files(directory: str, extension: Optional[str] = None) -> List[str]:
    """
    List files in directory
    
    Args:
        directory: Directory path
        extension: Filter by extension (e.g., '.txt')
        
    Returns:
        List of file paths
    """
    try:
        path = Path(directory)
        if not path.exists():
            return []

        if extension:
            files = list(path.glob(f"*{extension}"))
        else:
            files = [f for f in path.iterdir() if f.is_file()]

        return [str(f) for f in files]

    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return []


def delete_file(filepath: str) -> bool:
    """
    Delete file
    
    Args:
        filepath: File path
        
    Returns:
        Success status
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.debug(f"File deleted: {filepath}")
            return True
        return False

    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return False


def copy_file(source: str, destination: str) -> bool:
    """
    Copy file
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        Success status
    """
    try:
        shutil.copy2(source, destination)
        logger.debug(f"File copied: {source} -> {destination}")
        return True

    except Exception as e:
        logger.error(f"Error copying file: {e}")
        return False


def move_file(source: str, destination: str) -> bool:
    """
    Move file
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        Success status
    """
    try:
        shutil.move(source, destination)
        logger.debug(f"File moved: {source} -> {destination}")
        return True

    except Exception as e:
        logger.error(f"Error moving file: {e}")
        return False


def get_file_size(filepath: str) -> Optional[int]:
    """
    Get file size in bytes
    
    Args:
        filepath: File path
        
    Returns:
        File size or None
    """
    try:
        return os.path.getsize(filepath)
    except Exception as e:
        logger.error(f"Error getting file size: {e}")
        return None


def read_text_file(filepath: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    Read text file
    
    Args:
        filepath: File path
        encoding: File encoding
        
    Returns:
        File content or None
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return None


def write_text_file(
    filepath: str,
    content: str,
    encoding: str = 'utf-8',
    append: bool = False
) -> bool:
    """
    Write text file
    
    Args:
        filepath: File path
        content: Content to write
        encoding: File encoding
        append: Append mode
        
    Returns:
        Success status
    """
    try:
        mode = 'a' if append else 'w'
        with open(filepath, mode, encoding=encoding) as f:
            f.write(content)
        logger.debug(f"File written: {filepath}")
        return True

    except Exception as e:
        logger.error(f"Error writing file: {e}")
        return False


def clean_old_files(directory: str, days: int = 7) -> int:
    """
    Clean files older than specified days
    
    Args:
        directory: Directory path
        days: Age threshold in days
        
    Returns:
        Number of files deleted
    """
    try:
        from datetime import datetime, timedelta
        import time

        cutoff_time = time.time() - (days * 86400)
        deleted_count = 0

        for filepath in list_files(directory):
            if os.path.getmtime(filepath) < cutoff_time:
                if delete_file(filepath):
                    deleted_count += 1

        logger.info(f"Cleaned {deleted_count} old files from {directory}")
        return deleted_count

    except Exception as e:
        logger.error(f"Error cleaning old files: {e}")
        return 0
