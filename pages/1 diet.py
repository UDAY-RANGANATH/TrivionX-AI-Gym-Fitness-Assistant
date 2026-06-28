import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from utils.llm import llm

load_dotenv()

from utils.llm import llm

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

allergies = st.text_input(
    "Do you have any food allergies?",
    placeholder="Example: Peanuts, Milk, Soy, Gluten, None"
)

nonveg_frequency = st.selectbox(
    "How many days do you eat Non-Vegetarian food in a week?",
    [
        "0 Days",
        "1-2 Days",
        "3-4 Days",
        "5-7 Days"
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
    st.metric("BMI", bmi)

with col2:
    st.metric("BMI Category", category)

with col3:
    st.metric("Daily Calories", f"{daily_calories} kcal")

st.divider()


if st.button("Generate Diet Plan"):
    
    prompt = f"""
    You are NOT allowed to create your own diet.
    
    You must ONLY recommend foods that are present
    inside the Diet PDF knowledge and remove the items the user is allergic
    
    Non Veg Frequency : {nonveg_frequency}
    
    Food Allergies : {allergies}
    
    Daily Calories
    
    {daily_calories}
        Keep it as short as possible so the user can understand easily with more options

    If the requested diet cannot be found,
    reply exactly:
    
    Diet not found in the knowledge base.
    
    refer the chatbot to modify the plan
    Do not invent meals.
    
    Do not hallucinate.
    
    
    Return the meals available in the PDF.
    """

    with st.spinner("Generating your personalized diet plan..."):
        response = llm.invoke(prompt)

        st.markdown(response.content)

    st.success("Diet Plan Generated Successfully!")

    st.info("If you want to make any custom modifications with the diet plan you can reachout our chabot and paste your given plan and modify it")