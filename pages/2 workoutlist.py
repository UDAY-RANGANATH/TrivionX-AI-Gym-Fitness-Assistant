import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from utils.llm import llm


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.5
)

st.set_page_config(
    page_title="AI Workout Planner",
    layout="wide"
)

st.title("AI Workout Planner")
st.write("Generate a personalized workout routine using AI.")

st.divider()
col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=10,
        max_value=80,
        value=20
    )

    gender = st.radio(
        "Gender",
        ["Male", "Female"]
    )

    height = st.number_input(
        "Height (cm)",
        min_value=100,
        max_value=250,
        value=170
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=20,
        max_value=250,
        value=70
    )

with col2:

    goal = st.selectbox(
        "Fitness Goal",
        [
            "Weight Loss",
            "Muscle Gain",
            "Maintain Fitness",
            "Improve Strength",
            "Improve Endurance"
        ]
    )

    experience = st.selectbox(
        "Workout Experience",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    location = st.selectbox(
        "Workout Location",
        [
            "Gym",
            "Home"
        ]
    )

    days = st.slider(
        "Workout Days Per Week",
        1,
        7,
        5
    )

duration = st.slider(
    "Workout Duration (Minutes)",
    20,
    120,
    60
)

physical_condition = st.radio(
    "Are you physically handicapped?",
    ["No", "Yes"]
)

disability = ""

if physical_condition == "Yes":
    disability = st.text_input(
        "Please describe your physical condition",
        placeholder="Example: Knee injury, Shoulder injury, Wheelchair user..."
    )
st.divider()

if st.button("Generate a Workout Plan"):

    prompt = f"""
    You are a certified fitness trainer.
    
    You are NOT allowed to invent workouts.

    Keep it as short and simple as possible and give the pro tip with it
    
    You must ONLY recommend workouts available in the Workout PDF knowledge base and do not talk about the pdf
    
    Workout Location : {location}
    
    Workout Days : {days}
    
    Workout Duration : {duration}
    
    Physically Handicapped : {physical_condition}
    
    Disability Details : {disability}
    
    Rules
    
    1. ONLY use workouts from the PDF.
    
    2. If the user is physically handicapped,
    remove every exercise that targets the injured body part.
    
    3. Replace those exercises with safer alternatives
    already available inside the PDF.
    
    4. If no safe alternative exists, reply
    
    "No suitable workout exists in the Workout Guide.
    Please consult the AI Chatbot."
    
    Return
    
    Weekly Workout Schedule
    
    Warm-up
    
    Exercises
    
    Sets
    
    Reps
    
    Rest
    
    Cooldown
    
    Safety Tips
    """

    with st.spinner("Creating your personalized workout plan..."):

        response = llm.invoke(prompt)

        st.markdown(response.content)

    st.success("Workout Plan Generated Successfully!")

    st.info("If you want to make any custom modifications with the wokrout plan you can reachout our chabot and paste your given plan and modify it")
