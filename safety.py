"""
safety.py — Risk scoring + emergency contact escalation for KeyMood AI.

This is a lightweight, rule-based first version of the "SOS / Guardian"
module from the wider product plan. It combines:
  1. Emotion signal (from typing pattern or text analysis)
  2. Sustained-negative-emotion trend (session history)
  3. Explicit crisis-language detection in typed/document text

...into a single risk level (low / medium / high) with a clear reason,
plus an emergency-contact alert flow the user can trigger.

NOTE: This is a triage/awareness layer, not a diagnostic or clinical
tool. It should always be paired with real crisis resources and a
human in the loop — it should never be the only safety net.
"""

import re
import time
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────────────────────────────────

# Emotions treated as "negative" for trend tracking (sustained negativity
# across a session raises risk even without explicit crisis language).
NEGATIVE_EMOTIONS = {"sadness", "anger", "fear", "anxious", "disgust", "grief"}

# A small, general set of phrases that indicate a person may be in crisis.
# This is intentionally coarse (pattern-level, not exhaustive) — it exists
# to trigger a supportive response and route to real help, not to make a
# clinical judgement.
CRISIS_PATTERNS = [
    r"\bkill(ing)? myself\b",
    r"\bend(ing)? my life\b",
    r"\bwant(ed)? to die\b",
    r"\bsuicid(e|al)\b",
    r"\bhurt(ing)? myself\b",
    r"\bself[\s-]?harm\b",
    r"\bno reason to (live|go on)\b",
    r"\bcan'?t (go on|do this anymore)\b",
]
_CRISIS_RE = re.compile("|".join(CRISIS_PATTERNS), re.IGNORECASE)

CRISIS_RESOURCES_MD = """
**If you're going through something difficult, you don't have to handle it alone.**

- 🇺🇸 US: **988** (Suicide & Crisis Lifeline) — call or text, 24/7
- 🌍 International: [findahelpline.com](https://findahelpline.com) — find a local helpline
- If someone is in immediate danger, contact local emergency services.
"""


# ─────────────────────────────────────────────────────────────────────────
#  SESSION STATE HELPERS
# ─────────────────────────────────────────────────────────────────────────

def _ensure_state():
    if "emotion_history" not in st.session_state:
        st.session_state.emotion_history = []          # list of (timestamp, emotion)
    if "emergency_contacts" not in st.session_state:
        st.session_state.emergency_contacts = []        # list of dicts
    if "alert_log" not in st.session_state:
        st.session_state.alert_log = []                 # list of dicts


def record_emotion(emotion_label: str):
    """Call this every time an emotion is detected (typing or document)."""
    _ensure_state()
    st.session_state.emotion_history.append((time.time(), emotion_label.lower()))
    # keep last 20 readings only
    st.session_state.emotion_history = st.session_state.emotion_history[-20:]


def _negative_streak():
    """How many of the most recent readings in a row are negative."""
    streak = 0
    for _, emo in reversed(st.session_state.emotion_history):
        if emo in NEGATIVE_EMOTIONS:
            streak += 1
        else:
            break
    return streak


# ─────────────────────────────────────────────────────────────────────────
#  RISK SCORING
# ─────────────────────────────────────────────────────────────────────────

def assess_risk(text: str = "", emotion_label: str = ""):
    """
    Returns (level, reasons) where level is 'low' | 'medium' | 'high'
    and reasons is a list of short human-readable strings explaining why.
    """
    _ensure_state()
    reasons = []
    level = "low"

    # 1. Explicit crisis language in the text itself -> immediate high risk
    if text and _CRISIS_RE.search(text):
        level = "high"
        reasons.append("Language in the text suggests significant distress.")

    # 2. Sustained negative emotion trend across the session
    streak = _negative_streak()
    if streak >= 4:
        level = "high" if level != "high" else level
        reasons.append(f"{streak} consecutive negative-emotion readings this session.")
    elif streak >= 2:
        if level == "low":
            level = "medium"
        reasons.append(f"{streak} consecutive negative-emotion readings this session.")

    # 3. Single strongly negative reading
    if emotion_label and emotion_label.lower() in {"sadness", "fear", "anxious", "grief"}:
        if level == "low":
            level = "medium"
        reasons.append(f"Current reading: {emotion_label.title()}.")

    if not reasons:
        reasons.append("No significant risk indicators detected.")

    return level, reasons


# ─────────────────────────────────────────────────────────────────────────
#  UI COMPONENTS (call these from app.py)
# ─────────────────────────────────────────────────────────────────────────

_LEVEL_STYLE = {
    "low":    {"color": "#3ddc84", "label": "Low risk"},
    "medium": {"color": "#f5c518", "label": "Medium risk"},
    "high":   {"color": "#ff4d4f", "label": "High risk"},
}


def render_risk_badge(level: str, reasons: list):
    style = _LEVEL_STYLE[level]
    st.markdown(f"""
    <div style="
        margin-top: 0.8rem;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.06);
        border: 1px solid {style['color']}55;
        border-radius: 999px;
        padding: 0.4rem 1rem;
        font-family: 'Inter', sans-serif;
    ">
        <span style="width:9px;height:9px;border-radius:50%;background:{style['color']};display:inline-block;"></span>
        <span style="color:#fff;font-size:0.85rem;font-weight:600;">{style['label']}</span>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("Why this reading?"):
        for r in reasons:
            st.markdown(f"- {r}")

    if level == "high":
        st.markdown(CRISIS_RESOURCES_MD)
        _render_emergency_alert_flow()


def render_emergency_contacts_sidebar():
    """Sidebar UI to add/remove emergency contacts (Guardian module v0)."""
    _ensure_state()
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Emergency contacts**")

    with st.sidebar.form("add_contact_form", clear_on_submit=True):
        name = st.text_input("Name")
        relation = st.text_input("Relation (e.g. parent, friend)")
        contact_info = st.text_input("Phone or email")
        submitted = st.form_submit_button("Add contact")
        if submitted and name and contact_info:
            st.session_state.emergency_contacts.append({
                "name": name, "relation": relation, "contact": contact_info,
            })

    for i, c in enumerate(st.session_state.emergency_contacts):
        cols = st.sidebar.columns([4, 1])
        cols[0].markdown(f"<span style='font-size:0.8rem;color:#c8c8c8;'>{c['name']} ({c['relation']}) — {c['contact']}</span>", unsafe_allow_html=True)
        if cols[1].button("✕", key=f"remove_contact_{i}"):
            st.session_state.emergency_contacts.pop(i)
            st.rerun()


def _render_emergency_alert_flow():
    """Shown inline when risk == high. Lets the user trigger a (simulated)
    alert to their saved emergency contacts.

    NOTE: This does not actually send SMS/email yet — that requires a real
    provider (e.g. Twilio, SMTP) wired up with credentials. It's built to
    slot straight into that once the backend module is ready; for now it
    logs the alert so the flow is demoable end-to-end.
    """
    st.markdown("**You have the option to notify someone you trust.**")
    contacts = st.session_state.emergency_contacts
    if not contacts:
        st.info("No emergency contacts added yet — add one in the sidebar.")
        return

    names = [f"{c['name']} ({c['relation']})" for c in contacts]
    choice = st.selectbox("Notify:", names, key="alert_contact_choice")
    if st.button("Send alert", key="send_alert_btn"):
        chosen = contacts[names.index(choice)]
        st.session_state.alert_log.append({
            "to": chosen["name"],
            "contact": chosen["contact"],
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        st.success(f"Alert queued for {chosen['name']} ({chosen['contact']}). "
                   f"[Demo mode — real SMS/email delivery is the next build step.]")


def render_alert_log():
    """Optional: show a small log of triggered alerts, for the demo."""
    _ensure_state()
    if st.session_state.alert_log:
        with st.expander(f"Alert history ({len(st.session_state.alert_log)})"):
            for a in reversed(st.session_state.alert_log):
                st.markdown(f"- **{a['time']}** → {a['to']} ({a['contact']})")
