import os
from logging import Logger

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
        self._authenticate()

    def _authenticate(self):
        try: 
            # The file token.json stores the user"s access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first time.
            if os.path.exists("secrets/token.json"):
                self.creds = Credentials.from_authorized_user_file("secrets/token.json", self.SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "secrets/credentials.json", self.SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("secrets/token.json", "w") as token:
                token.write(self.creds.to_json())

            self.logger.info("Successfully authenticated Gmail Service.")

        except Exception as e:
            self.logger.error(f"Error while authenticating Gmail Service: {e}", exc_info=True)
            raise

    def _get_service(self):
        if not self.service:
            self.service = build("gmail", "v1", credentials=self.creds)
        return self.service

    def fetch_emails(self, query_tuple: tuple[int,str]) -> list:
        query_id, query = query_tuple
        self.logger.info(f"Fetching emails for query id: {query_id}")

        try:
            service = self._get_service()
            unread_mail = service.users().messages().list(userId="me", q=query).execute()['messages']
            msg_count = len(unread_mail)
            if msg_count > 0:
                self.logger.info(f"Successfully fetched {msg_count} messages for qeury id: {query_id}")
                return unread_mail
            else:
                self.logger.info(f"No new messages for query id: {query_id}")
                return []
        except Exception as e:
            self.logger.error(f"Error fetching messages for [query id: {query_id}]: {e}", exc_info=True)
            return []
    
    def extract_subject(self, msg_id) -> str|None:
        self.logger.info(f"Extracting subject for msg id: {msg_id}")
        try:
            service = self._get_service()
            metadata = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
            headers = metadata["payload"]["headers"]

            subject = None
            for header in headers:
                if header["name"] == "Subject":
                    subject =  header["value"]   

            if subject:
                self.logger.info(f"Subject extracted for msg id: {msg_id}")   
                return subject
            else:
                self.logger.warning(f"No subject header found for msg id: {msg_id}")
                return subject
        except Exception as e:
            self.logger.error(f"Error while extracting subject for [msg id: {msg_id}]: {e}", exc_info=True)
            return None
        