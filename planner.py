import os
import json
import re
import google.generativeai as genai

# Configure Google AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

def extract_days(goal_text):
    """Extract number of days from text; default 3."""
    match = re.search(r"(\d+)[-\s]*day", goal_text.lower())
    return int(match.group(1)) if match else 3

def fallback_plan(goal_text, days):
    """Fallback plan if AI fails."""
    return {
        "summary": f"{days}-day demo plan for: {goal_text}",
        "steps": ["Research the goal", "Break into tasks", "Assign time for each day"],
        "day_by_day": [
            {"day": i, "activities": [f"Activity {j} for day {i}" for j in range(1, 6)]}
            for i in range(1, days + 1)
        ]
    }

def generate_plan(goal_text):
    days = extract_days(goal_text)

    prompt = f"""
    You are a travel planner assistant. Generate a realistic {days}-day plan
    for the following goal:

    Goal: {goal_text}

    Respond ONLY in JSON with keys:
    - summary
    - steps
    - day_by_day (list of {{day: int, activities: [str]}})

    Make each day's activities specific and realistic.
    """

    if not model:
        return fallback_plan(goal_text, days)

    response = model.generate_content(prompt)
    text = response.text.strip()

    # Try to extract JSON if AI wrapped it in ```json
    try:
        match = re.search(r"```json(.*?)```", text, re.DOTALL)
        if match:
            text = match.group(1).strip()
        return json.loads(text)
    except Exception:
        return fallback_plan(goal_text, days)
