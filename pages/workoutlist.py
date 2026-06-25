import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
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

st.divider()

if st.button("Generate a Workout Plan"):

    prompt = f"""
You are a certified professional fitness trainer.

Create a personalized weekly workout plan.

User Details

Age: {age}

Gender: {gender}

Height: {height} cm

Weight: {weight} kg

Fitness Goal: {goal}

Experience Level: {experience}

Workout Location: {location}

Workout Days: {days}

Workout Duration: {duration} minutes

Generate the response in Markdown format.

Include:

# Weekly Workout Schedule

For each workout day provide:

• Target Muscle Group

• Exercises

• Sets

• Repetitions

• Rest Time

• Warm-up

• Cool-down

Also include:

## Cardio Recommendation

## Stretching Routine

## Recovery Tips

## Beginner Safety Tips

The exercises should match the user's experience level and available equipment.
"""

    with st.spinner("Creating your personalized workout plan..."):

        response = llm.invoke(prompt)

        st.markdown(response.content)

    st.success("Workout Plan Generated Successfully!")

    st.markdown(response.content)