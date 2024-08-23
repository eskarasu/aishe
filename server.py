from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Generative AI model setup
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""
        - You are AIShe, an AI designed to uplift, inspire, and support women. Your responses should always be positive, empowering, and encouraging. 
        - Speak with warmth, compassion, and a genuine desire to make the user feel good about themselves.
        - Provide thoughtful compliments, motivational messages, and words of encouragement.
        - Always remember old messages
    """
)

# JSON dosyasının yolu
CHAT_HISTORY_FILE = "chat_history.json"

# JSON dosyasını yükle
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# JSON dosyasına yaz
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

@app.route("/chat", methods=["POST"])
def chat():
    # Sohbet geçmişini yükle
    chat_history = load_chat_history()

    data = request.json
    user_message = data.get("message", "")

    # Kullanıcı mesajını geçmişe ekle
    chat_history.append({
        "role": "user",
        "parts": [user_message],
    })

    chat_session = model.start_chat(
        history=chat_history
    )
    response = chat_session.send_message(user_message)

    # Model cevabını geçmişe ekle
    chat_history.append({
        "role": "model",
        "parts": [response.text],
    })

    # Sohbet geçmişini kaydet
    save_chat_history(chat_history)

    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
