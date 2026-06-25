import streamlit as st
import os
from PIL import Image


st.set_page_config(
    page_title="TrivionX",
    layout="wide"
)

logo_path = "assets/Logo.png"

col1, col2 = st.columns([5, 1])
with col1:
    st.title("TrivionX Assistant")
    st.subheader("Your Personal AI Gym & Fitness Companion")
with col2:
    if os.path.exists(logo_path):
        st.image(logo_path, width=130)

st.write("""
Welcome to **TrvionX Assistant**.

I am your personal Fitness companion buddy

### Features


""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.success("BMI Calculator")
    st.write("Calculate your Body Mass Index instantly.")

    st.success("AI Dietician")
    st.write("Generate personalized diet plans using Gemini AI.")

    st.success("AI Chatbot")
    st.write("Ask fitness and nutrition questions.")

with col2:
    st.success("AI Workout Planner")
    st.write("Generate a complete weekly workout routine.")

    st.success("Habit Tracker")
    st.write("Track workouts, streaks and monthly progress.")
st.markdown("---")

st.info("choose an option from the left sidebar")
