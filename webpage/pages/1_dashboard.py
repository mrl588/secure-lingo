import streamlit as st
from datetime import datetime
from google import genai

import sys
import os, json


from pymongo import MongoClient

from typing import List
from pydantic import BaseModel


client = MongoClient(os.getenv("MONGO_URL"))
db = client.get_database('SecurityFilterDb')
lessons_collection = db.get_collection('Lesson')

class Quiz(BaseModel):
    question: str
    answers: list[str]
    correct_answer: str


class Result(BaseModel):
    quizes: list[Quiz]
    examples: list[str]
    checklists: List[str]
    summary: str
    title: str


def get_prompt(last_lesson):
    return f"""
    Give me a lesson focused on ONE topic on online security based on the following criteria:
        - Keep in mind the following past lessons, but do not repeat, overlap, or closely mirror any of the 
        information from them: {last_lesson}
        - Curate the lesson for people who aren't familiar with technology.
        - Focus on possible online scams, password management, social engineering, secure browsing, phishing, etc.
        - Make the response a concise but detailed paragraph, with examples separate from the paragraphs.
        - The said examples can include case studies, statistics, historical hacks, etc. 
        - Make the tone educational and conversational.
        - Provide a checklist with key takeaways
        - Don't ask a question at the end

    After you generate the lesson, generate a multiple choice quiz based on the following criteria:
        - Produce a total of 4 questions strictly based on the information given in the lesson.
        - Each question will have 4 answers, with the answers having assigned letters a, b, c, and d in order. These letters are placed one space over to the left of the answer.
        - Be sure to store the correct answer in correct_answer.
        
    """

def fetch_past_lessons():
    Lesson = []
    for lesson in lessons_collection.find():
        Lesson.append(lesson.get('content', ''))
    return Lesson


def generate_lessons():

    past_lessons = fetch_past_lessons()

    formatted_lessons = "\n".join([lesson for lesson in past_lessons])

    prompt = get_prompt(formatted_lessons)

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': Result,
        },
    )

    lesson = json.loads(response.text)
    # lesson_document = {
    #     "lesson": json.dumps(lesson)
    # }

    # lessons_collection.insert_one(lesson_document)

    return lesson

# Add the backend directory to Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend_2.0'))
sys.path.append(backend_path)

# Set page config (must be the first Streamlit command)
st.set_page_config(
    page_title="Cybersecurity Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Check authentication before displaying dashboard content
if not st.session_state.authenticated:
    st.warning("You need to log in first.")
else:
    # Your dashboard content here
    st.markdown("# Welcome to your Dashboard!")
    
    # Custom CSS for Logout Button placement
    st.markdown("""
        <style>
        .logout-btn {
            background-color: #ff4d4d;
            border: none;
            color: white;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 20px;
        }

        .main {
            background-color: #1a1a1a;
        }

        /* Navigation bar styling */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background-color: #2c2c2c;
            margin: -6rem -4rem 2rem -4rem;
        }

        .logo {
            color: #00ff00;
            font-size: 24px;
            font-weight: bold;
        }

        .nav-buttons {
            display: flex;
            gap: 20px;
        }

        .login-btn {
            background-color: transparent;
            border: 2px solid #00ff00;
            color: #00ff00;
            padding: 10px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
        }

        .signup-btn {
            background-color: #00ff00;
            border: none;
            color: #1a1a1a;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
        }

        /* Hero section styling */
        .hero {
            text-align: center;
            padding: 80px 20px;
            max-width: 1200px;
            margin: 0 auto;
            color: white;
        }

        .hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
            color: #00ff00;
        }

        .hero p {
            font-size: 20px;
            color: #cccccc;
            margin-bottom: 40px;
            line-height: 1.6;
        }

        /* Section Styling */
        .section {
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
            color: white;
            background-color: #2c2c2c;
            border-radius: 10px;
            margin-bottom: 30px;
        }

        .section h2 {
            color: #00ff00;
            font-size: 30px;
        }

        .lesson-content, .quiz-content {
            color: #cccccc;
            font-size: 18px;
            margin-bottom: 20px;
        }

        .question {
            color: #ffffff;
        }

        .quiz-option {
            color: #cccccc;
            margin-bottom: 10px;
        }

        /* Additional styles for interactive elements */
        .stButton button {
            background-color: #00ff00;
            color: #1a1a1a;
            font-weight: bold;
            border-radius: 25px;
            padding: 12px 25px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .stButton button:hover {
            background-color: #00cc00;
        }

        .stRadio > label {
            color: #cccccc !important;
        }

        .success-message {
            color: #00ff00;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }

        .error-message {
            color: #ff4d4d;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)

    # Display logout button under the dashboard content
    if st.button("Logout", key="logout_btn", help="Click here to log out", on_click=lambda: st.session_state.update({"authenticated": False, "user_email": None})):
        st.success("You have been logged out.")

    # Initialize session state for lessons if not exists
    if 'current_lesson' not in st.session_state:
        st.session_state.current_lesson = None

    # HERO SECTION
    hero_html = """
    <div class="hero">
        <h1>Welcome to the Cybersecurity Dashboard</h1>
        <p>Stay up to date with daily lessons and quizzes to strengthen your cybersecurity skills.</p>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

    # Generate new lesson button
    if st.button("Generate New Lesson"):
        with st.spinner("Generating new lesson..."):
            try:
                st.session_state.current_lesson = generate_lessons()
            except Exception as e:
                st.error(f"Error generating lesson: {str(e)}")

    # DAILY LESSON SECTION
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    if st.session_state.current_lesson:
        lesson_data = st.session_state.current_lesson
        
        # Display lesson title
        st.header(lesson_data["title"])
        
        # Display lesson summary
        st.markdown("### Summary")
        st.write(lesson_data["summary"])
        
        # Display examples
        if lesson_data["examples"]:
            st.markdown("### Examples")
            for example in lesson_data["examples"]:
                st.markdown(f"- {example}")
        
        # Display checklists
        if lesson_data["checklists"]:
            st.markdown("### Key Points")
            for item in lesson_data["checklists"]:
                st.markdown(f"- {item}")
    else:
        st.info("Click 'Generate New Lesson' to get today's cybersecurity lesson!")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # QUIZ SECTION
    if st.session_state.current_lesson and st.session_state.current_lesson["quizes"]:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        st.subheader("❓ Quiz: Test Your Knowledge")

        # Initialize session state for quiz responses
        if 'quiz_responses' not in st.session_state:
            st.session_state.quiz_responses = {}
        
        if 'quiz_submitted' not in st.session_state:
            st.session_state.quiz_submitted = False

        quizzes = st.session_state.current_lesson["quizes"]
        
        # Display quiz questions
        for i, quiz in enumerate(quizzes):
            st.markdown(f"### Question {i + 1}: {quiz["question"]}")
            key = f"quiz_{i}"
            st.session_state.quiz_responses[key] = st.radio(
                "Select your answer:",
                options=quiz["answers"],
                key=key
            )

        # Submit button for quiz
        if st.button("Submit Quiz"):
            st.session_state.quiz_submitted = True
            correct_answers = 0
            total_questions = len(quizzes)

            for i, quiz in enumerate(quizzes):
                user_answer = st.session_state.quiz_responses[f"quiz_{i}"]
                if user_answer == quiz["correct_answer"]:
                    correct_answers += 1
                    st.success(f"Question {i + 1}: Correct!")
                else:
                    st.error(f"Question {i + 1}: Incorrect. The correct answer was: {quiz["correct_answer"]}")

            score_percentage = (correct_answers / total_questions) * 100
            st.markdown(f"### Your Score: {score_percentage:.1f}%")
            st.markdown(f"You got {correct_answers} out of {total_questions} questions correct!")

        st.markdown('</div>', unsafe_allow_html=True)

    # Footer section
    st.markdown("""
        <footer style="color: #cccccc; text-align: center; padding: 20px;">
            <p>Made with ❤️ by SecureLingo | &copy; 2025</p>
        </footer>
    """, unsafe_allow_html=True)


