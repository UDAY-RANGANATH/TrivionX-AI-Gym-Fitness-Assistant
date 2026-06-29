import os
import re
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS   # ✅ this is the correct import          # ✅ standalone, not community
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage  # ✅

# ── Env ───────────────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found in .env file.")
    st.stop()

# ── Constants ─────────────────────────────────────────────────────────────────
PDF_PATH   = "assets/DIET.pdf"
INDEX_PATH = "diet_index"

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.3-70b-versatile",
    temperature=0.2,
)

# ── Embeddings — cached so weights load only ONCE ────────────────────────────
@st.cache_resource(show_spinner="Loading embeddings model...")
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

embeddings = get_embeddings()

# ── PDF helpers ───────────────────────────────────────────────────────────────
def get_pdf_text(pdf_path: str) -> str:
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def get_text_chunks(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    return splitter.split_text(text)


# ── Vector store — built once, cached ────────────────────────────────────────
@st.cache_resource(show_spinner="Building knowledge base...")
def load_vector_store():
    if not os.path.exists(INDEX_PATH):
        text   = get_pdf_text(PDF_PATH)
        chunks = get_text_chunks(text)
        db     = FAISS.from_texts(chunks, embedding=embeddings)
        db.save_local(INDEX_PATH)
    return FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )

db = load_vector_store()

# ── Search ────────────────────────────────────────────────────────────────────
def search_pdf(goal: str, food: str) -> str:
    query = f"{goal} {food} Indian meals Breakfast Lunch Dinner Snacks"
    docs  = db.similarity_search(query, k=3)
    context = ""
    for doc in docs:
        text = re.sub(r"\n\s*\n", "\n", doc.page_content)
        context += text + "\n\n"
    return context

# ── Groq summariser ───────────────────────────────────────────────────────────
def generate_diet_plan(
    context: str,
    goal: str,
    food: str,
    allergies: str,
    nonveg_frequency: str,
    daily_calories: int,
) -> str:
    system = (
        "You are a concise Indian diet assistant. "
        "Using ONLY the meals from the context provided, "
        "produce a short, clean plan in this exact format:\n\n"
        "**Breakfast**\n"
        "• Option 1: [meal name] (~kcal)\n"
        "• Option 2: [meal name] (~kcal)\n"
        "• Option 3: [meal name] (~kcal)\n\n"
        "**Lunch**\n• Option 1: ...\n\n"
        "**Dinner**\n• Option 1: ...\n\n"
        "**Snacks**\n• Option 1: ...\n\n"
        "**Quick Tips**\n• [1-2 short tips]\n\n"
        "Rules: max 3 options per meal • meal name only, no ingredients "
        "• each bullet under 10 words • skip allergens • stay within calorie target "
        "• never repeat dishes • never invent food not in the context."
    )
    user = (
        f"Goal: {goal}\n"
        f"Food preference: {food}\n"
        f"Allergies: {allergies or 'None'}\n"
        f"Non-veg days/week: {nonveg_frequency}\n"
        f"Daily calorie target: {daily_calories} kcal\n\n"
        f"Context:\n{context}"
    )
    response = llm.invoke([
        SystemMessage(content=system),
        HumanMessage(content=user),
    ])
    return response.content

# ── BMI & Calories ────────────────────────────────────────────────────────────
def calculate_bmi(weight: float, height: float) -> float:
    h = height / 100
    return round(weight / (h ** 2), 1)

def bmi_category(bmi: float) -> str:
    if bmi < 18.5: return "Underweight"
    elif bmi < 25: return "Normal Weight"
    elif bmi < 30: return "Overweight"
    else:          return "Obese"

def calculate_calories(age, height, weight, gender, goal) -> int:
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    calories = bmr * 1.55
    if goal == "Weight Loss":   calories -= 500
    elif goal == "Muscle Gain": calories += 300
    return round(calories)

# ══════════════════════════════════════════════════════
# STREAMLIT UI
# ══════════════════════════════════════════════════════

st.set_page_config(
    page_title="AI Dietician",
    page_icon="🥗",
    layout="wide",
)

st.title("🥗 TrivionX AI Dietician")
st.write(
    "Fill in your details to generate a personalised diet plan "
    "using the TrivionX Diet Knowledge Base."
)
st.divider()

# ── Input form ────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    age    = st.number_input("Age",         min_value=10,  max_value=100, value=20)
    gender = st.radio("Gender",             ["Male", "Female"])
    height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
    weight = st.number_input("Weight (kg)", min_value=20,  max_value=250, value=70)

with col2:
    goal = st.selectbox(
        "Fitness Goal",
        ["Weight Loss", "Muscle Gain", "Maintain Weight"],
    )
    food = st.radio("Food Preference", ["Vegetarian", "Non-Vegetarian"])
    allergies = st.text_input(
        "Food Allergies",
        placeholder="e.g. Milk, Peanuts, Soy — or None",
    )
    nonveg_frequency = st.selectbox(
        "Non-Vegetarian Meals Per Week",
        ["0 Days", "1-2 Days", "3-4 Days", "5-7 Days"],
    )

# ── Live metrics ──────────────────────────────────────
bmi            = calculate_bmi(weight, height)
category       = bmi_category(bmi)
daily_calories = calculate_calories(age, height, weight, gender, goal)

m1, m2, m3 = st.columns(3)
with m1: st.metric("BMI",            bmi)
with m2: st.metric("BMI Category",   category)
with m3: st.metric("Daily Calories", f"{daily_calories} kcal")

st.divider()

# ── Generate ──────────────────────────────────────────
if st.button("🍽 Generate Diet Plan", use_container_width=True):

    with st.spinner("Searching knowledge base..."):
        context = search_pdf(goal, food)

    with st.spinner("Generating your plan..."):
        try:
            plan = generate_diet_plan(
                context=context,
                goal=goal,
                food=food,
                allergies=allergies,
                nonveg_frequency=nonveg_frequency,
                daily_calories=daily_calories,
            )
            st.success("✅ Diet Plan Ready!")
            st.markdown(plan)
            st.info("💬 Want changes? Copy the plan and ask the AI Chatbot to modify it.")

        except Exception as e:
            st.error(f"Could not generate plan: {e}")
            if context.strip():
                st.markdown(context[:600] + "…")
            else:
                st.warning("No relevant diet options found. Check that assets/DIET.pdf exists.")