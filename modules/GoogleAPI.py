from google import genai
from google.genai import types
import os

class GoogleAPI():
    def __init__(self, apiKey=None, model="gemini-2.5-flash"):
        self.key = apiKey
        self.model = model

        genai.api_key = self.key
        self.client = genai.Client(api_key=self.key)

    def getResponse(self, input=None, context=None):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
            system_instruction=context
            ),
            contents=input,
        )

        # print(response.text)

        return response

    