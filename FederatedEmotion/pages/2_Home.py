import streamlit as st
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="KeyMood AI - Home", page_icon="🏠", layout="wide")

# ---------- SESSION & LOGIN CHECK ----------
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.warning("⚠️ Please login first from the Login Page in the sidebar.")
    st.stop()

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
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(18px);
    text-align: center;
    color: white;
    margin-top: 40px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.25);
    transition: all 0.4s ease;
}
.hero:hover { transform: scale(1.02); }
.hero-title { font-size:70px; font-weight:900; animation: fadeInDown 1.2s ease forwards; }
.hero-subtitle { font-size:22px; opacity:0.95; margin-top:10px; animation: fadeInUp 1.5s ease forwards; }

/* CARDS */
.card {
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 20px;
    margin-top: 20px;
    color: white;
    transition: transform 0.3s ease, background 0.3s ease;
}
.card:hover { transform: scale(1.03); background: rgba(255,255,255,0.35); }
.small-title { font-size: 24px; font-weight: 800; }

/* FOOTER */
.footer { text-align:center; color:white; opacity:0.8; margin-top:50px; font-size:14px; }

/* BUTTON CONTAINER (REMOVED NAVIGATION BUTTONS) */
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
    padding: 12px 25px;
    font-size: 18px;
    font-weight: bold;
    background: rgba(255,255,255,0.25);
    color: white;
    border-radius: 12px;
    text-decoration: none;
    border: 1px solid rgba(255,255,255,0.25);
    transition: 0.3s;
}
.btn-container a:hover { background: rgba(255,255,255,0.40); transform: scale(1.05); }

/* ANIMATION KEYFRAMES */
@keyframes fadeInDown { 0% {opacity:0; transform: translateY(-40px);} 100% {opacity:1; transform: translateY(0);} }
@keyframes fadeInUp { 0% {opacity:0; transform: translateY(40px);} 100% {opacity:1; transform: translateY(0);} }
</style>
""", unsafe_allow_html=True)

# ---------- WELCOME MESSAGE ----------
st.info(f"👋 Welcome {st.session_state.user_id} to KeyMood AI!", icon="🧠")

# ---------- HERO SECTION ----------
st.markdown("""
<div class="hero">
    <div class="hero-title">🧠 KeyMood AI</div>
    <div class="hero-subtitle">
        Federated Emotion Detection using Keystroke Dynamics <br>
        Privacy-Preserving • Real-Time • AI Powered
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- MAIN FEATURE CARDS ----------
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='card'>
        <div class='small-title'>🚀 Get Started</div><br>
        Navigate to the Emotion Detection page from the sidebar to predict moods..
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='card'>
        <div class='small-title'>🧠 Emotion Detection</div><br>
        Emotion detection is the process of identifying a person's emotional state from their behavior, expressions, or physiological signals. 
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='card'>
        <div class='small-title'>📊 Dashboard</div><br>
        Navigate to the Dashboard page from the sidebar to view history and reports.
    </div>
    """, unsafe_allow_html=True)

# ---------- EXTRA INFO CARDS ----------
st.markdown("---")
colA, colB = st.columns(2)

with colA:
    st.markdown("""
    <div class='card'>
        <div class='small-title'>🔐 Privacy First</div><br>
        User data never leaves the device. Only model updates are shared with the global model.
    </div>
    """, unsafe_allow_html=True)

with colB:
    st.markdown("""
    <div class='card'>
        <div class='small-title'>🌍 Federated Learning</div><br>
        Federated Learning is a privacy-preserving approach where multiple devices collaboratively train a shared model without sending their raw data to a central server.
    </div>
    """, unsafe_allow_html=True)

# ---------- TEAM SECTION ----------
st.markdown("---")
st.markdown("""
<div class='card'>
    <div class='small-title'>👥 Team Members</div><br>
    1. Team Leader – Jinit Gandhi<br>
    2. Member 2 – Krish Patel<br>
    3. Member 3 – Saman Sunasara<br>
    4. Member 4 – bhavesh Atmakuri<br>
</div>
""", unsafe_allow_html=True)

# ---------- FUTURE ENHANCEMENTS ----------
st.markdown("---")
st.markdown("""
<div class='card'>
    <div class='small-title'>🚀 Future Enhancements</div><br>
    🔹 Real-time keystroke capture using advanced event tracking <br>
    🔹 Deep Learning-based emotion prediction models <br>
    🔹 Support for mobile keyboards and multilingual typing <br>
    🔹 Improved federated aggregation and security methods <br>
</div>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("<div class='footer'>© 2026 KeyMood AI | Minor Project</div>", unsafe_allow_html=True)