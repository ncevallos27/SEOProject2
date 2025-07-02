from pathlib import Path
from dotenv import load_dotenv
import os
import pandas as pd

from modules.GoogleAPI import GoogleAPI
from modules.Database import Database

SQLPATH = "sqlite:///events.db"

# TODO: add Doc String
def main():
    load_dotenv(Path(".env"))
    #GAPI = GoogleAPI(apiKey=os.getenv('GENAI_KEY'))
    

    print("\nPersonal Assistant CLI App\n")
    while True:
        print("1. Create An Event")
        print("2. Organize Calendar")
        print("3. Display Calendar")
        print("4. Quit")
        
        try:
            userInput = int(input("Enter option: "))
            match userInput:
                case 1:
                    continue
                case 2:
                    continue
                case 3:
                    continue
                case 4:
                    # TODO: implement calendar and data base saving
                    break
                case _:
                    print("err: invalid option, try again")
                    continue
        except ValueError:
            print("error: Please enter a valid option")
    

    print("\nGoodBye")


if __name__ == "__main__":
    main()