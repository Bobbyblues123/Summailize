import unittest
from unittest.mock import MagicMock, patch
from src.summarizer import Summarizer

class TestSummarizer(unittest.TestCase):
    def setUp(self):
        patcher = patch('google.generativeai.GenerativeModel')
        self.addCleanup(patcher.stop)
        mock_model_class = patcher.start()

        self.mock_model_instance = MagicMock()
        mock_model_class.return_value = self.mock_model_instance

        self.summarizer = Summarizer()

    def test_summarizer_category_JobOpp(self):
        self.mock_model_instance.generate_content.return_value.text = (
            "Summary: Exciting job opportunities in data science and AI.\n"
            "Category: Job Opportunity"
        )
        email_text = "Your Job Alerts for Monday, June 2 ... DataAnnotation Postdoctoral Biology Associate ..."
        summary_text, category = self.summarizer.summarize_email(email_text)
        self.assertEqual(category, "Job Opportunity")

    def test_summarizer_category_Promotion(self):
        self.mock_model_instance.generate_content.return_value.text = (
            "Summary: Big sale alert with 50% off electronics!\n"
            "Category: Promotion"
        )
        email_text = "Big Summer Sale! 50% off on electronics. Limited time offer, shop now at BestBuy."
        summary_text, category = self.summarizer.summarize_email(email_text)
        self.assertEqual(category, "Promotion")

    def test_summarizer_category_Newsletter(self):
        self.mock_model_instance.generate_content.return_value.text = (
            "Summary: Weekly updates on AI and data science.\n"
            "Category: Newsletter"
        )
        email_text = "Welcome to our weekly article! Here's what's new in the world of AI and data science..."
        summary_text, category = self.summarizer.summarize_email(email_text)
        self.assertEqual(category, "Newsletter")

    def test_summarizer_category_Event(self):
        self.mock_model_instance.generate_content.return_value.text = (
            "Summary: You're invited to a webinar on ML in healthcare.\n"
            "Category: Event"
        )
        email_text = "You're invited to our upcoming webinar on machine learning applications in healthcare..."
        summary_text, category = self.summarizer.summarize_email(email_text)
        self.assertEqual(category, "Event")

    def test_summarizer_category_Other(self):
        self.mock_model_instance.generate_content.return_value.text = (
            "Summary: Following up on meeting notes and next week's schedule.\n"
            "Category: Other"
        )
        email_text = "Hello, I just wanted to follow up on our meeting notes and see when you're available next week."
        summary_text, category = self.summarizer.summarize_email(email_text)
        self.assertEqual(category, "Other")

    def test_summarizer_category_Gaming(self):
        self.mock_model_instance.generate_content.return_value.text = (
            "Summary: New releases and discounts on top gaming titles.\n"
            "Category: Gaming"
        )
        email_text = "Get the latest deals on gaming laptops and pre-order Call of Duty: Modern Warfare 4 now!"
        summary_text, category = self.summarizer.summarize_email(email_text)
        self.assertEqual(category, "Gaming")
