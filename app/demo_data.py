from .schemas import WorkoutPlan, WorkoutDay, Exercise

def demo_workout_plan(goal: str, intensity: str) -> WorkoutPlan:
    base = {
        "title": f"FitBuddy 7-Day {goal.title()} Plan",
        "summary": f"A {intensity}-intensity starter plan with training, recovery and mobility.",
        "safety_note": "This demo plan is for general wellness. Stop if you feel pain, dizziness, chest pain or unusual shortness of breath.",
        "days": []
    }
    focuses = [
        ("Day 1", "Full Body Strength"),
        ("Day 2", "Cardio + Mobility"),
        ("Day 3", "Lower Body"),
        ("Day 4", "Active Recovery"),
        ("Day 5", "Upper Body"),
        ("Day 6", "Core + Cardio"),
        ("Day 7", "Rest + Mobility"),
    ]
    for day, focus in focuses:
        if "Rest" in focus or "Recovery" in focus:
            exercises = [Exercise(name="Easy walk", sets="1", reps_or_duration="20–30 min", rest="As needed", notes="Keep the pace comfortable.")]
        else:
            exercises = [
                Exercise(name="Bodyweight squat", sets="3", reps_or_duration="8–12", rest="60–90 sec"),
                Exercise(name="Incline push-up", sets="3", reps_or_duration="8–12", rest="60–90 sec"),
                Exercise(name="Glute bridge", sets="3", reps_or_duration="10–15", rest="60 sec"),
            ]
        base["days"].append(WorkoutDay(
            day=day, focus=focus, warm_up="5–10 min easy movement and dynamic mobility.",
            exercises=exercises,
            cool_down="5–10 min gentle stretching and breathing.",
            recovery_tip="Hydrate and prioritize sleep."
        ))
    return WorkoutPlan.model_validate(base)
