import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class GoogleCalAPI():
    def __init__(self, pathCred = "credentials.json", pathToken = None):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(pathToken):
            self.creds = Credentials.from_authorized_user_file(pathToken, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file(
                    pathCred, SCOPES
                )
                self.creds = self.flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    def getEvents(self, dayStart=datetime.datetime.now(tz=datetime.timezone.utc).isoformat()):
        try:
            service = build("calendar", "v3", credentials=self.creds)

            # Call the Calendar API
            now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
            print("Getting the upcoming 10 events")
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=dayStart,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])

        except HttpError as error:
            print(f"An error occurred: {error}")