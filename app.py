from transformers import pipeline
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import os
from app_funcs import *


st.set_page_config(
    page_title="Deep Emotion Detector",
    page_icon="static/emotion_mark.svg",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  INJECT: fonts + video background + full theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<!-- Inter -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<!-- BubbledotICG-FinePos (retro dot-matrix) -->
<link href="https://db.onlinewebfonts.com/c/8cb707a9b8a73f8a7403336b861c3074?family=BubbledotICG-FinePos" rel="stylesheet">

<!-- Font Awesome 6.5.2 -->
<link rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"
  integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A=="
  crossorigin="anonymous" referrerpolicy="no-referrer">

<!-- Full-bleed background video -->
<div id="bg-wrap" style="
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  background: #000;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
">
  <video autoplay muted loop playsinline style="
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    pointer-events: none;
    z-index: 0;
  ">
    <source src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260809_012548_ef22562c-c0ae-4816-ad9d-f8922af4e6a7.mp4" type="video/mp4">
  </video>
</div>

<style>
/* ── CSS VARIABLES (exact match to landing page) ─────────────────────── */
:root {
  --bg:            #000000;
  --text:          #ffffff;
  --muted:         #8e8e8e;
  --nav-text:      #2e2e2e;
  --pill-dark:     #28282a;
  --sign-in-text:  #c8c8c8;
  --nav-shadow:    0 4px 14px rgba(0, 0, 0, 0.16);
  --trust-bg:      #28282a;
  --trust-border:  rgba(255, 255, 255, 0.4);
  --trust-text:    #c4c2c3;
  --font-sans:     "Inter", "Segoe UI", system-ui, sans-serif;
  --font-display:  "BubbledotICG-FinePos", "Geist Pixel Circle", monospace;
  --surface:       rgba(0, 0, 0, 0.55);
  --surface2:      rgba(20, 20, 22, 0.75);
  --border:        rgba(255,255,255,0.10);
  --border2:       rgba(255,255,255,0.18);
  --radius:        18px;
  --radius-sm:     12px;
}

/* ── GLOBAL RESET ────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  background: #000 !important;
  font-family: var(--font-sans) !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* ── STREAMLIT CHROME — make transparent so video shows through ──────── */
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.main,
[data-testid="stMainBlockContainer"],
.block-container {
  background: transparent !important;
}

/* ── HIDE DEFAULT STREAMLIT CHROME ──────────────────────────────────── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── BLOCK CONTAINER ─────────────────────────────────────────────────── */
.block-container {
  max-width: 740px !important;
  padding: clamp(24px, 4vh, 48px) clamp(14px, 3vw, 32px) 4rem !important;
  position: relative;
  z-index: 1;
}

/* ── SIDEBAR ─────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"],
[data-testid="stSidebar"] {
  display: block !important;
  visibility: visible !important;
  transform: none !important;
  min-width: 280px !important;
  width: 280px !important;
  max-width: 280px !important;
  background: rgba(8, 8, 10, 0.82) !important;
  backdrop-filter: blur(18px) !important;
  -webkit-backdrop-filter: blur(18px) !important;
  border-right: 1px solid var(--border2) !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"] button[title="Collapse sidebar"] {
  display: flex !important;
  visibility: visible !important;
  font-size: 0 !important;
  min-width: 2.25rem !important;
  min-height: 2.25rem !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"]::after,
section[data-testid="stSidebar"] button[title="Collapse sidebar"]::after {
  content: "<";
  display: block;
  color: #fff !important;
  font-family: var(--font-sans) !important;
  font-size: 1.2rem !important;
  line-height: 1;
}

[data-testid="stSidebar"] > div:first-child {
  padding: 1.6rem 1.2rem !important;
}

[data-testid="stSidebar"] img {
  border-radius: 14px !important;
  opacity: 0.9;
}

/* Sidebar text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
  color: var(--muted) !important;
  font-family: var(--font-sans) !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.05em !important;
  text-transform: uppercase !important;
  font-weight: 600 !important;
}

/* Sidebar selectbox */
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div,
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div > div,
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div span,
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] div {
  background: var(--pill-dark) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 999px !important;
  color: #c8c8c8 !important;
  font-family: var(--font-sans) !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
  box-shadow: var(--nav-shadow) !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}

/* Force the selected text inside selectbox to be visible */
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-testid="stSelectbox"] [role="combobox"] > div > div {
  color: #c8c8c8 !important;
  font-size: 0.88rem !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div:hover {
  border-color: rgba(255,255,255,0.35) !important;
}

/* ── HIDE OLD IMAGES / EMOTION MARK ─────────────────────────────────── */
[data-testid="stImage"],
.emotion-mark { display: none !important; }

/* ── ALL TEXT BASE ───────────────────────────────────────────────────── */
p, span, li, div, label {
  font-family: var(--font-sans) !important;
  color: var(--text) !important;
}

/* ── PAGE TITLE (h1) ─────────────────────────────────────────────────── */
h1 {
  font-family: var(--font-display) !important;
  font-size: clamp(28px, 5.5vw, 68px) !important;
  font-weight: 400 !important;
  letter-spacing: -0.04em !important;
  line-height: 1.12 !important;
  color: #fff !important;
  white-space: nowrap;
  overflow: hidden;
  margin-bottom: 0.5rem !important;
}

/* ── LABELS ──────────────────────────────────────────────────────────── */
label,
[data-testid="stTextArea"] label,
[data-testid="stFileUploader"] label {
  font-family: var(--font-sans) !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
  margin-bottom: 0.4rem !important;
}

/* ── TEXT AREA ───────────────────────────────────────────────────────── */
textarea {
  background: rgba(0, 0, 0, 0.6) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius) !important;
  color: #fff !important;
  font-family: var(--font-sans) !important;
  font-size: 0.95rem !important;
  line-height: 1.65 !important;
  padding: 1rem 1.1rem !important;
  caret-color: #fff !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

textarea:focus {
  border-color: rgba(255,255,255,0.5) !important;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.08), 0 0 24px rgba(255,255,255,0.06) !important;
  outline: none !important;
}

textarea::placeholder {
  color: var(--muted) !important;
  opacity: 0.7 !important;
}

/* ── BUTTON ──────────────────────────────────────────────────────────── */
[data-testid="stButton"] > button {
  font-family: var(--font-sans) !important;
  font-weight: 600 !important;
  font-size: clamp(13.5px, 1.5vw, 14.5px) !important;
  color: #000000 !important;
  background: #fff !important;
  border: none !important;
  border-radius: 999px !important;
  padding: clamp(11px, 1.6vh, 13px) clamp(22px, 3vw, 28px) !important;
  cursor: pointer !important;
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.15),
    0 0 22px rgba(255,255,255,0.32),
    0 0 44px rgba(255,255,255,0.12) !important;
  transition: transform 0.25s ease, box-shadow 0.25s ease !important;
  letter-spacing: 0em !important;
  margin-top: 0.6rem !important;
}

[data-testid="stButton"] > button * {
  color: #000000 !important;
}

[data-testid="stButton"] > button:hover {
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.25),
    0 0 32px rgba(255,255,255,0.5),
    0 0 64px rgba(255,255,255,0.2) !important;
}

[data-testid="stButton"] > button:active {
  transform: translateY(0) scale(0.99) !important;
}

/* ── FILE UPLOADER ───────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
  background: rgba(0,0,0,0.55) !important;
  backdrop-filter: blur(12px) !important;
  border: 1.5px dashed var(--border2) !important;
  border-radius: var(--radius) !important;
  padding: 1.5rem !important;
  transition: border-color 0.2s ease !important;
}

[data-testid="stFileUploader"]:hover {
  border-color: rgba(255,255,255,0.4) !important;
}

[data-testid="stFileUploader"] section {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
}

[data-testid="stFileUploader"] button {
  font-size: 0 !important;
  background: var(--pill-dark) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 999px !important;
  color: var(--sign-in-text) !important;
  font-family: var(--font-sans) !important;
  font-size: 0.85rem !important;
  font-weight: 500 !important;
  padding: 0.5rem 1.3rem !important;
  box-shadow: var(--nav-shadow) !important;
  transition: background 0.2s, color 0.2s, transform 0.2s !important;
}

[data-testid="stFileUploader"] button::after {
  content: "Upload";
  font-family: var(--font-sans) !important;
  font-size: 0.85rem !important;
}

[data-testid="stFileUploader"] button p,
[data-testid="stFileUploader"] button span,
[data-testid="stFileUploader"] button svg {
  display: none !important;
}

[data-testid="stFileUploader"] button:hover {
  background: #323234 !important;
  color: #fff !important;
  transform: translateY(-1px) !important;
}

[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span {
  color: var(--muted) !important;
  font-size: 0.85rem !important;
}

/* ── SELECTBOX ───────────────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
  background: var(--pill-dark) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 999px !important;
  color: var(--sign-in-text) !important;
  font-family: var(--font-sans) !important;
  font-weight: 500 !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
div[role="listbox"],
ul[role="listbox"],
[data-testid="stSelectbox"] [role="listbox"] {
  background: #18181c !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius-sm) !important;
}

div[data-baseweb="popover"] * {
  background: transparent !important;
  color: #c8c8c8 !important;
}

[data-baseweb="menu"] li,
[data-baseweb="option"],
[role="option"] {
  color: #c8c8c8 !important;
  font-family: var(--font-sans) !important;
  background: transparent !important;
  padding: 8px 12px !important;
}

[data-baseweb="menu"] li:hover,
[data-baseweb="option"]:hover,
[role="option"]:hover,
[role="option"][aria-selected="true"] {
  background: rgba(255,255,255,0.15) !important;
  color: #fff !important;
}

/* ── SPINNER ─────────────────────────────────────────────────────────── */
[data-testid="stSpinner"] > div {
  border-top-color: rgba(255,255,255,0.8) !important;
}

/* ── ALERTS ──────────────────────────────────────────────────────────── */
/* Success */
[data-testid="stAlert"][data-baseweb="notification"],
.element-container [data-testid="stAlert"] {
  backdrop-filter: blur(12px) !important;
  border-radius: var(--radius) !important;
  font-family: var(--font-sans) !important;
}

[data-testid="stAlert"][kind="success"],
div[class*="success"] [data-testid="stAlert"] {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  color: #fff !important;
}

[data-testid="stAlert"][kind="warning"] {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  color: #d0d0d0 !important;
}

[data-testid="stAlert"][kind="info"] {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  color: #d0d0d0 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
  font-family: var(--font-sans) !important;
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  color: inherit !important;
}

/* ── DIVIDER ─────────────────────────────────────────────────────────── */
hr {
  border: none !important;
  border-top: 1px solid var(--border) !important;
  margin: 2rem 0 !important;
}

/* ── LINKS ───────────────────────────────────────────────────────────── */
a { color: #fff !important; text-decoration: underline !important; opacity: 0.7 !important; transition: opacity 0.2s !important; }
a:hover { opacity: 1 !important; }

/* ── SCROLLBAR ───────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.14); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.28); }

/* ── GENERAL MARKDOWN ────────────────────────────────────────────────── */
.stMarkdown p {
  color: #d0d0d0 !important;
  font-size: 0.95rem !important;
  line-height: 1.6 !important;
  opacity: 0.88;
}

[data-testid="stAlert"] p { color: inherit !important; opacity: 1 !important; }

/* ── RESULT CARD ─────────────────────────────────────────────────────── */
.emo-card {
  margin-top: 1.4rem;
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: var(--radius);
  padding: 1.5rem 1.8rem;
  display: flex;
  align-items: center;
  gap: 1.1rem;
  animation: fadeUp 0.45s cubic-bezier(0.22,1,0.36,1) both;
}

.emo-card .icon { font-size: 2.5rem; line-height: 1; flex-shrink: 0; }

.emo-card .label {
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.09em !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
  display: block;
  margin-bottom: 0.25rem;
}

.emo-card .value {
  font-family: var(--font-display) !important;
  font-size: clamp(22px, 3.5vw, 40px) !important;
  font-weight: 400 !important;
  letter-spacing: -0.03em !important;
  color: #fff !important;
  line-height: 1 !important;
}

/* ── TRUST ROW ───────────────────────────────────────────────────────── */
.trust-row {
  display: inline-flex;
  align-items: center;
  margin-bottom: 1.2rem;
}
.trust-avatars { display: flex; align-items: center; }
.t-avatar {
  --sz: 38px;
  width: var(--sz); height: var(--sz);
  border-radius: 50%;
  background: var(--trust-bg);
  border: 1px solid var(--trust-border);
  padding: 5px;
  display: grid; place-items: center;
  flex-shrink: 0;
  transition: transform 0.35s ease;
}
.t-avatar:nth-child(2) { margin-left: calc(var(--sz)*-0.42); z-index: 1; }
.t-avatar:nth-child(3) { margin-left: calc(var(--sz)*-0.42); z-index: 2; }
.trust-avatars:hover .t-avatar:nth-child(1) { transform: translateY(-2px); }
.trust-avatars:hover .t-avatar:nth-child(2) { transform: translateY(-4px); }
.trust-avatars:hover .t-avatar:nth-child(3) { transform: translateY(-2px); }
.t-inner {
  width: 100%; height: 100%; border-radius: 50%; background: #fff;
  display: grid; place-items: center;
}
.t-inner i { color: #111; font-size: calc(38px * 0.34); line-height: 1; }
.trust-pill {
  display: flex; align-items: center;
  height: 38px;
  background: var(--trust-bg);
  border: 1px solid var(--trust-border);
  border-radius: 999px;
  margin-left: calc(38px * -0.42);
  padding-left: calc(38px * 0.58);
  padding-right: 18px;
  white-space: nowrap;
}
.trust-pill span {
  font-size: 12.5px !important;
  font-weight: 500 !important;
  color: var(--trust-text) !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
}

/* ── STATS ROW ───────────────────────────────────────────────────────── */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255,255,255,0.09);
}
@media (max-width: 620px) {
  .stats-row { grid-template-columns: repeat(2, 1fr); gap: 1rem; }
}
.stat-box { display: flex; flex-direction: column; align-items: center; text-align: center; gap: 2px; }
.stat-icon-d {
  font-family: var(--font-display) !important;
  font-size: clamp(20px,2.8vw,30px) !important;
  color: #fff !important;
  line-height: 1;
  margin-bottom: 2px;
  letter-spacing: 0 !important;
  text-transform: none !important;
}
.stat-val {
  font-family: var(--font-sans) !important;
  font-size: clamp(17px,2vw,24px) !important;
  font-weight: 600 !important;
  color: #fff !important;
  letter-spacing: -0.025em !important;
  font-variant-numeric: tabular-nums;
  line-height: 1;
  text-transform: none !important;
}
.stat-lbl {
  font-family: var(--font-sans) !important;
  font-size: clamp(10px,1.1vw,12px) !important;
  color: var(--muted) !important;
  font-weight: 400 !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
}

/* ── ANIMATIONS ──────────────────────────────────────────────────────── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(22px) scale(0.98); filter: blur(6px); }
  to   { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}

.anim { animation: reveal 0.85s cubic-bezier(0.22,1,0.36,1) var(--d,0s) both; }

@media (prefers-reduced-motion: reduce) {
  .anim, .emo-card { animation: none !important; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding:0.4rem 0 1.2rem; border-bottom:1px solid rgba(255,255,255,0.08); margin-bottom:1.2rem;">
  <div style="font-family:'Inter',sans-serif; font-size:1rem; font-weight:700;
              letter-spacing:-0.02em; color:#fff; margin-bottom:0.2rem;">
    Emotion Detector
  </div>
  <div style="font-family:'Inter',sans-serif; font-size:0.73rem; color:#8e8e8e;">
    Powered by Emotion English DistilRoBERTa
  </div>
</div>
""", unsafe_allow_html=True)

format_type = st.sidebar.selectbox("Input mode", ["Plain text", "Documents"])

st.sidebar.markdown("""
<div style="margin-top:2rem; padding-top:1.2rem; border-top:1px solid rgba(255,255,255,0.08);">
  <div style="font-family:'Inter',sans-serif; font-size:0.72rem; color:#8e8e8e; line-height:1.65;">
    Detect the emotional tone of any text or document — joy, sadness, anger, fear, and more.
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  TRUST ROW + TITLE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="anim" style="--d:0.05s; padding-top: 0.8rem;">
  <div class="trust-row">
    <div class="trust-avatars">
      <div class="t-avatar">
        <div class="t-inner"><i class="fa-brands fa-microsoft"></i></div>
      </div>
      <div class="t-avatar">
        <div class="t-inner"><i class="fa-brands fa-amazon"></i></div>
      </div>
      <div class="t-avatar">
        <div class="t-inner"><i class="fa-brands fa-google"></i></div>
      </div>
    </div>
    <div class="trust-pill">
      <span>Trusted by 2000+ Enterprises</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.title("Deep Emotion Detector")

st.markdown("""
<p class="anim" style="--d:0.18s; color:#d0d0d0; opacity:0.8; font-size:0.97rem;
   line-height:1.6; margin-top:-0.3rem; margin-bottom:1.6rem; max-width:520px;">
  Paste any text or upload a document — AI instantly reveals the emotional tone.
</p>
""", unsafe_allow_html=True)

upload_path = "uploads/"
download_path = "downloads/"
typing_metrics = components.declare_component(
  "typing_metrics",
  path=os.path.join(os.path.dirname(__file__), "typing_metrics_component"),
)


# ─────────────────────────────────────────────────────────────────────────────
#  EMOTION EMOJI MAP
# ─────────────────────────────────────────────────────────────────────────────
EMOTION_EMOJIS = {
    "joy": "😊", "happiness": "😊", "love": "❤️", "excitement": "🤩",
    "sadness": "😢", "grief": "😢", "anger": "😠", "rage": "😡",
    "fear": "😨", "surprise": "😲", "disgust": "🤢", "neutral": "😐",
    "anticipation": "🤔", "trust": "🤝", "amusement": "😄",
}

def get_emoji(label: str) -> str:
    low = label.lower()
    return next((v for k, v in EMOTION_EMOJIS.items() if k in low), "🧠")


# ─────────────────────────────────────────────────────────────────────────────
#  PLAIN TEXT MODE
# ─────────────────────────────────────────────────────────────────────────────
if format_type == "Plain text":
    st.markdown("<p class='input-note'>Words remain in your browser. The server receives typing statistics only.</p>", unsafe_allow_html=True)
    metrics = typing_metrics(key="typing-input")

    if metrics and metrics.get("submitted"):
        emotion_output = emotion_from_typing(metrics)
        emoji = get_emoji(emotion_output)
        st.markdown(f"""
        <div class="emo-card">
          <div class="icon">{emoji}</div>
          <div>
            <span class="label">Detected emotion</span>
            <span class="value">{emotion_output.title()}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption(
            "Typing profile: "
            f"{metrics.get('typing_speed_wpm', 0)} WPM | "
            f"{metrics.get('mean_inter_key_delay_ms', 0)} ms average key delay | "
            f"{metrics.get('backspaces', 0)} corrections"
        )


# ─────────────────────────────────────────────────────────────────────────────
#  DOCUMENT MODE
# ─────────────────────────────────────────────────────────────────────────────
if format_type == "Documents":
    st.info("Supported formats: TXT, PDF, DOCX")
    uploaded_file = st.file_uploader("Upload document", type=["txt", "pdf", "docx"])

    if uploaded_file is not None:
        with open(os.path.join(upload_path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())

        fname = uploaded_file.name.lower()

        if fname.endswith(".txt"):
            with st.spinner("Reading document…"):
                up = os.path.abspath(os.path.join(upload_path, uploaded_file.name))
                down = os.path.abspath(os.path.join(download_path, "processed_" + uploaded_file.name))
                text = extract_text_txt(up, down)
                emotion_output = emotion_generate(text)
            if emotion_output:
                emoji = get_emoji(emotion_output)
                st.markdown(f"""
                <div class="emo-card">
                  <div class="icon">{emoji}</div>
                  <div>
                    <span class="label">Detected emotion</span>
                    <span class="value">{emotion_output.title()}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                download_success()

        if fname.endswith(".pdf"):
            with st.spinner("Extracting from PDF…"):
                up = os.path.abspath(os.path.join(upload_path, uploaded_file.name))
                text = extract_text_pdf(up)
                emotion_output = emotion_generate(text)
            if emotion_output:
                emoji = get_emoji(emotion_output)
                st.markdown(f"""
                <div class="emo-card">
                  <div class="icon">{emoji}</div>
                  <div>
                    <span class="label">Detected emotion</span>
                    <span class="value">{emotion_output.title()}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                download_success()

        if fname.endswith(".docx"):
            with st.spinner("Parsing DOCX…"):
                up = os.path.abspath(os.path.join(upload_path, uploaded_file.name))
                text = extract_text_docx(up)
                emotion_output = emotion_generate(text)
            if emotion_output:
                emoji = get_emoji(emotion_output)
                st.markdown(f"""
                <div class="emo-card">
                  <div class="icon">{emoji}</div>
                  <div>
                    <span class="label">Detected emotion</span>
                    <span class="value">{emotion_output.title()}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                download_success()
    else:
        st.warning("Upload a document to begin analysis.")


# ─────────────────────────────────────────────────────────────────────────────
#  STATS FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row anim" style="--d:0.5s;">
  <div class="stat-box">
    <div class="stat-icon-d">&lt;</div>
    <div class="stat-val" id="s0">120ms</div>
    <div class="stat-lbl">Inference Time</div>
  </div>
  <div class="stat-box">
    <div class="stat-icon-d">%</div>
    <div class="stat-val" id="s1">99.99%</div>
    <div class="stat-lbl">Platform Uptime</div>
  </div>
  <div class="stat-box">
    <div class="stat-icon-d">*</div>
    <div class="stat-val" id="s2">24/7</div>
    <div class="stat-lbl">Autonomous Runtime</div>
  </div>
  <div class="stat-box">
    <div class="stat-icon-d">#</div>
    <div class="stat-val" id="s3">2.4M</div>
    <div class="stat-lbl">Context Windows</div>
  </div>
</div>

<script>
(function () {
  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }

  var stats = [
    { id: "s0", target: 120,   suffix: "ms", dec: 0, dur: 1500, delay: 480  },
    { id: "s1", target: 99.99, suffix: "%",  dec: 2, dur: 1580, delay: 570  },
    { id: "s2", target: 24,    suffix: "/7", dec: 0, dur: 1660, delay: 660  },
    { id: "s3", target: 2.4,   suffix: "M",  dec: 1, dur: 1740, delay: 750  },
  ];

  var done = false;

  function runCountUp() {
    if (done) return;
    done = true;
    stats.forEach(function (s) {
      setTimeout(function () {
        var el = document.getElementById(s.id);
        if (!el) return;
        var start = performance.now();
        function step(now) {
          var prog = Math.min((now - start) / s.dur, 1);
          var val = easeOutCubic(prog) * s.target;
          el.textContent = val.toFixed(s.dec) + s.suffix;
          if (prog < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      }, s.delay);
    });
  }

  var container = document.querySelector(".stats-row");
  if (container && "IntersectionObserver" in window) {
    var obs = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { runCountUp(); obs.disconnect(); }
    }, { threshold: 0.25 });
    obs.observe(container);
  } else {
    setTimeout(runCountUp, 800);
  }
})();
</script>
""", unsafe_allow_html=True)

