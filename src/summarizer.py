import google.generativeai as genai
import logging
from .config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Summarizer:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def summarize_email(self, email_text):
        """Summarize and classify."""
        try:
            prompt = f"""
You are an assistant that summarizes emails and classifies them.

Summarize the following email in 1–2 sentences, then provide a category label from this list: 
["Job Opportunity", "Personal", "Newsletter", "Important", "Promotional", "Gaming", "Messaging", "Other"]

Email:
\"\"\"
{email_text}
\"\"\"

Respond in this format:

Summary: <summary>
Category: <category>
"""
            response = self.model.generate_content(prompt)
            summary_text = response.text.strip()
            summary_lines = summary_text.split("\n")
            category_line = next((line for line in summary_lines if line.startswith("Category:")), "Category: Other")
            category = category_line.replace("Category:", "").strip()
            return summary_text, category
        except Exception as e:
            logger.error(f"Failed to summarize email: {e}")
            return "Summary: Unable to summarize email due to an error.\nCategory: Other", "Other"