import schedule
import time
import logging
from .gmail_service import GmailService
from .summarizer import Summarizer
from .notifier import Notifier
from .config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GmailSummarizer:
    def __init__(self):
        self.gmail_service = GmailService()
        self.summarizer = Summarizer()
        self.notifier = Notifier()
        self.last_message_id = None

    def job(self):
        try:
            email_data, new_message_id = self.gmail_service.read_latest_email(self.last_message_id)
            if email_data:
                self.last_message_id = new_message_id
                summary_text, category = self.summarizer.summarize_email(email_data['body'])
                logger.info(summary_text)
                self.gmail_service.label_email(email_data['message_id'], category)
                self.notifier.send_notification(summary_text, email_data['sender'], email_data['subject'])
        except Exception as e:
            logger.error(f"Error in job execution: {e}")

    def run(self):
        schedule.every(Config.CHECK_INTERVAL_SECONDS).seconds.do(self.job)
        logger.info(f"Starting Gmail Summarizer, checking every {Config.CHECK_INTERVAL_SECONDS} seconds.")
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    summarizer = GmailSummarizer()
    summarizer.run()