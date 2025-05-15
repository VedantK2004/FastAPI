from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")

os.environ["GOOGLE_API_KEY"] = GEMMA_API_KEY

llm = ChatGoogleGenerativeAI(model="gemma-3-27b-it")
result = llm.invoke("Write a python script to generate a chatbot using langchaina nd openai")
print(result.content)
