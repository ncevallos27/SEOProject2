import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

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

        self.service = build("calendar", "v3", credentials=self.creds)

    def getEvents(self, dayStart=datetime.datetime.now(tz=datetime.timezone.utc).isoformat()):
        try:
            # Call the Calendar API
            now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
            print("Getting the upcoming 10 events")
            events_result = (
                self.service.events()
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

        except Exception as error:
            print(f"An error occurred: {error}")

    def createEvent(self, eventDict=None):
        # Refer to the Python quickstart on how to setup the environment:
        # https://developers.google.com/workspace/calendar/quickstart/python
        # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
        # stored credentials.

        # event = {
        # 'summary': 'Google I/O 2015',
        # # 'location': '800 Howard St., San Francisco, CA 94103',
        # 'description': 'A chance to hear more about Google\'s developer products.',
        # 'start': {
        #     'dateTime': '2017-05-28T09:00:00-07:00',
        #     # 'timeZone': 'America/Los_Angeles',
        # },
        # 'end': {
        #     'dateTime': '2017-05-28T17:00:00-07:00',
        #     # 'timeZone': 'America/Los_Angeles',
        # },
        # # 'recurrence': [
        # #     'RRULE:FREQ=DAILY;COUNT=2'
        # # ],
        # # 'attendees': [
        # #     {'email': 'lpage@example.com'},
        # #     {'email': 'sbrin@example.com'},
        # # ],
        # # 'reminders': {
        # #     'useDefault': False,
        # #     'overrides': [
        # #     {'method': 'email', 'minutes': 24 * 60},
        # #     {'method': 'popup', 'minutes': 10},
        # #     ],
        # # },
        # }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            return event.get('htmlLink')
        except Exception as error:
            print(f"An error occurred: {error}")
            return None

        
