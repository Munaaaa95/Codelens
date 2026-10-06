import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# -----------------------------
# SETUP
# -----------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "GEMINI_API_KEY was not found. "
        "Add it to your .env file or Streamlit Secrets."
    )
    st.stop()

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"


# -----------------------------
# PAGE
# -----------------------------

st.set_page_config(
    page_title="CodeLens",
    page_icon="🔎",
    layout="wide"
)


# -----------------------------
# STYLING
# -----------------------------

st.markdown(
    """
    <style>
    .title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    '<div class="title">🔎 CodeLens</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Understand. Debug. Improve. Learn.</div>',
    unsafe_allow_html=True
)


# -----------------------------
# FEATURE CARDS
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
        <b>🧠 Explain</b><br>
        Understand what your code does.
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="card">
        <b>🐛 Debug</b><br>
        Find bugs and potential problems.
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="card">
        <b>⚡ Improve</b><br>
        Make your code cleaner and better.
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# -----------------------------
# CODE INPUT
# -----------------------------

st.subheader("💻 Your Python Code")

code = st.text_area(
    "Paste your Python code below",
    height=300,
    placeholder="""def calculate_average(numbers):
    return sum(numbers) / len(numbers)

print(calculate_average([10, 20, 30]))""",
    label_visibility="collapsed"
)


# -----------------------------
# OPTIONS
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    analysis_level = st.selectbox(
        "Analysis Level",
        [
            "Beginner-friendly",
            "Intermediate",
            "Advanced"
        ]
    )

with col2:
    focus = st.selectbox(
        "Focus",
        [
            "Full Analysis",
            "Bugs & Errors",
            "Code Quality",
            "Learning"
        ]
    )


# -----------------------------
# ANALYZE
# -----------------------------

if st.button(
    "🔍 Analyze Code",
    type="primary",
    use_container_width=True
):

    if not code.strip():

        st.warning("Please paste some Python code first.")

    else:

        prompt_parts = [
            "You are an expert Python developer, code reviewer, "
            "debugger, and programming tutor.",
            "",
            "Analyze the following Python code:",
            "",
            code,
            "",
            f"Analysis level: {analysis_level}",
            f"Primary focus: {focus}",
            "",
            "Provide your response using these sections:",
            "",
            "## What This Code Does",
            "Explain what the code does and how it works.",
            "",
            "## Code Breakdown",
            "Explain the important parts of the code.",
            "",
            "## Potential Problems",
            "Identify bugs, runtime errors, logical problems, "
            "edge cases, and poor practices.",
            "",
            "## Improvements",
            "Suggest practical improvements to readability, "
            "performance, maintainability, and correctness.",
            "",
            "## Improved Version",
            "Provide a cleaner or safer version of the code.",
            "",
            "## Learning Notes",
            "Explain the important Python concepts demonstrated.",
            "",
            "Be accurate and educational. Do not invent problems."
        ]

        prompt = "\n".join(prompt_parts)

        with st.spinner("CodeLens is analyzing your code..."):

            try:

                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt
                )

                if response and response.text:

                    st.divider()

                    st.subheader("🔎 Code Analysis")

                    st.markdown(response.text)

                else:

                    st.error(
                        "No analysis was returned. Please try again."
                    )

            except Exception as e:

                if "503" in str(e):

                    st.error(
                        "Gemini is temporarily experiencing high demand. "
                        "Please try again in a moment."
                    )

                else:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "CodeLens • AI-powered Python learning and code analysis"
)