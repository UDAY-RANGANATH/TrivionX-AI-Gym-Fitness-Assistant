from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

# Load .env file
load_dotenv()

# Read API Key
api_key = os.getenv("GROQ_API_KEY")

if api_key is None:
    raise ValueError(
        "GROQ_API_KEY not found. Please check your .env file."
    )

# Create LLM
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.5
)