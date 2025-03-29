import cv2
import base64
import numpy as np
import os
import google.generativeai as genai

# Load API Key from environment
GEMINI_API_KEY = "AIzaSyAKn0r8PVTktGLvao3UnvZdQy7wG-cruRo"
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Set it as an environment variable.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Initialize webcam
cap = cv2.VideoCapture(0)

def analyze_emotion_with_gemini(image):
    """Use Gemini AI for real-time facial sentiment analysis."""
    _, buffer = cv2.imencode(".jpg", image)
    image_base64 = base64.b64encode(buffer).decode("utf-8")

    prompt = "Analyze the emotion in this image and classify it strictly into one of the following categories: 'happy', 'sad', 'confused', 'trying hard to solve'. Only return the classification word without any description."

    response = model.generate_content([
        {"text": prompt},
        {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
    ])

    return response.text.strip()

def detect_facial_emotion():
    """Continuously detect emotion using webcam feed."""
    session_emotion = "neutral"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not capture frame")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Emotion Detection", frame)

        # Analyze emotion
        current_emotion = analyze_emotion_with_gemini(gray)

        # Print only if emotion changes
        if current_emotion != session_emotion:
            session_emotion = current_emotion
            print(f"Detected Emotion: {current_emotion}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_facial_emotion()
