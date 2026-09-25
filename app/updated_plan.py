import time
from google import genai
from google.genai import types
from .config import settings
from .schemas import WorkoutPlan

def update_workout_plan(original_plan: str, feedback: str) -> WorkoutPlan:
    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured.")

    prompt = f"""
You are FitBuddy. Revise the existing 7-day workout plan according to the user's feedback.

Existing plan:
{original_plan}

User feedback:
{feedback}

Rules:
- Preserve the user's original goal and general safety.
- Apply the feedback where reasonable.
- Keep exactly 7 days.
- Keep warm-up, exercises, cooldown, and recovery guidance.
- Do not introduce unsafe or extreme training.
- If the feedback requests something medically risky, use a safer alternative.
- Return only structured JSON matching the supplied schema.
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
                        temperature=0.55,
                        max_output_tokens=7000,
                    ),
                )
            if response.text:
                return WorkoutPlan.model_validate_json(response.text)
        except Exception as exc:
            last_exc = exc
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))

    raise last_exc or RuntimeError("Gemini returned an empty updated plan.")
