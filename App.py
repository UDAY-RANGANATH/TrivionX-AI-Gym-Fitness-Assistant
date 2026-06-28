import streamlit as st
import os
from PIL import Image
import sqlite3
import pandas as pd
import plotly.express as px

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
Welcome to **TrivionX Assistant**.

Your personal AI-powered fitness companion.

### Features
""")

st.markdown("---")
left, right = st.columns([2, 1])

with left:

    st.success("BMI Calculator")
    st.write("Calculate your Body Mass Index instantly.")

    st.success("AI Dietician")
    st.write("Generate personalized Indian diet plans.")

    st.success("AI Workout Planner")
    st.write("Generate weekly workout routines.")

    st.success("AI Chatbot")
    st.write("Ask health and fitness questions.")

    st.success("Habit Tracker")
    st.write("Track workouts, calories and progress.")

with right:

    st.subheader("Your Fitness Progress")

    conn = sqlite3.connect("database.db")

    try:
        df = pd.read_sql_query(
            "SELECT * FROM Workout",
            conn
        )

        if not df.empty:

            total_workouts = len(df)
            total_calories = df["Calories"].sum()
            total_duration = df["Duration"].sum()

            st.metric(
                " Workouts",
                total_workouts
            )

            st.metric(
                " Calories",
                f"{total_calories} kcal"
            )

            st.metric(
                " Duration",
                f"{total_duration} min"
            )

            chart = (
                df.groupby("WorkoutType")
                .size()
                .reset_index(name="Count")
            )

            fig = px.pie(
                chart,
                names="WorkoutType",
                values="Count",
                hole=0.45,
                title="Workout Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No workout data available yet.")

    except Exception:

        st.info("Start logging workouts to view progress.")

    conn.close()

st.markdown("---")

st.info(" Choose an option from the left sidebar.")