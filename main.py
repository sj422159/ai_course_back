from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
import re
import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class ChapterRequest(BaseModel):
    course_name: str




class ChapterAccessRequest(BaseModel):
    courseTitle: str  # Only courseTitle is required now

# Ensure GEMINI_API_KEY is set
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY is missing. Set it before running the server.")

genai.configure(api_key=GEMINI_API_KEY)

courses = {}  # Dictionary to store generated chapters

def generate_chapters_ai(course_name: str):
    prompt = f"""
    You are an expert Indian curriculum designer. Generate exactly **4 chapter titles** for a course on "{course_name}".
    - Only provide **chapter names** without numbering, descriptions, or additional formatting.
    - Keep the names concise, professional, and well-structured.
    - Do not use any bullet points, asterisks, or extra symbols.
    - Ensure logical progression from basic to advanced concepts.

    Generate only the **plain text** chapter names for "{course_name}".
    """

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)

    # Ensure response contains text
    if not response or not hasattr(response, "text") or not response.text.strip():
        raise HTTPException(status_code=500, detail="Failed to generate chapter titles from Gemini API")

    raw_chapters = response.text.strip().split("\n")
    cleaned_chapters = [re.sub(r"^[*\d\.\-\s]+", "", chapter).strip() for chapter in raw_chapters]

    courses[course_name] = cleaned_chapters[:4]  # Store chapters
    print("📌 Courses Dictionary:", courses)  # Debugging
    return courses[course_name]

@app.post("/generate-chapters/")
async def generate_chapters(request: ChapterRequest):
    chapters = generate_chapters_ai(request.course_name)
    return {"chapters": chapters}


@app.post("/api/chapter-access")
async def generate_course_content(request: ChapterAccessRequest):
    try:
        course_title = request.courseTitle.strip()
        chapter_title = request.chapterTitle.strip()

        # Validate inputs
        if not course_title or not chapter_title:
            raise HTTPException(status_code=400, detail="❌ Course and chapter titles are required.")

        # Prepare structured prompt
        prompt = (
            f"Generate a well-structured and clean lesson for the chapter '{chapter_title}' "
            f"in the course '{course_title}'. The content should be properly formatted with:\n"
            "- A clear **Introduction**\n"
            "- **Explanations** with real-world examples\n"
            "- **Key Takeaways**\n"
            "- **Important Concepts**\n"
            "- **Practical Applications** if relevant\n"
            "Ensure the response is clear, professional, and formatted properly for direct use."
        )

        # Generate content asynchronously
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = await model.generate_content_async(prompt)

        # Validate API response
        if not response or not hasattr(response, "text") or not response.text.strip():
            raise HTTPException(status_code=500, detail="❌ Failed to generate content from Gemini API.")

        # Process and clean response text
        generated_content = response.text.strip()
        
        # Return only the cleaned content
        return generated_content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Internal Server Error: {str(e)}")
