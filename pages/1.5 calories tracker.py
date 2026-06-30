import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Calorie Tracker",
    layout="wide"
)

st.title("TrivionX Calorie Tracker")
st.write("Track your daily calorie intake.")

conn = sqlite3.connect(
    "database.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Calories(

    Date TEXT,

    Meal TEXT,

    Food TEXT,

    Calories INTEGER

)
""")

conn.commit()

today = datetime.now().strftime("%Y-%m-%d")

st.subheader("Add Meal")

meal = st.selectbox(
    "Meal",
    [
        "Breakfast",
        "Lunch",
        "Dinner",
        "Snack"
    ]
)

food = st.text_input(
    "Food Name",
    placeholder="Example: Idli"
)

calories = st.number_input(
    "Calories",
    min_value=0,
    max_value=5000,
    value=200
)

if st.button("Add Food"):

    cursor.execute(
        """
        INSERT INTO Calories
        VALUES(?,?,?,?)
        """,
        (
            today,
            meal,
            food,
            calories
        )
    )

    conn.commit()

    st.success("Food Added Successfully!")

df = pd.read_sql_query(
    "SELECT * FROM Calories",
    conn
)

if not df.empty:

    st.divider()

    today_df = df[df["Date"] == today]

    total = today_df["Calories"].sum()

    st.metric(
        "Today's Calories",
        f"{total} kcal"
    )

    st.divider()

    st.subheader("Today's Meals")

    st.dataframe(
        today_df,
        use_container_width=True
    )

    st.divider()

    chart = (
        today_df
        .groupby("Meal")["Calories"]
        .sum()
        .reset_index()
    )

    if not chart.empty:

        fig = px.pie(
            chart,
            names="Meal",
            values="Calories",
            hole=0.45,
            title="Calories by Meal"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    daily = (
        df.groupby("Date")["Calories"]
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        daily,
        x="Date",
        y="Calories",
        markers=True,
        title="Daily Calorie Intake"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    if st.button("Clear Today's Calories"):

        cursor.execute(
            "DELETE FROM Calories WHERE Date=?",
            (today,)
        )

        conn.commit()

        st.success("Today's Data Cleared!")

        st.rerun()

else:

    st.info("No calorie data available.")

conn.close()