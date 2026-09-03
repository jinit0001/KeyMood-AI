import streamlit as st
from transformers import pipeline
import pymupdf as fitz
import docx
import re

@st.cache_resource(show_spinner=False)
def get_emotion_pipeline():
    return pipeline(
        'sentiment-analysis',
        model='j-hartmann/emotion-english-distilroberta-base',
    )


def emotion_generate(plain_text):
    emotion_labels = get_emotion_pipeline()(
        plain_text,
        truncation=True,
        max_length=512,
    )
    return emotion_labels[0]['label']


def emotion_from_typing(metrics):
    speed = metrics.get('typing_speed_wpm', 0)
    delay = metrics.get('mean_inter_key_delay_ms', 0)
    variability = metrics.get('delay_variability_ms', 0)
    correction_rate = metrics.get('corrections', 0) / max(metrics.get('key_count', 1), 1)
    pauses = metrics.get('pauses', 0)

    if correction_rate >= 0.16 or variability >= 900:
        return 'anxious'
    if delay >= 700 or speed < 12 or pauses >= 3:
        return 'sadness'
    if speed >= 70 and correction_rate < 0.05 and variability < 250:
        return 'joy'
    if speed >= 55 and correction_rate >= 0.08:
        return 'anger'
    if delay < 170 and speed >= 45:
        return 'surprise'
    return 'neutral'

@st.cache_data(show_spinner=False)
def extract_text_txt(uploaded_txt_file,downloaded_txt_file):
    with open(uploaded_txt_file) as intxt:
        data = intxt.read()

    data = re.findall('[aA-zZ]+', data)
    with open(downloaded_txt_file, 'w') as outtxt:
        outtxt.write('\n'.join(data))
    return ' '.join(data)


@st.cache_data(show_spinner=False)
def extract_text_pdf(uploaded_pdf_file):
    with fitz.open(uploaded_pdf_file) as intxt:
        text = ""
        for page in intxt:
            text += page.get_text()
    return text


@st.cache_data(show_spinner=False)
def extract_text_docx(uploaded_docx_file):
    doc = docx.Document(uploaded_docx_file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return ' '.join(fullText)


def download_success():
    st.balloons()
