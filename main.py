from pathlib import Path
from dotenv import load_dotenv
import os
import pandas as pd

from modules.GoogleAPI import GoogleAPI
from modules.Database import Database
from modules.Agent import Agent
from modules.GoogleCalAPI import GoogleCalAPI

SQLPATH = "sqlite:///events.db"

# TODO: add Doc String
def main():
    load_dotenv(Path(".env"))

    gcapi = GoogleCalAPI(pathCred=Path("credentials.json").resolve(), pathToken=Path("token.json").resolve())
    gapi = GoogleAPI(apiKey=os.getenv('GENAI_KEY'))
    dbase = Database(path=SQLPATH)
    agent = Agent(gapi, dbase, gcapi)

    print("\nPersonal Assistant CLI App\n")
    print("Type q to quit or h for help")
    while True:
        userInput = input("[APP NAME] Enter what you would like me to do: ")
        match userInput.lower():
            case 'q':
                break
            case 'h':
                print("\nHelp Screen")
                continue
            case _:
                answer = agent.getAnswer(userInput)
                
                continue


    print("\nGoodBye")


if __name__ == "__main__":
    main()