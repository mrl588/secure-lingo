import os
import streamlit as st
import streamlit.components.v1 as components
from pymongo import MongoClient
from datetime import datetime
import time
from streamlit_extras.switch_page_button import switch_page

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'show_login' not in st.session_state:
    st.session_state.show_login = False
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

# Connect to MongoDB
client = MongoClient("mongodb+srv://dzheng4m:cGqGXWHSHFQRxSRZ@cluster0.06nr7.mongodb.net/")
database = client['SecurityFilterDb']
users_collection = database["users"]

# Configure the page
st.set_page_config(
    page_title="safeBrowsing",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
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
    
    /* Feature cards styling */
    .features {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        padding: 40px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .feature-card {
        background-color: #2c2c2c;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
    }
    
    .feature-icon {
        font-size: 40px;
        color: #00ff00;
    }
    
    .feature-card h3 {
        color: #00ff00;
        margin: 20px 0;
    }
    
    .feature-card p {
        color: #cccccc;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def handle_login(login_email, login_password):
    if not login_email.endswith("@gmail.com") or len(login_email) <= 6:
        st.sidebar.warning("Please enter a valid @gmail.com email address longer than 6 characters.")
        return False
    
    login_email = login_email.lower()
    user = users_collection.find_one({"email": login_email})
    
    if not user:
        st.sidebar.error("User not found. Please sign up.")
        return False
    elif user["password"] != login_password:
        st.sidebar.error("Incorrect password.")
        return False
    else:
        st.session_state.authenticated = True
        st.session_state.user_email = login_email
        st.session_state.show_login = False
        st.sidebar.success("Logged In! Redirecting...")

        time.sleep(1)  # Show success message briefly
        switch_page("dashboard")  # Redirect to Dashboard Page
        return True


def handle_signup(signup_email, signup_password, confirm_password):
    if not signup_email.endswith("@gmail.com") or len(signup_email) <= 6:
        st.sidebar.warning("Please enter a valid @gmail.com email address longer than 6 characters.")
        return False
    elif signup_password != confirm_password:
        st.sidebar.warning("Passwords do not match")
        return False
    
    signup_email = signup_email.lower()
    existing_user = users_collection.find_one({"email": signup_email})
    if existing_user:
        st.sidebar.warning("An account with this email already exists. Please log in.")
        return False
    
    users_collection.insert_one({"email": signup_email, "password": signup_password})
    st.sidebar.success("Account Created!")
    st.session_state.show_signup = False
    return True

# Navbar function
def navbar():
    st.sidebar.markdown("<h1 style='font-size: 40px; color: #00ff00;'>SecureLingo</h1>", unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        if st.sidebar.button("Log In", key="nav_login"):
            st.session_state.show_login = True
            st.session_state.show_signup = False
        if st.sidebar.button("Sign Up", key="nav_signup"):
            st.session_state.show_signup = True
            st.session_state.show_login = False

# Call navbar
navbar()

# LOGIN FORM
if st.session_state.show_login and not st.session_state.authenticated:
    with st.sidebar.form(key="login_form"):
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        submit_login = st.form_submit_button("Submit")
        
        if submit_login:
            if handle_login(login_email, login_password):
                st.rerun()

# SIGN-UP FORM
if st.session_state.show_signup and not st.session_state.authenticated:
    with st.sidebar.form(key="signup_form"):
        st.subheader("Create Account")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        submit_signup = st.form_submit_button("Submit")
        
        if submit_signup:
            if handle_signup(signup_email, signup_password, confirm_password):
                st.rerun()

# MAIN CONTENT
# HERO SECTION
hero_html = """
<div class="hero">
    <h1>Learn Cybersecurity The Fun Way</h1>
    <p>Master essential cybersecurity skills through interactive lessons, real-world scenarios, and daily practice. 
    Join millions of learners protecting themselves and their organizations online.</p>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# FEATURES SECTION
features_html = """
<div class="features">
    <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <h3>Interactive Lessons</h3>
        <p>Learn through hands-on exercises and real-world scenarios</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3>Daily Practice</h3>
        <p>Build your security skills with bite-sized daily lessons</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3>Track Progress</h3>
        <p>Monitor your learning journey with detailed analytics</p>
    </div>
</div>
"""
st.markdown(features_html, unsafe_allow_html=True)

# Check authentication status and display appropriate content
if st.session_state.authenticated:
    st.write(f"Welcome, {st.session_state.user_email}!")
    # Add your dashboard or protected content here
else:
    st.write("Please log in to access the content.")