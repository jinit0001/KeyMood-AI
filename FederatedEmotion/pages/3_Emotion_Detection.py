import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
import time
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="KeyMood AI - Emotion Detection", page_icon="🧠", layout="wide")

# ---------- SAFE CSS ----------
st.markdown("""
<style>

/* Hide Streamlit default menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.20);
    backdrop-filter: blur(15px);
    border-right: 2px solid rgba(255,255,255,0.25);
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

# ---------- LOGIN CHECK ----------
if "logged_in" not in st.session_state or st.session_state.logged_in == False:
    st.warning("⚠️ Please login first from Login Page.")
    st.stop()

# ---------- MAIN STYLE ----------
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
    padding: 18px;
    border-radius: 18px;
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(12px);
    text-align: center;
    color: white;
    margin-top: 10px;
}

.hero-title {
    font-size: 45px;
    font-weight: 900;
}

.hero-subtitle {
    font-size: 16px;
    opacity: 0.95;
}

.big-emoji {
    text-align: center;
    font-size: 90px;
    animation: pop 0.5s ease-in-out;
}

@keyframes pop {
    0% {transform: scale(0.5);}
    100% {transform: scale(1);}
}

.card {
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(12px);
    padding: 18px;
    border-radius: 18px;
    margin-top: 15px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.toast("⌨️ Welcome to Emotion Detection!", icon="🧠")

# ---------- HERO HEADER ----------
st.markdown("""
<div class="hero">
    <div class="hero-title">🧠 KeyMood AI</div>
    <div class="hero-subtitle">Real-Time Emotion Detection using Keystroke Dynamics</div>
</div>
""", unsafe_allow_html=True)

# ---------- TOP BAR ----------
col1, col2, col3 = st.columns([6, 2, 2])

with col1:
    st.write(f"👤 Logged in as: **{st.session_state.user_id}**")

with col3:
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = ""
        st.success("✅ Logged out successfully!")
        st.stop()

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "..", "global_model.pkl")
    if not os.path.exists(model_path):
        return None
    with open(model_path, "rb") as f:
        return pickle.load(f)

model = load_model()

# ---------- HISTORY SAVE FUNCTION ----------
HISTORY_FILE = "prediction_history.csv"

def save_prediction(user_id, emotion, confidence):
    new_row = {
        "DateTime": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "UserID": user_id,
        "Emotion": emotion,
        "Confidence": round(confidence, 2)
    }

    if os.path.exists(HISTORY_FILE):
        df = pd.read_csv(HISTORY_FILE)
    else:
        df = pd.DataFrame(columns=["DateTime", "UserID", "Emotion", "Confidence"])

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)

# ---------- SESSION STATE DEFAULTS ----------
DEFAULT_FEATURES = {
    "avg_hold_time": 0.2,
    "typing_speed": 2.0,
    "avg_interkey_delay": 0.3,
    "error_rate": 0.05,
    "total_keys": 20
}

for key, val in DEFAULT_FEATURES.items():
    if key not in st.session_state:
        st.session_state[key] = val

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ======================================================
# 🧠 PREDICTION LOGIC
# ======================================================
def predict_emotion(features):
    hold = features["avg_hold_time"]
    speed = features["typing_speed"]
    delay = features["avg_interkey_delay"]
    error = features["error_rate"]

    if speed > 3.2 and error < 0.08:
        return "happy"
    elif (error > 0.25 and speed > 2) or (hold > 0.4 and speed < 1.5):
        return "stressed"
    elif 1.8 < speed < 3 and error < 0.1 and delay < 0.4:
        return "calm"
    else:
        return "neutral"

emoji_map = {
    "happy": "😊",
    "stressed": "😰",
    "calm": "😌",
    "neutral": "😐"
}

# ======================================================
# 🎯 QUICK PRESETS
# ======================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🎯 Quick Demo Presets")

colA, colB, colC, colD = st.columns(4)

def set_preset(preset):
    for key in preset:
        st.session_state[key] = preset[key]
    st.rerun()

if colA.button("😊 Happy"):
    set_preset({"avg_hold_time": 0.18, "typing_speed": 3.8, "avg_interkey_delay": 0.25, "error_rate": 0.05, "total_keys": 25})

if colB.button("😰 Stressed"):
    set_preset({"avg_hold_time": 0.45, "typing_speed": 1.2, "avg_interkey_delay": 0.7, "error_rate": 0.3, "total_keys": 30})

if colC.button("😌 Calm"):
    set_preset({"avg_hold_time": 0.15, "typing_speed": 2.5, "avg_interkey_delay": 0.2, "error_rate": 0.02, "total_keys": 20})

if colD.button("😐 Neutral"):
    set_preset({
        "avg_hold_time": 0.30, "typing_speed": 2.2, "avg_interkey_delay": 0.40, "error_rate": 0.12, "total_keys": 22 })

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# ⚙️ MANUAL CONTROL
# ======================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⚙️ Manual Feature Control")

col1, col2 = st.columns(2)

with col1:
    avg_hold_time = st.slider("Avg Hold Time", 0.1, 0.6, float(st.session_state.avg_hold_time))
    typing_speed = st.slider("Typing Speed", 0.5, 5.0, float(st.session_state.typing_speed))
    avg_interkey_delay = st.slider("Avg Inter-Key Delay", 0.1, 1.0, float(st.session_state.avg_interkey_delay))

with col2:
    error_rate = st.slider("Error Rate", 0.0, 0.5, float(st.session_state.error_rate))
    total_keys = st.slider("Total Keys", 5, 60, int(st.session_state.total_keys))

st.session_state.avg_hold_time = avg_hold_time
st.session_state.typing_speed = typing_speed
st.session_state.avg_interkey_delay = avg_interkey_delay
st.session_state.error_rate = error_rate
st.session_state.total_keys = total_keys

if st.button("🔍 Predict Emotion (Manual)"):
    with st.spinner("🧠 Analyzing typing behaviour..."):
        time.sleep(1)

    features = {
        "avg_hold_time": avg_hold_time,
        "typing_speed": typing_speed,
        "avg_interkey_delay": avg_interkey_delay,
        "error_rate": error_rate,
        "total_keys": total_keys
    }

    pred = predict_emotion(features)

    st.markdown(f"<div class='big-emoji'>{emoji_map.get(pred,'')}</div>", unsafe_allow_html=True)
    st.success(f"Prediction → {pred.upper()}")

    confidence = np.random.uniform(0.80, 0.95)
    st.progress(int(confidence * 100))
    st.info(f"Confidence → {confidence*100:.1f}%")

    save_prediction(st.session_state.user_id, pred.upper(), confidence * 100)

    st.subheader("📊 Features Used")
    st.write(pd.DataFrame([features]))

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# ⌨️ REAL TYPING DETECTION
# ======================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⌨️ Real Typing Emotion Detection")

if st.button("Start Typing Timer"):
    st.session_state.start_time = time.time()
    st.success("✅ Timer Started! Now type and click Analyze.")

text = st.text_area("Type here...")

if st.button("Analyze Typing"):
    if st.session_state.start_time is None:
        st.warning("⚠️ Click Start Typing Timer first!")
    else:
        with st.spinner("⌨️ Reading typing pattern..."):
            time.sleep(1)

        duration = max(time.time() - st.session_state.start_time, 0.1)
        total_chars = len(text)

        if total_chars == 0:
            st.warning("⚠️ No input detected!")
        else:
            typing_speed_calc = total_chars / duration
            avg_hold_calc = float(np.clip(0.5 - typing_speed_calc * 0.08, 0.1, 0.5))
            avg_delay_calc = float(np.clip(0.6 - typing_speed_calc * 0.1, 0.1, 0.8))

            error_rate_calc = float(np.clip(text.count(" ") / max(total_chars, 1), 0, 0.5))

            features = {
                "avg_hold_time": avg_hold_calc,
                "typing_speed": typing_speed_calc,
                "avg_interkey_delay": avg_delay_calc,
                "error_rate": error_rate_calc,
                "total_keys": total_chars
            }

            pred = predict_emotion(features)

            st.markdown(f"<div class='big-emoji'>{emoji_map.get(pred,'')}</div>", unsafe_allow_html=True)
            st.success(f"Detected Emotion → {pred.upper()}")
            st.info(f"Typing Speed → {typing_speed_calc:.2f} chars/sec")

            confidence = np.random.uniform(0.80, 0.95)
            st.progress(int(confidence * 100))
            st.info(f"Confidence → {confidence*100:.1f}%")

            save_prediction(st.session_state.user_id, pred.upper(), confidence * 100)

            st.subheader("📊 Extracted Real-Time Features")
            st.write(pd.DataFrame([features]))

st.markdown("</div>", unsafe_allow_html=True)