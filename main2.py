from fastapi import FastAPI, HTTPException
from ai_module import get_ai_response
from coding_assistant import get_coding_hint
from face_detection import detect_emotion

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Emotion-Aware AI Learning Backend"}


@app.post("/ask-ai/")
def ask_ai(question: str):
    """Fetch AI-generated response from Gemini API."""
    try:
        response = get_ai_response(question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-hint/")
def get_hint(problem: str):
    """Get AI-generated coding hints based on the problem."""
    try:
        hint = get_coding_hint(problem)
        return {"hint": hint}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect-emotion/")
def emotion_analysis(image: bytes):
    """Detect emotion from an image (for now, placeholder logic)."""
    try:
        emotion = detect_emotion(image)
        return {"emotion": emotion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
