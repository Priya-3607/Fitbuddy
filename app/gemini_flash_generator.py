import time
from google import genai
from google.genai import types
from .config import settings
from .schemas import UserInput

def generate_nutrition_tip_with_flash(user: UserInput) -> str:
    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured.")

    prompt = f"""
You are FitBuddy's concise nutrition and recovery assistant.

User profile:
- Goal: {user.goal}
- Age: {user.age}
- Weight: {user.weight} kg
- Intensity: {user.intensity}
- Experience: {user.experience_level}

Give one practical, evidence-aligned nutrition or recovery tip in 2-4 sentences.
Do not prescribe supplements or medical treatment. Avoid exact calorie prescriptions.
Mention hydration, balanced meals, protein/fiber, sleep, or recovery when relevant.
Do not promise a specific amount of weight or muscle gain.
"""
    last_exc = None
    for attempt in range(3):
        try:
            with genai.Client(api_key=settings.google_api_key) as client:
                response = client.models.generate_content(
                    model=settings.gemini_tip_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.4,
                        max_output_tokens=300,
                    ),
                )
            text = (response.text or "").strip()
            if text:
                return text
        except Exception as exc:
            last_exc = exc
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))

    raise last_exc or RuntimeError("Gemini returned an empty nutrition tip.")
