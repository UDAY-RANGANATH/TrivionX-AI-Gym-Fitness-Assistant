import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from PIL import Image
from utils.llm import llm

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.5
)

logo_path = """assets\Logo2.png"""

if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=180)

st.set_page_config(
    page_title="AI Fitness Chatbot",
    page_icon=""
)

st.title("TrivionX Chatbot")
st.write("You can ask me anything about fitness, workouts, nutrition and healthy living!")

st.divider()


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello there! I'm your AI Fitness Coach. Ask me anything about workouts, diet, calories, supplements, or healthy habits."
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Type your question...")

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    history = ""

    for msg in st.session_state.messages:
        history += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
    You are TrivionX, a expert AI Fitness Coach.
    
    Your expertise includes:
    
    • Weight Loss
    • Muscle Gain
    • Bodybuilding
    • Cardio
    • Nutrition
    • Supplements
    • Yoga
    • Home Workouts
    • Gym Exercises
    • Calories
    • Protein
    • Healthy Lifestyle
    
    Rules:
    
    1. Be friendly.
    
    2. Give practical advice.
    
    3. Explain simply.
    
    4. Motivate the user.
    
    5. If asked about dangerous medical conditions, advise consulting a doctor.
    
    Conversation:
    
    {history}
    
    User:
    
    {user_input}
    """

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = llm.invoke(prompt)

            st.markdown(response.content)

            answer = response.content

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )