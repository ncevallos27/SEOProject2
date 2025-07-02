import os
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(Path(".env"))

# Set environment variables
my_api_key = os.getenv('GENAI_KEY')

genai.api_key = my_api_key


# Create an genAI client using the key from our environment variable
client = genai.Client(
    api_key=my_api_key,
)

# Specify the model to use and the messages to send
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
      system_instruction="You are a university instructor and can explain programming concepts clearly in a few words."
    ),
    contents="What are the advantages of pair programming?",
)

print(response.text)
# WRITE YOUR CODE HERE