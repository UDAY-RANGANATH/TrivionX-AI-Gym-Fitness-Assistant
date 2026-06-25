from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

env_path = Path(__file__).resolve().parent.parent / ".env"

print("Looking for:", env_path)
print("Exists:", env_path.exists())

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")

print("API Key:", api_key)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=api_key,
    temperature=0.5,
)