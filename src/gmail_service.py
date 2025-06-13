import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import logging
from .config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GmailService:
    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):
        try:
            creds = None 
            if os.path.exists(Config.TOKEN_PATH):
                creds = Credentials.from_authorized_user_file(Config.TOKEN_PATH, Config.SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(Config.CREDENTIALS_PATH, Config.SCOPES)
                    creds = flow.run_local_server(port=0)
                with open(Config.TOKEN_PATH, 'w') as token:
                    token.write(creds.to_json())
            return build('gmail', 'v1', credentials=creds)
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise

    def get_or_create_label(self, label_name):
        label_name = label_name.lower()
        try:
            labels = self.service.users().labels().list(userId='me').execute().get('labels', [])
            for label in labels:
                if label['name'].lower() == label_name:
                    return label['id']
            new_label = self.service.users().labels().create(
                userId='me',
                body={
                    'name': label_name.capitalize(),
                    'labelListVisibility': 'labelShow',
                    'messageListVisibility': 'show'
                }
            ).execute()
            return new_label['id']
        except Exception as e:
            logger.error(f"Failed to get or create label {label_name}: {e}")
            raise

    def read_latest_email(self, last_message_id):
        try:
            results = self.service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=1).execute()
            messages = results.get('messages', [])
            if not messages:
                logger.info("No new messages.")
                return None, last_message_id

            message_id = messages[0]['id']
            if message_id == last_message_id:
                logger.info("Same message. Skipping.")
                return None, last_message_id

            msg = self.service.users().messages().get(userId='me', id=message_id, format='full').execute()
            payload = msg['payload']
            headers = payload.get("headers", [])

            subject = sender = None
            for header in headers:
                if header['name'] == 'From':
                    sender = header['value']
                if header['name'] == 'Subject':
                    subject = header['value']

            body = self._get_message_body(payload)
            if body and body.strip().startswith("<"):
                soup = BeautifulSoup(body, 'html.parser')
                body = soup.get_text()

            return {
                'message_id': message_id,
                'subject': subject,
                'sender': sender,
                'body': body
            }, message_id
        except Exception as e:
            logger.error(f"Failed to read latest email: {e}")
            return None, last_message_id

    def _get_message_body(self, payload):
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    return base64.urlsafe_b64decode(part['body']['data']).decode()
                elif 'parts' in part:
                    result = self._get_message_body(part)
                    if result:
                        return result
        elif 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode()
        return ""

    def label_email(self, message_id, category):
        try:
            system_labels = ["IMPORTANT", "SPAM", "TRASH", "STARRED", "UNREAD", "INBOX"]
            label_ids = ['INBOX']
            category = category if not category.lower().startswith("other") else "Other"
            if category.upper() in system_labels:
                label_ids.append(category.upper())
            else:
                custom_label_id = self.get_or_create_label(category)
                label_ids.append(custom_label_id)

            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={
                    'addLabelIds': label_ids,
                    'removeLabelIds': ['UNREAD']
                }
            ).execute()
            logger.info(f"Labeled email {message_id} with {label_ids}")
        except Exception as e:
            logger.error(f"Failed to label email {message_id}: {e}")