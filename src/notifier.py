from pync import notify
import datetime
import logging
from .config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Notifier:
    @staticmethod
    def send_notification(summary_text, sender, subject):
        """Send a desktop notification for a new email."""
        try:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            notify(
                message=f"{summary_text}\n\n{timestamp}",
                title=f"📬 New Email from {sender}",
                subtitle=subject,
                open="https://mail.google.com/mail/u/0/#inbox",
                app_icon=Config.NOTIFICATION_ICON,
                app_id="Gmail Summarizer"
            )
            logger.info("Notification sent successfully.")
        except Exception as e:
            logger.error(f"Notification error: {e}")