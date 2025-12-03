"""
Voice Interface for JARVIS v2.0
Speech recognition and text-to-speech capabilities
"""

import speech_recognition as sr
import pyttsx3
from typing import Optional
from config.settings import Settings
from interfaces.cli import CLIInterface
from utils.logger import setup_logger

logger = setup_logger(__name__)


class VoiceInterface:
    """Voice interface for JARVIS"""

    def __init__(self, settings: Settings):
        """Initialize voice interface"""
        self.settings = settings
        self.cli = CLIInterface(settings)

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Initialize text-to-speech
        if settings.USE_LOCAL_TTS:
            self.tts_engine = pyttsx3.init()
            self._configure_tts()
        else:
            self.tts_engine = None

        # Wake word
        self.wake_word = "hey jarvis"
        self.listening = False

        logger.info("Voice interface initialized")

    def _configure_tts(self):
        """Configure TTS engine"""
        try:
            # Set properties
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume

            # Try to set a better voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if "female" in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break

        except Exception as e:
            logger.warning(f"TTS configuration warning: {e}")

    def run(self):
        """Run the voice interface"""
        try:
            print("🎤 Voice mode activated")
            self.speak("Voice mode activated. Say 'Hey JARVIS' to start.")

            # Adjust for ambient noise
            with self.microphone as source:
                print("Calibrating for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)

            print(f"Listening for wake word: '{self.wake_word}'")

            while True:
                try:
                    # Listen for wake word
                    if not self.listening:
                        audio = self.listen(timeout=5)
                        if audio:
                            text = self.recognize_speech(audio)
                            if text and self.wake_word in text.lower():
                                print("✓ Wake word detected!")
                                self.speak("Yes, how can I help?")
                                self.listening = True
                        continue

                    # Listen for command
                    print("Listening for command...")
                    audio = self.listen(timeout=10)

                    if not audio:
                        print("No speech detected")
                        self.listening = False
                        continue

                    # Recognize speech
                    text = self.recognize_speech(audio)

                    if not text:
                        self.speak("I didn't catch that. Could you repeat?")
                        continue

                    print(f"You said: {text}")

                    # Check for exit
                    if any(word in text.lower() for word in ["exit", "quit", "goodbye", "stop"]):
                        self.speak("Goodbye! Have a great day!")
                        break

                    # Process command
                    response = self.cli.process_input(text)

                    # Speak response
                    self.speak(response)

                    # Reset listening state
                    self.listening = False

                except KeyboardInterrupt:
                    print("\nStopping voice interface...")
                    self.speak("Shutting down voice interface")
                    break
                except Exception as e:
                    logger.error(f"Voice loop error: {e}")
                    self.speak("I encountered an error. Please try again.")
                    self.listening = False

        except Exception as e:
            logger.error(f"Voice interface error: {e}")
            print(f"Error: {e}")

    def listen(self, timeout: int = 5) -> Optional[sr.AudioData]:
        """
        Listen for audio input
        
        Args:
            timeout: Listening timeout in seconds
            
        Returns:
            Audio data or None
        """
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                return audio
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return None

    def recognize_speech(self, audio: sr.AudioData) -> Optional[str]:
        """
        Recognize speech from audio
        
        Args:
            audio: Audio data
            
        Returns:
            Recognized text or None
        """
        try:
            # Try Google Speech Recognition (free)
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            logger.debug("Speech not understood")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            logger.error(f"Recognition error: {e}")
            return None

    def speak(self, text: str):
        """
        Speak text using TTS
        
        Args:
            text: Text to speak
        """
        try:
            if self.settings.USE_LOCAL_TTS and self.tts_engine:
                # Use local TTS
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Use ElevenLabs or other cloud TTS
                # This would require additional implementation
                print(f"JARVIS: {text}")

        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"JARVIS: {text}")
