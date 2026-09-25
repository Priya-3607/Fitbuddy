from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

Goal = Literal["weight loss", "muscle gain", "general wellness", "flexibility", "strength"]
Intensity = Literal["low", "medium", "high"]
Experience = Literal["beginner", "intermediate", "advanced"]

class Exercise(BaseModel):
    name: str
    sets: str
    reps_or_duration: str
    rest: str
    notes: str = ""

class WorkoutDay(BaseModel):
    day: str
    focus: str
    warm_up: str
    exercises: list[Exercise]
    cool_down: str
    recovery_tip: str = ""

class WorkoutPlan(BaseModel):
    title: str
    summary: str
    safety_note: str
    days: list[WorkoutDay] = Field(min_length=7, max_length=7)

class UserInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str = Field(min_length=2, max_length=120)
    user_id: str = Field(min_length=2, max_length=80)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, lt=400)
    goal: Goal
    intensity: Intensity
    experience_level: Experience = "beginner"
    workout_schedule: str = Field(default="5 days/week", max_length=80)

class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=2, max_length=80)
    feedback: str = Field(min_length=3, max_length=1000)

class GenerateResponse(BaseModel):
    user_id: str
    workout_plan: WorkoutPlan
    nutrition_tip: str
