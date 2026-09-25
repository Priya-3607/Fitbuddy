import time
from google import genai
from google.genai import types
from .config import settings
from .schemas import UserInput, WorkoutPlan

def _profile_text(user: UserInput) -> str:
    return (
        f"Name: {user.username}\n"
        f"Age: {user.age}\n"
        f"Weight: {user.weight} kg\n"
        f"Goal: {user.goal}\n"
        f"Intensity: {user.intensity}\n"
        f"Experience: {user.experience_level}\n"
        f"Preferred schedule: {user.workout_schedule}"
    )

def generate_workout_gemini(user: UserInput) -> WorkoutPlan:
    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured.")

    prompt = f"""
You are FitBuddy, a careful fitness-planning assistant.

Create a practical personalized 7-day workout plan for this profile:
{_profile_text(user)}

Requirements:
- Return exactly 7 days (Day 1 through Day 7).
- STRICT SCHEDULE MATCH: If the preferred schedule is "3 days/week", generate EXACTLY 3 active workout days and 4 rest/active-recovery days. If "4 days/week", generate 4 workout days and 3 rest/recovery days. If "5 days/week", generate 5 workout days and 2 rest/recovery days.
- STRICT GOAL ALIGNMENT: Choose exercises, sets, reps, and training focus strictly tailored to the specific goal ("{user.goal}"). For example, "muscle gain" must emphasize progressive hypertrophy resistance training; "weight loss" must emphasize calorie-burning circuits and cardio intervals; "flexibility" must emphasize mobility flows and stretches; "strength" must emphasize compound movements with lower reps and longer rest.
- VARIETY: Ensure training days feature distinct, non-repetitive exercise routines appropriate for each day's focus (e.g. Upper Body vs Lower Body vs Full Body). Do NOT repeat identical exercise lists across different training days.
- Include warm-up, exercises with sets/reps or duration/rest, cooldown, and a recovery tip for each day.
- Avoid unsafe extreme volume, dangerous exercises, or guaranteed medical/weight-loss claims.
- The output must be structured JSON matching the supplied schema.
- Include a concise safety note telling the user to stop if they experience pain, dizziness, chest pain, unusual shortness of breath, or concerning symptoms.
"""
    last_exc = None
    for attempt in range(3):
        try:
            with genai.Client(api_key=settings.google_api_key) as client:
                response = client.models.generate_content(
                    model=settings.gemini_workout_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=WorkoutPlan,
                        temperature=0.65,
                        max_output_tokens=7000,
                    ),
                )
            if response.text:
                return WorkoutPlan.model_validate_json(response.text)
        except Exception as exc:
            last_exc = exc
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))

    raise last_exc or RuntimeError("Gemini returned an empty workout plan.")
