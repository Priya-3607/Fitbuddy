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
- Return exactly 7 days.
- Adapt exercise selection, volume, and intensity to the goal, intensity, experience,
  age, weight, and preferred schedule.
- Include warm-up, exercises with sets/reps or duration/rest, cooldown, and a recovery tip.
- If the preferred schedule has fewer than 7 training days, use appropriate active-recovery
  or rest days rather than forcing hard training every day.
- Avoid unsafe extreme volume, dangerous exercises, or guaranteed medical/weight-loss claims.
- The output must be structured JSON matching the supplied schema.
- Include a concise safety note telling the user to stop if they experience pain, dizziness,
  chest pain, unusual shortness of breath, or other concerning symptoms and to seek qualified
  medical/fitness advice when appropriate.
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
