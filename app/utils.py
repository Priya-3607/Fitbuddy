import json
from .schemas import WorkoutPlan

def plan_to_json(plan: WorkoutPlan) -> str:
    return json.dumps(plan.model_dump(), ensure_ascii=False, indent=2)

def plan_from_json(value: str) -> WorkoutPlan:
    return WorkoutPlan.model_validate_json(value)
