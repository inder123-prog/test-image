import os
import requests
from PIL import Image
import pytesseract
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Perplexity Sonar API config
API_URL = "https://api.perplexity.ai/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
MODEL = "sonar"  # or sonar-medium-chat / sonar-large-chat

def extract_text_from_image(image_path: str) -> str:
    """Extracts text using OCR from the screenshot"""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"[OCR ERROR] {str(e)}"

def ask_ai(prompt: str) -> str:
    """Sends prompt to Perplexity Sonar and returns response"""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"[API ERROR] {str(e)}"

def main():
    print("🖼️ Screenshot Chatbot via Perplexity Sonar\n")
    image_path = input("Enter path to the screenshot image (e.g., screenshot.png): ").strip()

    if not os.path.exists(image_path):
        print("[ERROR] File not found.")
        return

    print("📤 Extracting text from image...")
    text = extract_text_from_image(image_path)

    if not text:
        print("[WARNING] No text found in image.")
        return

    print(f"\n📜 Extracted Text:\n{text}\n")

    print("🤖 Sending to Perplexity Sonar...")
    ai_response = ask_ai(text)
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
    print(f"\n🧠 AI Response:\n{ai_response}\n")

if __name__ == "__main__":
    main()
