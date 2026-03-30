import streamlit as st
import time
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="KeyMood AI", page_icon="🧠", layout="wide")

# ---------- SESSION STATE ----------
if "welcome_done" not in st.session_state:
    st.session_state.welcome_done = False
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

/* HERO SECTION */
.hero {
    padding: 60px;
    border-radius: 25px;
    background: rgba(255,255,255,0.20);
    backdrop-filter: blur(18px);
    text-align: center;
    color: white;
    margin-top: 50px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.2);
    transition: all 0.5s ease;
}
.hero-title {
    font-size: 75px;
    font-weight: 900;
    animation: fadeInDown 1.5s ease forwards;
}
.hero-subtitle {
    font-size: 22px;
    opacity: 0.95;
    margin-top: 10px;
    animation: fadeInUp 2s ease forwards;
}
@keyframes fadeInDown {
    0% {opacity:0; transform: translateY(-50px);}
    100% {opacity:1; transform: translateY(0);}
}
@keyframes fadeInUp {
    0% {opacity:0; transform: translateY(50px);}
    100% {opacity:1; transform: translateY(0);}
}

/* LOGIN CARD CENTERED */
.login-center {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
    transition: all 0.5s ease;
}
.login-card {
    background: rgba(255,255,255,0.25);
    padding: 25px 40px;
    border-radius: 18px;
    backdrop-filter: blur(15px);
    box-shadow: 0px 5px 20px rgba(0,0,0,0.3);
    text-align:center;
    transition: transform 0.3s ease, background 0.3s ease;
}
.login-card:hover {
    transform: scale(1.03);
    background: rgba(255,255,255,0.35);
}

/* BUTTONS AT BOTTOM */
.btn-container {
    position: fixed;
    bottom: 20px;
    width: 100%;
    text-align: center;
    z-index: 9999;
    display: flex;
    justify-content: center;
    gap: 30px;
}
.btn-container a {
    padding: 12px 28px;
    font-size: 18px;
    font-weight: bold;
    background: rgba(255,255,255,0.25);
    color: white;
    border-radius: 12px;
    text-decoration: none;
    border: 1px solid rgba(255,255,255,0.25);
    transition: 0.3s;
}
.btn-container a:hover {
    background: rgba(255,255,255,0.40);
    transform: scale(1.05);
}

/* FOOTER */
.footer {
    text-align:center;
    color:white;
    opacity:0.8;
    margin-top:60px;
    font-size:14px;
}

/* ALERTS & SPINNER */
.stAlert, .stInfo, .stSuccess, .stSpinner {
    border-radius: 15px;
    padding: 18px;
    font-weight: 600;
}

/* PROGRESS BAR */
.progress-container {
    width: 50%;
    margin: 20px auto;
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

# ---------- HERO SECTION ----------
st.markdown("""
<div class="hero">
    <div class="hero-title">🧠 KeyMood AI</div>
    <div class="hero-subtitle">
        Federated Emotion Detection using Keystroke Dynamics <br>
        Secure • Real-Time • Privacy Preserving
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- INITIAL LOADING & TIMER ----------
if st.session_state.welcome_done == False:
    st.info("🔄 Initializing KeyMood AI Modules...")

    # Animated Progress Bar
    st.markdown('<div class="progress-container"><div class="progress-bar" id="progress">0%</div></div>', unsafe_allow_html=True)
    progress_bar = st.empty()
    
    st.success("✅ KeyMood AI Ready!")
    st.session_state.welcome_done = True
    st.rerun()  # Refresh to show login dynamically

# ---------- LOGIN BUTTON CENTER ----------
if not st.session_state.logged_in:
    st.markdown("<div class='login-center'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="login-card">
        <h3>Welcome to KeyMood AI</h3>
        <p>Click below to login and start exploring!</p>
    """, unsafe_allow_html=True)

    if st.button("🔐 Login to Continue", key="main_login"):

        st.markdown("<h4 style='text-align:center;'>🔄 Redirecting to Login Page...</h4>", unsafe_allow_html=True)
        st.switch_page("pages/1_Login.py")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
# ---------- PAGE BUTTONS AT BOTTOM ----------


# ---------- FOOTER ----------
st.markdown("<div class='footer'>© 2026 KeyMood AI | Minor Project</div>", unsafe_allow_html=True)

# ---------- DISPLAY USER INFO ----------
if st.session_state.logged_in:
    st.markdown(f"<div style='text-align:center; margin-top:15px; color:white; font-weight:bold;'>👤 Logged in as: {st.session_state.user_id}</div>", unsafe_allow_html=True)