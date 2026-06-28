import streamlit as st
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

def get_pdf_text(pdf_path):

    text = ""

    pdf_reader = PdfReader(pdf_path)

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


def get_text_chunks(text):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=10000,

        chunk_overlap=1000

    )

    return splitter.split_text(text)


def create_vector_store():

    pdf_path = "assets/DIET.pdf"

    text = get_pdf_text(pdf_path)

    chunks = get_text_chunks(text)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_texts(
        chunks,
        embedding=embeddings
    )

    db.save_local("diet_index")

if not os.path.exists("diet_index"):
    create_vector_store()


def search_pdf(question):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        "diet_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(question, k=5)

    answer = ""

    for doc in docs:
        answer += doc.page_content
        answer += "\n\n"

    return answer

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

    query = f"""
Age: {age}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg

Goal: {goal}

Food Preference: {food}

Food Allergies: {allergies}

Non-Vegetarian Frequency: {nonveg_frequency}

Daily Calories: {daily_calories}

Give ONLY 5 items as options of the diet available givr the name of food items only not ingredients in the PDF.

keep it as short and simple as possible so that the user can understand easily

Include:
- Breakfast
- Lunch
- Dinner
- Snacks

Remove foods containing the allergies.

If no suitable diet is found, reply:

Diet not found in the knowledge base.
"""

    with st.spinner("Searching Diet Guide..."):

        answer = search_pdf(query)

        if answer.strip():
            st.markdown(answer)
        else:
            st.warning(
                "Diet not found in the knowledge base.\n\nPlease use the AI Chatbot for further assistance."
            )

    st.success("Diet Plan Generated Successfully!")

    st.info(
        "Need more changes? Copy this plan and ask the AI Chatbot to modify it."
    )