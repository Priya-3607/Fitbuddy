import secrets
from pathlib import Path
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db, User, Plan
from .schemas import UserInput, FeedbackRequest, GenerateResponse
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan
from .demo_data import demo_workout_plan
from .utils import plan_to_json, plan_from_json

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

def ai_generate(user: UserInput):
    if settings.demo_mode or not settings.google_api_key:
        return demo_workout_plan(user.goal, user.intensity, user.workout_schedule, user.experience_level), (
            "Demo tip: build balanced meals around protein, vegetables/fruit, whole grains "
            "and adequate hydration. Prioritize recovery and sleep."
        )
    try:
        return generate_workout_gemini(user), generate_nutrition_tip_with_flash(user)
    except Exception as exc:
        err_str = str(exc)
        if any(k in err_str for k in ["503", "UNAVAILABLE", "429", "404"]):
            return demo_workout_plan(user.goal, user.intensity, user.workout_schedule, user.experience_level), (
                "Nutrition tip: build balanced meals around protein, vegetables/fruit, whole grains "
                "and adequate hydration. Prioritize recovery and sleep. (Generated via resilient fallback)."
            )
        raise exc

def require_admin(request: Request):
    if not request.session.get("admin"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin login required.")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    experience_level: str = Form("beginner"),
    workout_schedule: str = Form("5 days/week"),
    db: Session = Depends(get_db),
):
    try:
        user_input = UserInput(
            username=username, user_id=user_id, age=age, weight=weight,
            goal=goal, intensity=intensity, experience_level=experience_level,
            workout_schedule=workout_schedule,
        )
        workout, tip = ai_generate(user_input)
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)},
            status_code=500,
        )

    user = db.query(User).filter(User.user_id == user_input.user_id).first()
    if user is None:
        user = User(
            user_id=user_input.user_id,
            username=user_input.username,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
            experience_level=user_input.experience_level,
            workout_schedule=user_input.workout_schedule,
        )
        db.add(user)
        db.flush()
    else:
        user.username = user_input.username
        user.age = user_input.age
        user.weight = user_input.weight
        user.goal = user_input.goal
        user.intensity = user_input.intensity
        user.experience_level = user_input.experience_level
        user.workout_schedule = user_input.workout_schedule

    plan = Plan(
        user_id=user.id,
        original_plan=plan_to_json(workout),
        nutrition_tip=tip,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "plan": plan_from_json(plan.original_plan),
            "nutrition_tip": plan.nutrition_tip,
            "db_plan": plan,
            "updated": False,
        },
    )

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or not user.plans:
        return templates.TemplateResponse(
            request=request,
            name="feedback.html",
            context={"error": "User ID not found. Generate a plan first.", "user_id": user_id},
            status_code=404,
        )

    plan = user.plans[-1]
    source_json = plan.updated_plan or plan.original_plan

    try:
        if settings.demo_mode or not settings.google_api_key:
            updated = demo_workout_plan(user.goal, user.intensity, user.workout_schedule, user.experience_level)
        else:
            try:
                updated = update_workout_plan(source_json, feedback)
            except Exception as exc:
                err_str = str(exc)
                if any(k in err_str for k in ["503", "UNAVAILABLE", "429", "404"]):
                    updated = demo_workout_plan(user.goal, user.intensity, user.workout_schedule, user.experience_level)
                else:
                    raise exc
        plan.updated_plan = plan_to_json(updated)
        plan.feedback = feedback
        db.commit()
        db.refresh(plan)
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="feedback.html",
            context={"error": str(exc), "user_id": user_id},
            status_code=500,
        )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "plan": updated,
            "nutrition_tip": plan.nutrition_tip,
            "db_plan": plan,
            "updated": True,
        },
    )

@router.get("/feedback", response_class=HTMLResponse)
def feedback_page(request: Request, user_id: str | None = None):
    return templates.TemplateResponse(
        request=request,
        name="feedback.html",
        context={"user_id": user_id},
    )

@router.get("/admin/login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
    )

@router.post("/admin/login")
def admin_login(request: Request, password: str = Form(...)):
    if not secrets.compare_digest(password, settings.admin_password):
        return templates.TemplateResponse(
            request=request,
            name="admin_login.html",
            context={"error": "Invalid admin password."},
            status_code=401,
        )
    request.session["admin"] = True
    return RedirectResponse("/view-all-users", status_code=303)

@router.post("/admin/logout")
def admin_logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login", status_code=303)
    users = db.query(User).order_by(User.created_at.desc()).all()
    for u in users:
        for p in u.plans:
            try:
                p.parsed_original = plan_from_json(p.original_plan)
            except Exception:
                p.parsed_original = None
            if p.updated_plan:
                try:
                    p.parsed_updated = plan_from_json(p.updated_plan)
                except Exception:
                    p.parsed_updated = None
            else:
                p.parsed_updated = None

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": users},
    )

@router.post("/admin/users/{user_id}/delete")
def delete_user(user_id: str, request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return RedirectResponse("/view-all-users", status_code=303)

@router.get("/health")
def health():
    return {"status": "ok", "service": "fitbuddy"}

@router.post("/api/generate", response_model=GenerateResponse)
def api_generate(payload: UserInput, db: Session = Depends(get_db)):
    try:
        workout, tip = ai_generate(payload)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    user = db.query(User).filter(User.user_id == payload.user_id).first()
    if user is None:
        user = User(
            user_id=payload.user_id, username=payload.username, age=payload.age,
            weight=payload.weight, goal=payload.goal, intensity=payload.intensity,
            experience_level=payload.experience_level, workout_schedule=payload.workout_schedule,
        )
        db.add(user)
        db.flush()
    else:
        user.username, user.age, user.weight = payload.username, payload.age, payload.weight
        user.goal, user.intensity = payload.goal, payload.intensity
        user.experience_level, user.workout_schedule = payload.experience_level, payload.workout_schedule

    db.add(Plan(user_id=user.id, original_plan=plan_to_json(workout), nutrition_tip=tip))
    db.commit()
    return GenerateResponse(user_id=payload.user_id, workout_plan=workout, nutrition_tip=tip)

@router.post("/api/feedback", response_model=GenerateResponse)
def api_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == payload.user_id).first()
    if not user or not user.plans:
        raise HTTPException(status_code=404, detail="User or plan not found.")

    plan = user.plans[-1]
    source_json = plan.updated_plan or plan.original_plan
    try:
        if settings.demo_mode or not settings.google_api_key:
            updated = demo_workout_plan(user.goal, user.intensity, user.workout_schedule, user.experience_level)
        else:
            updated = update_workout_plan(source_json, payload.feedback)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    plan.updated_plan = plan_to_json(updated)
    plan.feedback = payload.feedback
    db.commit()
    return GenerateResponse(
        user_id=user.user_id,
        workout_plan=updated,
        nutrition_tip=plan.nutrition_tip,
    )

@router.get("/api/users")
def api_users(request: Request, db: Session = Depends(get_db)):
    require_admin(request)
    users = db.query(User).order_by(User.created_at.desc()).all()
    return JSONResponse({
        "users": [
            {
                "user_id": u.user_id,
                "username": u.username,
                "age": u.age,
                "weight": u.weight,
                "goal": u.goal,
                "intensity": u.intensity,
                "plans": len(u.plans),
            }
            for u in users
        ]
    })
