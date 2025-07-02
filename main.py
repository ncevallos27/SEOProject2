from pathlib import Path
from dotenv import load_dotenv
from modules.GoogleAPI import GoogleAPI

# TODO: add Doc String
def main():
    load_dotenv(Path(".env"))

    GAPI = GoogleAPI()
    print(GAPI.getResponse())


if __name__ == "__main__":
    main()