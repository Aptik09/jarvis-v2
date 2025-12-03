"""
File Skill for JARVIS v2.0
Handles file operations including PDF creation
"""

from typing import Dict, Any
from pathlib import Path
from skills.base_skill import BaseSkill
from config.settings import Settings
from utils.logger import setup_logger
from utils.file_utils import write_text_file, sanitize_filename

logger = setup_logger(__name__)


class FileSkill(BaseSkill):
    """Handles file operations"""

    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.files_dir = settings.FILES_DIR

    def can_handle(self, intent_data: Dict) -> bool:
        """Check if this skill can handle the intent"""
        return "file" in intent_data.get("all_intents", [])

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute file operation
        
        Args:
            action: Action to perform (create_text, create_pdf)
            **kwargs: Action parameters
            
        Returns:
            Action result
        """
        try:
            if action == "create_text":
                return self.create_text_file(**kwargs)
            elif action == "create_pdf":
                return self.create_pdf(**kwargs)
            else:
                return self.create_response(
                    success=False,
                    error=f"Unknown action: {action}"
                )

        except Exception as e:
            logger.error(f"File operation error: {e}")
            return self.create_response(
                success=False,
                error=f"File operation failed: {str(e)}"
            )

    def create_text_file(
        self,
        content: str,
        filename: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a text file
        
        Args:
            content: File content
            filename: Output filename
            
        Returns:
            Creation result
        """
        try:
            if not content:
                return self.create_response(
                    success=False,
                    error="Content is required"
                )

            # Generate filename if not provided
            if not filename:
                from datetime import datetime
                filename = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            # Sanitize filename
            filename = sanitize_filename(filename)
            filepath = self.files_dir / filename

            # Write file
            success = write_text_file(str(filepath), content)

            if success:
                return self.create_response(
                    success=True,
                    data={"filepath": str(filepath), "filename": filename},
                    message=f"Text file created: {filename}"
                )
            else:
                return self.create_response(
                    success=False,
                    error="Failed to write file"
                )

        except Exception as e:
            logger.error(f"Error creating text file: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to create text file: {str(e)}"
            )

    def create_pdf(
        self,
        content: str,
        filename: str = None,
        title: str = "Document",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a PDF file
        
        Args:
            content: PDF content
            filename: Output filename
            title: Document title
            
        Returns:
            Creation result
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch

            if not content:
                return self.create_response(
                    success=False,
                    error="Content is required"
                )

            # Generate filename if not provided
            if not filename:
                from datetime import datetime
                filename = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            # Sanitize filename
            filename = sanitize_filename(filename)
            if not filename.endswith('.pdf'):
                filename += '.pdf'

            filepath = self.files_dir / filename

            # Create PDF
            doc = SimpleDocTemplate(str(filepath), pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Add title
            title_style = styles['Title']
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 0.2 * inch))

            # Add content
            body_style = styles['BodyText']
            for paragraph in content.split('\n\n'):
                if paragraph.strip():
                    story.append(Paragraph(paragraph, body_style))
                    story.append(Spacer(1, 0.1 * inch))

            # Build PDF
            doc.build(story)

            return self.create_response(
                success=True,
                data={"filepath": str(filepath), "filename": filename},
                message=f"PDF created: {filename}"
            )

        except ImportError:
            return self.create_response(
                success=False,
                error="reportlab not installed. Install with: pip install reportlab"
            )
        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to create PDF: {str(e)}"
            )
