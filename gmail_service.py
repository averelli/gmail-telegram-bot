import os
from logging import Logger
from config import GMAIL_TOKEN_PATH, GMAIL_CREDS_PATH

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GmailService:
    def __init__(self, logger: Logger):
        self.creds = None
        self.service = None
        self.logger = logger
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
        self.CREDS_PATH = GMAIL_CREDS_PATH
        self.TOKEN_PATH = GMAIL_TOKEN_PATH
        self._authenticate()

    def _authenticate(self):
        try: 
            # The file token.json stores the user"s access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first time.
            if os.path.exists(self.TOKEN_PATH):
                self.creds = Credentials.from_authorized_user_file(self.TOKEN_PATH, self.SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.CREDS_PATH, self.SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.TOKEN_PATH, "w") as token:
                token.write(self.creds.to_json())

            self.logger.info("Successfully authenticated Gmail Service.")

        except Exception as e:
            self.logger.error(f"Error while authenticating Gmail Service: {e}", exc_info=True)
            raise

    def _get_service(self):
        if not self.service:
            self.service = build("gmail", "v1", credentials=self.creds)
        return self.service

    def fetch_emails(self, query_id:int, query:str) -> list:
        self.logger.info(f"[Query id: {query_id}] Started fetching emails")
        try:
            service = self._get_service()
            unread_mail = service.users().messages().list(userId="me", q=query).execute().get("messages", [])
            msg_count = len(unread_mail)
            if msg_count > 0:
                self.logger.info(f"[Query id: {query_id}] Successfully fetched {msg_count} messages")
                return unread_mail
            else:
                self.logger.info(f"[Query id: {query_id}] No new messages found")
                return []
        except Exception as e:
            self.logger.error(f"[Query id: {query_id}] Error fetching messages: {e}", exc_info=True)
            return []
    
    def extract_subject(self, msg_id) -> str|None:
        self.logger.info(f"[msg id: {msg_id}] Starting subject extraction")
        try:
            service = self._get_service()
            metadata = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
            headers = metadata["payload"]["headers"]

            subject = None
            for header in headers:
                if header["name"] == "Subject":
                    subject =  header["value"]   

            if subject:
                self.logger.info(f"[msg id: {msg_id}] Subject extracted")   
                return subject
            else:
                self.logger.warning(f"[msg id: {msg_id}] No subject header found")
                return subject
        except Exception as e:
            self.logger.error(f"[msg id: {msg_id}] Error while extracting subject: {e}", exc_info=True)
            return None
        