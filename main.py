import datetime
import os.path
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google import genai
from google.genai import types

SQLPATH = "sqlite:///events.db"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def insert_calendar_event(event_data, creds, calendar_id="primary"):
    """
    Inserts a user event into the specified Google Calendar.

    Parameters:
        event_data (dict): A dictionary representing the event to insert.
        creds (google.oauth2.credentials.Credentials): Authorized credentials to access the Google Calendar API.
        calendar_id (str): The ID of the calendar to insert the event into. Defaults to 'primary'.

    Returns:
        None

    Side Effects:
        Prints the URL of the created event to the console if successful.
        Prints an error message if the event insertion fails.
    """

    try:
        service = build("calendar", "v3", credentials=creds)

        event = (
            service.events().insert(calendarId=calendar_id, body=event_data).execute()
        )
        print(f'Event created: {event.get("htmlLink")}')

    except HttpError as error:
        print(f"An error occurred: {error}")


def list_calendar_event(creds, quantity=10):
    """
    Retrieves a list of upcoming events from the user's Google Calendar.

    Parameters:
        creds (google.oauth2.credentials.Credentials): Authorized credentials to access the Google Calendar API.
        quantity (int): The number of upcoming events to retrieve. Defaults to 10.

    Returns:
        list[dict]: A list of events, where each event is a dictionary containing the start time and summary.

    Side Effects:
        Prints each event's start time and summary to the console.
        Prints a message if no upcoming events are found or if an API error occurs.
    """
    
    try:
        service = build("calendar", "v3", credentials=creds)

        # Calling the Calendar API
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        print(f"Getting the upcoming {quantity} event(s)")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=quantity,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")

        event_list = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            print(start, event["summary"])
            event_list.append({"start" : start, "summary" : event.get("summary", "no title"), "end":end})
        return event_list
    except HttpError as error:
        print(f"An error occurred: {error}")


# Google Gen Ai Function Declarations
insert_calendar_event_function = {
    "name": "insert_calendar_event",
    "description": "Inserts a user provided event into their calendar",
    "parameters": {
        "type": "object",
        "properties": {
            "event_data": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "description": "Summary of event."},
                    "location": {"type": "string", "description": "Location of event."},
                    "description": {
                        "type": "string",
                        "description": "Descriptive summary of the event and its purpose.",
                    },
                    "start": {
                        "type": "object",
                        "properties": {
                            "dateTime": {
                                "type": "string",
                                "description": "Date of the event in YYYY-MM-DDTHH:MM:SS-OFFSET format",
                            },
                            "timeZone": {
                                "type": "string",
                                "description": "Timezone of the event.",
                            },
                        },
                        "required": ["dateTime", "timeZone"],
                    },
                    "end": {
                        "type": "object",
                        "properties": {
                            "dateTime": {
                                "type": "string",
                                "description": "Date of the event in YYYY-MM-DDTHH:MM:SS-OFFSET format",
                            },
                            "timeZone": {
                                "type": "string",
                                "description": "Timezone of the event.",
                            },
                        },
                        "required": ["dateTime", "timeZone"],
                    },
                    "attendees": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "email": {
                                    "type": "string",
                                    "description": "Email of an attendee.",
                                },
                            },
                            "required": ["email"],
                        },
                        "description": "List of attendees for the event, each with an email property.",
                    },
                    "reminders": {
                        "type": "object",
                        "properties": {
                            "useDefault": {
                                "type": "boolean",
                                "description": "Whether to use default reminders for the calendar.",
                            },
                            "overrides": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "method": {
                                            "type": "string",
                                            "description": "Method for the reminder (e.g., 'email', 'popup').",
                                        },
                                        "minutes": {
                                            "type": "integer",
                                            "description": "Number of minutes before the event to send the reminder.",
                                        },
                                    },
                                    "required": ["method", "minutes"],
                                },
                            },
                        },
                    },
                },
                "required": ["summary", "start", "end"],
            },
            "calendar_id": {
                "type": "string",
                "description": "Identifier of the calendar. Defaults to 'primary'.",
            },
        },
        "required": ["event_data"],
    },
}

list_calendar_event_function = {
    "name": "list_calendar_event",
    "description": "Lists the events on the calendar and displays them to the user",
    "parameters": {
        "type": "object",
        "properties" : {
            "quantity" : {
            'type' : 'integer',
            'description' : "number of events to list. Defaults to '10'."
            },
        },
        "required" : ["quantity"],
    },  
}


def main():
    """
    Handles authentication, initializes the GenAI client, and manages an interactive loop
    for user prompts. The function supports inserting and listing Google Calendar events
    via natural language through Gemini AI.
    """
    
    load_dotenv()  # reads .env by default (no need for Path module)
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    event_data = list_calendar_event(creds=creds, quantity=10)

    # Config client and tools
    client = genai.Client()
    tools = types.Tool(function_declarations=[insert_calendar_event_function, list_calendar_event_function])
    config = types.GenerateContentConfig(tools=[tools])

    context = ""
    for event in event_data:
        context+=str(f"{event["start"]}->{event["end"]}:{event["summary"]}\n")

    history = [
        types.Content(
            role="model",
            parts=[types.Part(text=f"Here are the upcoming events on the user's calendar to take into account when creating new events and listing events:\n{context}")]
    )]  # convo history

    while True:
        user_input = input("Enter prompt (q to quit): ")

        if user_input.lower() == 'q':
            print("Goodbye")
            return
        
        history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))

        # Send request with function declarations
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history,
            config=config,
        )

        # Check for function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            print(f"Calling {function_call.name}()")
            # print(f"Arguments: {function_call.args}")
            match function_call.name:
                case 'list_calendar_event':
                    result = list_calendar_event(**function_call.args, creds=creds)
                    continue
                case 'insert_calendar_event':
                    result = insert_calendar_event(**function_call.args, creds=creds)
                    continue

            # print(f"result: {result}")
            history.append(types.Content(role='model', parts=[types.Part(function_response=types.FunctionResponse(name=function_call.name, response=result))]))
            #print(history)
        else:
            model_text_response = response.candidates[0].content.parts[0].text
            print(model_text_response)
            history.append(
                types.Content(
                    role="model", parts=[types.Part(text=model_text_response)]
                )
            )

if __name__ == "__main__":
    main()
