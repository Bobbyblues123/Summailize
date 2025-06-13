import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
    TOKEN_PATH = os.path.join(os.path.dirname(__file__), '..', 'token.json')
    NOTIFICATION_ICON = os.path.join(os.path.dirname(__file__), '..', 'gmailsummarizerlogo.png')
    CHECK_INTERVAL_SECONDS = 10
