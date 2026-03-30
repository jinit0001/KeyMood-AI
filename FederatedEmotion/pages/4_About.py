import streamlit as st

st.set_page_config(page_title="KeyMood AI - About", page_icon="📘", layout="wide")
st.markdown("""
<style>

/* Hide Streamlit default header/footer/menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.20);
    backdrop-filter: blur(15px);
    border-right: 2px solid rgba(255,255,255,0.25);
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: 600;
}

/* Sidebar title */
.sidebar-title {
    text-align: center;
    font-size: 28px;
    font-weight: 900;
    margin-top: 15px;
    margin-bottom: 15px;
    color: white;
}

/* Sidebar buttons look */
div.stButton > button {
    width: 100%;
    border-radius: 12px;
    padding: 10px;
    font-size: 16px;
    font-weight: bold;
    background: rgba(255,255,255,0.25);
    color: white;
    border: 1px solid rgba(255,255,255,0.25);
    transition: 0.3s;
}

div.stButton > button:hover {
    background: rgba(255,255,255,0.40);
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #ffdde1, #ee9ca7, #a1c4fd, #c2e9fb);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.hero {
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(12px);
    text-align: center;
    margin-top: 20px;
    color: white;
}

.hero-title {
    font-size: 50px;
    font-weight: 900;
}

.hero-subtitle {
    font-size: 18px;
    opacity: 0.95;
}

.card {
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(12px);
    padding: 18px;
    border-radius: 18px;
    margin-top: 18px;
    color: white;
}

.card-title {
    font-size: 22px;
    font-weight: 800;
}

.footer {
    text-align:center;
    color:white;
    opacity:0.85;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="hero-title">📘 About KeyMood AI</div>
    <div class="hero-subtitle">
        Federated Emotion Detection using Keystroke Dynamics <br>
        Privacy Preserving AI System
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- CONTENT ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">📌 Project Summary</div><br>
        KeyMood AI is a behaviour-based emotion detection system that predicts emotions
        using typing patterns (keystroke dynamics).  
        <br><br>
        It is designed to work in real-time while ensuring user privacy.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">🧠 Key Features</div><br>
        ✅ Typing Speed Measurement <br>
        ✅ Error Rate Analysis <br>
        ✅ Hold Time & Inter-Key Delay <br>
        ✅ Emotion Prediction with Confidence <br>
        ✅ Dashboard History Tracking <br>
        ✅ Federated Learning Support
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">🔐 Privacy Advantage</div><br>
        Federated Learning ensures that the user's raw keystroke data stays on their device.
        Only trained model parameters are shared with the global model.
        <br><br>
        This makes KeyMood AI secure, privacy-preserving, and scalable.
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-title">🎯 Applications</div><br>
        💼 Workplace Stress Monitoring <br>
        🧘 Mental Health Tracking <br>
        🎮 Gaming Emotion Detection <br>
        📱 Personalized User Experience <br>
        🏫 Student Stress Analysis <br>
        🏥 Healthcare Support Systems
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div class="card">
    <div class="card-title">🚀 Future Enhancements</div><br>
    🔹 Real-time keystroke capture using advanced event tracking <br>
    🔹 Deep Learning based emotion prediction models <br>
    🔹 Support for mobile keyboards and multilingual typing <br>
    🔹 Improved federated aggregation and security methods <br>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='footer'>© 2026 KeyMood AI | Minor Project</div>", unsafe_allow_html=True)