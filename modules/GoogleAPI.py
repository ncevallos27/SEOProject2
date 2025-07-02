from google import genai
from google.genai import types
import os


class GoogleAPI():
    def __init__(self, apiKey=os.getenv('GENAI_KEY'), model="gemini-2.5-flash"):
        self.key = apiKey
        self.model = model

        genai.api_key = self.key
        self.client = genai.Client(api_key=self.key)

    def getResponse(self):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
            system_instruction="You are a university instructor and can explain programming concepts clearly in a few words."
            ),
            contents="What are the advantages of pair programming?",
        )

        print(response.text)

        return response

    