import streamlit as st
import time
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="KeyMood AI - Login", page_icon="🔐", layout="centered")

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# ---------- CSS STYLING ----------
st.markdown("""
<style>
/* BACKGROUND GRADIENT ANIMATION */
.stApp {
    background: linear-gradient(120deg, #ffdde1, #ee9ca7, #a1c4fd, #c2e9fb, #fbc2eb, #a6c1ee);
    background-size: 600% 600%;
    animation: gradientBG 15s ease infinite;
    transition: all 0.6s ease-in-out;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    25% {background-position: 50% 50%;}
    50% {background-position: 100% 50%;}
    75% {background-position: 50% 50%;}
    100% {background-position: 0% 50%;}
}

/* LOGIN CARD */
.login-center {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
}
.login-box {
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(18px);
    padding: 40px 50px;
    border-radius: 20px;
    text-align: center;
    color: white;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.25);
    transition: transform 0.3s ease, background 0.3s ease;
}
.login-box:hover {
    transform: scale(1.03);
    background: rgba(255,255,255,0.35);
}

/* TITLES */
.title {
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 10px;
    animation: fadeInDown 1.2s ease forwards;
}
.subtitle {
    font-size: 18px;
    opacity: 0.9;
    margin-bottom: 25px;
    animation: fadeInUp 1.5s ease forwards;
}

/* FORM INPUTS */
.stTextInput>div>div>input {
    border-radius: 12px;
    padding: 10px;
    font-size: 16px;
    background: rgba(255,255,255,0.15);
    color: white;
    border: 1px solid rgba(255,255,255,0.25);
}
.stTextInput>div>label {
    font-weight: 600;
    color: white;
}
.stButton>button {
    border-radius: 12px;
    padding: 12px 25px;
    font-size: 18px;
    font-weight: 700;
    background: rgba(255,255,255,0.25);
    color: white;
    border: 1px solid rgba(255,255,255,0.25);
    transition: 0.3s;
}
.stButton>button:hover {
    background: rgba(255,255,255,0.40);
    transform: scale(1.05);
}

/* ALERTS */
.stAlert, .stInfo, .stSuccess, .stSpinner {
    border-radius: 15px;
    padding: 18px;
    font-weight: 600;
}

/* FOOTER */
.footer {
    text-align:center;
    color:white;
    opacity:0.8;
    margin-top:50px;
    font-size:14px;
}

/* ANIMATION KEYFRAMES */
@keyframes fadeInDown {
    0% {opacity:0; transform: translateY(-40px);}
    100% {opacity:1; transform: translateY(0);}
}
@keyframes fadeInUp {
    0% {opacity:0; transform: translateY(40px);}
    100% {opacity:1; transform: translateY(0);}
}

/* PROGRESS BAR */
.progress-container {
    width: 60%;
    margin: 15px auto 25px auto;
    background: rgba(255,255,255,0.20);
    border-radius: 20px;
    overflow: hidden;
}
.progress-bar {
    height: 18px;
    width: 0%;
    background: rgba(255,255,255,0.45);
    text-align:center;
    color:white;
    font-weight:bold;
    line-height:18px;
    border-radius:20px;
    transition: width 1s ease;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGIN CARD ----------
st.markdown('<div class="login-center">', unsafe_allow_html=True)
st.markdown("""
<div class="login-box">
    <div class="title">🔐 KeyMood AI</div>
    <div class="subtitle">Login to access Emotion Detection & Dashboard</div>
""", unsafe_allow_html=True)

user_id = st.text_input("👤 User ID")
password = st.text_input("🔑 Password", type="password")

# ---------- DEMO USER DATABASE ----------
USER_DB = {
    "admin": "admin123",
    "user1": "1234",
    "user2": "1234",
    "user3": "1234"
}

# ---------- LOGIN BUTTON WITH ANIMATION ----------
if st.button("🚀 Login"):
    if user_id in USER_DB and USER_DB[user_id] == password:
        st.session_state.logged_in = True
        st.session_state.user_id = user_id

        # Show progress bar animation
        

        st.success("✅ Login Successful!")
        time.sleep(1)
        # Redirect to Home page after login
        st.switch_page("pages/2_Home.py")
     
    else:
        st.error("❌ Invalid User ID or Password")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------- PAGE NAVIGATION BUTTONS ----------


# ---------- FOOTER ----------
st.markdown("<div class='footer'>© 2026 KeyMood AI | Minor Project | Demo Users: admin/admin123, user1/1234</div>", unsafe_allow_html=True)