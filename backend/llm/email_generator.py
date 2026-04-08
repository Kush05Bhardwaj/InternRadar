import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_email(title, company, description):
    prompt = f"""
    Write a short cold email for this internship:

    Role: {title}
    Company: {company}
    Description: {description}

    Candidate:
    - BTech CSE student
    - Skills: Python, React, AI basics
    - Passionate about building real-world projects

    Keep it:
    - Short
    - Professional
    - Personalized

    Output only email (no explanation)
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Error generating email"