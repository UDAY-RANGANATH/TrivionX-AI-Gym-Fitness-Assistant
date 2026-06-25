import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.llm import llm

st.set_page_config(
    page_title="Fitness Habit Tracker",
    layout="wide"
)

st.title(" TrivionX Habit Tracker")
st.write("Log today's workout and track your fitness journey!")
st.divider()
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Workout(

    Date TEXT PRIMARY KEY,

    WorkoutType TEXT,

    Exercise TEXT,

    Sets INTEGER,

    Reps INTEGER,

    Weight REAL,

    Duration INTEGER,

    Calories INTEGER,

    Completed INTEGER

)
""")

conn.commit()
today = datetime.now().strftime("%Y-%m-%d")
st.subheader("Log Today's Workout")

workout = st.selectbox(
    "Workout Type",
    [
        "Chest",
        "Back",
        "Legs",
        "Shoulders",
        "Biceps",
        "Triceps",
        "Abs",
        "Cardio",
        "Yoga",
        "Running",
        "Cycling",
        "Full Body"
    ]
)

exercise = st.text_input(
    "Exercise Name",
    placeholder="Example: Bench Press"
)

sets = st.number_input(
    "Sets",
    min_value=1,
    max_value=20,
    value=4
)

reps = st.number_input(
    "Repetitions",
    min_value=1,
    max_value=100,
    value=12
)

weight = st.number_input(
    "Weight Lifted (kg)",
    min_value=0.0,
    value=40.0,
    step=2.5
)

duration = st.number_input(
    "Workout Duration (minutes)",
    min_value=5,
    max_value=300,
    value=60
)

calories = st.number_input(
    "Calories Burned",
    min_value=0,
    max_value=3000,
    value=450
)

if st.button("Save Today's Workout"):

    cursor.execute("""
    INSERT OR REPLACE INTO Workout
    (
        Date,
        WorkoutType,
        Exercise,
        Sets,
        Reps,
        Weight,
        Duration,
        Calories,
        Completed
    )

    VALUES(?,?,?,?,?,?,?,?,?)
    """,
    (
        today,
        workout,
        exercise,
        sets,
        reps,
        weight,
        duration,
        calories,
        1
    ))

    conn.commit()

    st.success("Workout Saved Successfully!")

df = pd.read_sql_query(
    "SELECT * FROM Workout ORDER BY Date",
    conn
)

if not df.empty:

    total_days = len(df)

    completed = df["Completed"].sum()

    workout_percent = round(
        (completed / total_days) * 100,
        1
    )

    total_calories = df["Calories"].sum()

    streak = 0

    completed_list = df["Completed"].tolist()

    for value in reversed(completed_list):

        if value == 1:
            streak += 1
        else:
            break

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Current Streak",
            f"{streak} Days"
        )

    with col2:
        st.metric(
            "Workout %",
            f"{workout_percent}%"
        )

    with col3:
        st.metric(
            "Calories Burned",
            f"{total_calories} kcal"
        )

    with col4:
        st.metric(
            "Total Workouts",
            completed
        )

    st.divider()
    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = df["Date"].dt.strftime("%b")

    monthly = (
        df.groupby("Month")["Calories"]
        .sum()
        .reset_index()
    )

    st.subheader("Monthly Calories Burned")
    fig = px.bar(
        monthly,
        x="Month",
        y="Calories",
        text="Calories",
        color="Calories"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Calories Burned"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()
    st.subheader("Workout History")
    st.dataframe(
        df.sort_values("Date", ascending=False),
        use_container_width=True
    )

else:

    st.info("No workout history yet. Log today's workout to get started!")

conn.close()