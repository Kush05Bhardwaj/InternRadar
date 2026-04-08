import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def score_internship(description):
    prompt = f"""
        You are a strict evaluator.

        Analyze this internship:

        {description}

        Return ONLY in this exact format (no extra text):

        score: X
        reason: Y

        Rules:
        - Score between 0 to 10
        - Prefer remote roles
        - Prefer beginner friendly
        - Prefer Python/Web/AI relevance
    """

    try:
        response = model.generate_content(prompt)
        output = response.text

        lines = output.split("\n")

        score_line = [l for l in lines if "score" in l.lower()]
        reason_line = [l for l in lines if "reason" in l.lower()]

        if not score_line:
            return 0, "No score returned"

        score = int(score_line[0].split(":")[1].strip())

        reason = reason_line[0] if reason_line else "No reason"

        return score, reason

    except Exception as e:
        print("Gemini Error:", e)
        return 0, "Error"