"""
Image Generation Skill for JARVIS v2.0
Generates images using AI models
"""

import openai
from typing import Dict, Any
from pathlib import Path
from skills.base_skill import BaseSkill
from config.settings import Settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageSkill(BaseSkill):
    """Generates images using AI"""

    def __init__(self, settings: Settings):
        super().__init__(settings)
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.IMAGE_MODEL
        self.size = settings.IMAGE_SIZE
        self.quality = settings.IMAGE_QUALITY
        self.images_dir = settings.FILES_DIR / "images"
        self.images_dir.mkdir(exist_ok=True)

    def can_handle(self, intent_data: Dict) -> bool:
        """Check if this skill can handle the intent"""
        return "image" in intent_data.get("all_intents", [])

    def execute(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Generate image
        
        Args:
            prompt: Image description
            **kwargs: Additional parameters
            
        Returns:
            Generation result
        """
        try:
            if not prompt:
                return self.create_response(
                    success=False,
                    error="Image prompt is required"
                )

            # Generate image
            response = openai.images.generate(
                model=self.model,
                prompt=prompt,
                size=kwargs.get("size", self.size),
                quality=kwargs.get("quality", self.quality),
                n=1
            )

            image_url = response.data[0].url

            # Optionally download and save
            if kwargs.get("save", False):
                import requests
                from datetime import datetime

                filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                filepath = self.images_dir / filename

                img_response = requests.get(image_url)
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)

                return self.create_response(
                    success=True,
                    data={
                        "url": image_url,
                        "filepath": str(filepath),
                        "prompt": prompt
                    },
                    message="Image generated and saved"
                )

            return self.create_response(
                success=True,
                data={"url": image_url, "prompt": prompt},
                message="Image generated successfully"
            )

        except Exception as e:
            logger.error(f"Image generation error: {e}")
            return self.create_response(
                success=False,
                error=f"Image generation failed: {str(e)}"
            )
