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

def calculate_bmi(weight, height):
    height = height / 100
    bmi = weight / (height ** 2)
    return round(bmi, 1)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_calories(age, height, weight, gender, goal):
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    calories = bmr * 1.55

    if goal == "Weight Loss":
        calories -= 500

    elif goal == "Muscle Gain":
        calories += 300

    return round(calories)


st.title("AI Dietician")
st.write("Fill in your details to generate a personalized AI diet plan.")
st.divider()

age = st.number_input(
    "Age",
    min_value=10,
    max_value=100,
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

goal = st.selectbox(
    "Fitness Goal",
    [
        "Weight Loss",
        "Muscle Gain",
        "Maintain Weight"
    ]
)

food = st.radio(
    "Food Preference",
    [
        "Vegetarian",
        "Non-Vegetarian"
    ]
)

bmi = calculate_bmi(weight, height)
category = bmi_category(bmi)

daily_calories = calculate_calories(
    age,
    height,
    weight,
    gender,
    goal
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📏 BMI", bmi)

with col2:
    st.metric("🏷 BMI Category", category)

with col3:
    st.metric("🔥 Daily Calories", f"{daily_calories} kcal")

st.divider()


if st.button("Generate Diet Plan"):

    prompt = f"""
You are an expert dietician and nutritionist.

Generate a personalized Indian diet plan.

User Details:

Age: {age}

Gender: {gender}

Height: {height} cm

Weight: {weight} kg

BMI: {bmi}

BMI Category: {category}

Fitness Goal: {goal}

Food Preference: {food}

Recommended Daily Calories:
{daily_calories} kcal

Create the response in Markdown format.

Include the following:

## Daily Calories

## Breakfast

## Mid-Morning Snack

## Lunch

## Evening Snack

## Dinner

## Water Intake

## Protein Intake

## Grocery List

## Foods to Avoid

## Health Tips

Make the diet practical, affordable and suitable for an Indian lifestyle.
"""

    with st.spinner("Generating your personalized diet plan..."):
        response = llm.invoke(prompt)

        st.markdown(response.content)

    st.success("Diet Plan Generated Successfully!")

    st.markdown(response.content)