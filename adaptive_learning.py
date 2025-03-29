from fastapi import FastAPI, Body
import google.generativeai as genai
import os
from dotenv import load_dotenv
import sqlite3

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Set it in the .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

app = FastAPI()

# Database setup
conn = sqlite3.connect("learning_progress.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    user_id TEXT PRIMARY KEY,
    topic TEXT,
    difficulty TEXT
)
""")
conn.commit()

def get_adaptive_lesson(topic: str, difficulty: str):
    """Fetch lesson based on topic and difficulty."""
    prompt = f"Generate a {difficulty} level lesson on {topic}. Keep it concise and engaging."
    response = model.generate_content(prompt)
    return response.text.strip()

@app.post("/get_lesson/")
async def get_lesson(user_id: str = Body(...), topic: str = Body(...)):
    """Fetch an adaptive lesson based on user history."""
    cursor.execute("SELECT difficulty FROM progress WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    difficulty = result[0] if result else "medium"
    
    lesson = get_adaptive_lesson(topic, difficulty)
    return {"lesson": lesson, "difficulty": difficulty}

@app.post("/update_progress/")
async def update_progress(user_id: str = Body(...), topic: str = Body(...), feedback: str = Body(...)):
    """Update user progress based on feedback."""
    new_difficulty = "easy" if feedback == "Need More Explanation" else "hard"
    cursor.execute("""
    INSERT INTO progress (user_id, topic, difficulty) VALUES (?, ?, ?) 
    ON CONFLICT(user_id) DO UPDATE SET difficulty = ?
    """, (user_id, topic, new_difficulty, new_difficulty))
    conn.commit()
    return {"message": "Progress updated", "new_difficulty": new_difficulty}
