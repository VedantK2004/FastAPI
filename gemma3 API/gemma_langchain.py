from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyCdBE2hHnytVmloXOIMsI9K9RN1c1uuy8c"

llm = ChatGoogleGenerativeAI(model="gemma-3-27b-it")
result = llm.invoke("Write me a ballad about LangChain")
print(result.content)
