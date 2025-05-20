import streamlit as st
import pytesseract
from PIL import Image
import requests
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Optional: Set Tesseract path for macOS
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Perplexity Sonar config
API_URL = "https://api.perplexity.ai/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
MODEL = "sonar-small-chat"  # or sonar-medium-chat

def extract_text(image: Image.Image) -> str:
    return pytesseract.image_to_string(image).strip()

def ask_ai(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[API ERROR] {str(e)}"

# Streamlit UI
st.set_page_config(page_title="OCR + AI Chat", layout="centered")
st.title("🖼️ Screenshot Q&A via OCR + 🤖 Perplexity AI")

uploaded_file = st.file_uploader("Upload a screenshot", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Extracting text..."):
        extracted_text = extract_text(image)

    st.subheader("📜 Extracted Text")
    st.text_area("OCR Result", extracted_text, height=200)

    if extracted_text:
        with st.spinner("Asking AI..."):
            ai_answer = ask_ai(extracted_text)

        st.subheader("💡 AI Response")
        st.text_area("Answer", ai_answer, height=300)
