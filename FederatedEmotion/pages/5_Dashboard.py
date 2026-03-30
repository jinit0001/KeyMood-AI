import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="KeyMood AI - Dashboard", page_icon="📊", layout="wide")
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


# ---------- LOGIN CHECK ----------
if "logged_in" not in st.session_state or st.session_state.logged_in == False:
    st.warning("⚠️ Please login first from Login Page.")
    st.stop()

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

st.toast("📊 Dashboard Loaded Successfully!", icon="📌")

# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="hero-title">📊 KeyMood AI Dashboard</div>
    <div class="hero-subtitle">Prediction History & Reports</div>
</div>
""", unsafe_allow_html=True)

st.write(f"👤 Logged in as: **{st.session_state.user_id}**")

# ---------- FILE PATH ----------
HISTORY_FILE = "prediction_history.csv"

# ---------- CREATE FILE IF NOT EXISTS ----------
if not os.path.exists(HISTORY_FILE):
    df_init = pd.DataFrame(columns=["DateTime", "UserID", "Emotion", "Confidence"])
    df_init.to_csv(HISTORY_FILE, index=False)

# ---------- LOAD HISTORY ----------
df = pd.read_csv(HISTORY_FILE)

# ---------- FILTER FOR CURRENT USER ----------
user_df = df[df["UserID"] == st.session_state.user_id]

# ---------- RECENT ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📌 Recent Predictions (Last 5)")
if user_df.empty:
    st.warning("No prediction history found for this user.")
else:
    st.table(user_df.tail(5))
st.markdown("</div>", unsafe_allow_html=True)

# ---------- FULL HISTORY ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📜 Full Prediction History")
if user_df.empty:
    st.info("No records available yet.")
else:
    st.dataframe(user_df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------- DOWNLOAD ----------
if not user_df.empty:
    csv_data = user_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download My History (CSV)",
        data=csv_data,
        file_name=f"{st.session_state.user_id}_history.csv",
        mime="text/csv"
    )

# ---------- CLEAR HISTORY ----------
if st.button("🗑️ Clear My History"):
    df = df[df["UserID"] != st.session_state.user_id]
    df.to_csv(HISTORY_FILE, index=False)
    st.success("✅ Your history cleared successfully!")
    st.rerun()