
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")

client = genai.Client(api_key=GEMMA_API_KEY)

response = client.models.generate_content(
    model="gemma-3-12b-it",
    contents="Write a python script to generate a chatbot using langchaina nd openai",
)

print(response.text)