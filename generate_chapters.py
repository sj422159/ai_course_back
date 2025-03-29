import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_chapter_titles(course_name: str):
    """
    Generate a structured list of Indian-style chapter titles using Gemini AI.
    """
    prompt = f"""
    You are an expert Indian curriculum designer. Generate a list of **comprehensive** chapter titles 
    for a course on "{course_name}". Ensure it follows a **structured Indian learning format**, covering 
    both **basic and advanced** topics. The chapters should be **progressively arranged**, starting 
    with fundamental concepts and leading up to advanced applications.

    **Guidelines:**
    - Provide at least **8 to 12 chapter titles** (more if necessary).
    - Use **simple yet informative** language suited for Indian students.
    - **Include real-life applications**, Indian examples, and cultural relevance where possible.
    - Ensure it follows a **logical progression** from introduction to mastery.
    - The final chapter should be a **project or assessment-based module**.

    **Example for a Python Course in India:**
    1. Introduction to Python: Understanding the Basics  
    2. Setting Up Python: Installation & First Program  
    3. Variables and Data Types in Python  
    4. Control Flow: If-Else Conditions & Loops  
    5. Functions and Modules in Python  
    6. Object-Oriented Programming: Classes & Objects  
    7. File Handling in Python: Reading & Writing Files  
    8. Introduction to Libraries: NumPy, Pandas & Matplotlib  
    9. Real-Life Applications: Python in Web Development & AI  
    10. Capstone Project: Developing a Python-Based Application  

    Now, generate a similar **structured chapter list** for "{course_name}".
    """

    try:
        response = genai.generate_text(prompt=prompt)
        return response.text.strip().split("\n")
    except Exception as e:
        raise Exception(f"Error generating chapters: {str(e)}")
