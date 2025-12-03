"""
Schedule Skill for JARVIS v2.0
Manages reminders and scheduled tasks
"""

import json
import schedule
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
from skills.base_skill import BaseSkill
from config.settings import Settings
from utils.logger import setup_logger
from utils.helpers import parse_time_string

logger = setup_logger(__name__)


class ScheduleSkill(BaseSkill):
    """Manages reminders and scheduled tasks"""

    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.schedules_file = settings.SCHEDULES_DIR / "schedules.json"
        self.schedules = self._load_schedules()

    def can_handle(self, intent_data: Dict) -> bool:
        """Check if this skill can handle the intent"""
        return "schedule" in intent_data.get("all_intents", [])

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute scheduling action
        
        Args:
            action: Action to perform (create, list, delete)
            **kwargs: Action parameters
            
        Returns:
            Action result
        """
        try:
            if action == "create":
                return self.create_reminder(**kwargs)
            elif action == "list":
                return self.list_reminders()
            elif action == "delete":
                return self.delete_reminder(**kwargs)
            else:
                return self.create_response(
                    success=False,
                    error=f"Unknown action: {action}"
                )

        except Exception as e:
            logger.error(f"Schedule execution error: {e}")
            return self.create_response(
                success=False,
                error=f"Scheduling failed: {str(e)}"
            )

    def create_reminder(
        self,
        message: str,
        time_str: str,
        recurring: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a reminder
        
        Args:
            message: Reminder message
            time_str: Time string (e.g., "in 5 minutes", "tomorrow at 3pm")
            recurring: Whether reminder is recurring
            
        Returns:
            Creation result
        """
        try:
            # Parse time
            target_time = parse_time_string(time_str)
            if not target_time:
                return self.create_response(
                    success=False,
                    error=f"Could not parse time: {time_str}"
                )

            # Create reminder
            reminder = {
                "id": f"reminder_{datetime.now().timestamp()}",
                "message": message,
                "time": target_time.isoformat(),
                "time_str": time_str,
                "recurring": recurring,
                "created_at": datetime.now().isoformat(),
                "status": "pending"
            }

            self.schedules.append(reminder)
            self._save_schedules()

            return self.create_response(
                success=True,
                data=reminder,
                message=f"Reminder set for {target_time.strftime('%Y-%m-%d %H:%M')}"
            )

        except Exception as e:
            logger.error(f"Error creating reminder: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to create reminder: {str(e)}"
            )

    def list_reminders(self, status: str = "all") -> Dict[str, Any]:
        """
        List reminders
        
        Args:
            status: Filter by status (all, pending, completed)
            
        Returns:
            List of reminders
        """
        try:
            if status == "all":
                reminders = self.schedules
            else:
                reminders = [r for r in self.schedules if r.get("status") == status]

            return self.create_response(
                success=True,
                data={"reminders": reminders, "count": len(reminders)},
                message=f"Found {len(reminders)} reminder(s)"
            )

        except Exception as e:
            logger.error(f"Error listing reminders: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to list reminders: {str(e)}"
            )

    def delete_reminder(self, reminder_id: str) -> Dict[str, Any]:
        """
        Delete a reminder
        
        Args:
            reminder_id: Reminder ID
            
        Returns:
            Deletion result
        """
        try:
            original_count = len(self.schedules)
            self.schedules = [r for r in self.schedules if r.get("id") != reminder_id]

            if len(self.schedules) < original_count:
                self._save_schedules()
                return self.create_response(
                    success=True,
                    message="Reminder deleted successfully"
                )
            else:
                return self.create_response(
                    success=False,
                    error=f"Reminder not found: {reminder_id}"
                )

        except Exception as e:
            logger.error(f"Error deleting reminder: {e}")
            return self.create_response(
                success=False,
                error=f"Failed to delete reminder: {str(e)}"
            )

    def check_due_reminders(self) -> List[Dict]:
        """
        Check for due reminders
        
        Returns:
            List of due reminders
        """
        try:
            now = datetime.now()
            due_reminders = []

            for reminder in self.schedules:
                if reminder.get("status") != "pending":
                    continue

                reminder_time = datetime.fromisoformat(reminder["time"])
                if reminder_time <= now:
                    due_reminders.append(reminder)

                    # Update status
                    if not reminder.get("recurring"):
                        reminder["status"] = "completed"

            if due_reminders:
                self._save_schedules()

            return due_reminders

        except Exception as e:
            logger.error(f"Error checking due reminders: {e}")
            return []

    def _load_schedules(self) -> List[Dict]:
        """Load schedules from file"""
        try:
            if self.schedules_file.exists():
                with open(self.schedules_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading schedules: {e}")
            return []

    def _save_schedules(self) -> None:
        """Save schedules to file"""
        try:
            with open(self.schedules_file, 'w') as f:
                json.dump(self.schedules, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving schedules: {e}")
