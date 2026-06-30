import streamlit as st
import os
from PIL import Image
import sqlite3
import pandas as pd
import plotly.express as px
import hashlib

st.set_page_config(
    page_title="TrivionX",
    layout="wide"
)

# -----------------------------
# Database
# -----------------------------

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
    Username TEXT PRIMARY KEY,
    Password TEXT
)
""")
conn.commit()


# -----------------------------
# Password Hashing
# -----------------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -----------------------------
# Session State
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# -----------------------------
# Login / Register Page
# -----------------------------

if not st.session_state.logged_in:

    st.title("🏋️ TrivionX Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------------- LOGIN ----------------

    with tab1:

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            cursor.execute(
                "SELECT * FROM Users WHERE Username=? AND Password=?",
                (
                    username,
                    hash_password(password)
                )
            )

            user = cursor.fetchone()

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Username or Password")

    # ---------------- REGISTER ----------------

    with tab2:

        new_username = st.text_input(
            "Create Username"
        )

        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button("Register"):

            cursor.execute(
                "SELECT * FROM Users WHERE Username=?",
                (new_username,)
            )

            exists = cursor.fetchone()

            if exists:

                st.warning("Username already exists")

            else:

                cursor.execute(
                    "INSERT INTO Users VALUES(?,?)",
                    (
                        new_username,
                        hash_password(new_password)
                    )
                )

                conn.commit()

                st.success("Registration Successful!")

    st.stop()

# ====================================================
# MAIN APPLICATION
# ====================================================

logo_path = "assets/Logo.png"

col1, col2 = st.columns([5,1])

with col1:

    st.title("TrivionX Assistant")

    st.subheader(
        f"Welcome {st.session_state.username} 👋"
    )

with col2:

    if os.path.exists(logo_path):
        st.image(
            logo_path,
            width=130
        )

st.write("""
Your Personal AI Gym & Fitness Companion.
""")

# Logout Button

if st.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()

st.markdown("---")

left, right = st.columns([2,1])

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

    try:

        df = pd.read_sql_query(
            "SELECT * FROM Workout",
            conn
        )

        if not df.empty:

            st.metric(
                "Workouts",
                len(df)
            )

            st.metric(
                "Calories",
                f"{df['Calories'].sum()} kcal"
            )

            st.metric(
                "Duration",
                f"{df['Duration'].sum()} min"
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

            st.info(
                "No workout data available yet."
            )

    except:

        st.info(
            "Start logging workouts to view progress."
        )

conn.close()

st.markdown("---")

st.info("Choose an option from the left sidebar.")