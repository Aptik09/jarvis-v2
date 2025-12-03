"""
Audio utilities for JARVIS v2.0
"""

import os
from pathlib import Path
from typing import Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


def save_audio(audio_data: bytes, filename: str, directory: str = "temp_audio") -> str:
    """
    Save audio data to file
    
    Args:
        audio_data: Audio bytes
        filename: Output filename
        directory: Output directory
        
    Returns:
        Path to saved file
    """
    try:
        # Create directory
        audio_dir = Path(directory)
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Save file
        filepath = audio_dir / filename
        with open(filepath, 'wb') as f:
            f.write(audio_data)

        logger.debug(f"Audio saved: {filepath}")
        return str(filepath)

    except Exception as e:
        logger.error(f"Error saving audio: {e}")
        raise


def load_audio(filepath: str) -> bytes:
    """
    Load audio from file
    
    Args:
        filepath: Path to audio file
        
    Returns:
        Audio bytes
    """
    try:
        with open(filepath, 'rb') as f:
            audio_data = f.read()

        logger.debug(f"Audio loaded: {filepath}")
        return audio_data

    except Exception as e:
        logger.error(f"Error loading audio: {e}")
        raise


def delete_audio(filepath: str) -> bool:
    """
    Delete audio file
    
    Args:
        filepath: Path to audio file
        
    Returns:
        Success status
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.debug(f"Audio deleted: {filepath}")
            return True
        return False

    except Exception as e:
        logger.error(f"Error deleting audio: {e}")
        return False


def get_audio_duration(filepath: str) -> Optional[float]:
    """
    Get audio file duration in seconds
    
    Args:
        filepath: Path to audio file
        
    Returns:
        Duration in seconds or None
    """
    try:
        import wave
        with wave.open(filepath, 'r') as audio_file:
            frames = audio_file.getnframes()
            rate = audio_file.getframerate()
            duration = frames / float(rate)
            return duration

    except Exception as e:
        logger.error(f"Error getting audio duration: {e}")
        return None


def convert_audio_format(
    input_path: str,
    output_path: str,
    output_format: str = "wav"
) -> bool:
    """
    Convert audio file format
    
    Args:
        input_path: Input file path
        output_path: Output file path
        output_format: Output format (wav, mp3, etc.)
        
    Returns:
        Success status
    """
    try:
        from pydub import AudioSegment

        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=output_format)

        logger.debug(f"Audio converted: {input_path} -> {output_path}")
        return True

    except ImportError:
        logger.warning("pydub not installed, audio conversion unavailable")
        return False
    except Exception as e:
        logger.error(f"Error converting audio: {e}")
        return False
