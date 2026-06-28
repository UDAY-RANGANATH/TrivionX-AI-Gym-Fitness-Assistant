import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load local .env (works on your computer)
load_dotenv()

api_key = None

# Try Streamlit Secrets first
try:
    import streamlit as st
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

# Fallback to local .env
if api_key is None:
    api_key = os.getenv("GROQ_API_KEY")

# Final check
if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Add it to Streamlit Secrets or your local .env file."
    )

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.5,
)