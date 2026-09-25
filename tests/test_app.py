import os
os.environ["DEMO_MODE"] = "true"
os.environ["ADMIN_PASSWORD"] = "test-password"
os.environ["SESSION_SECRET"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text

def test_generate_workout_page():
    response = client.post("/generate-workout", data={
        "username": "Test User",
        "user_id": "TEST001",
        "age": 25,
        "weight": 70,
        "goal": "general wellness",
        "intensity": "medium",
        "experience_level": "beginner",
        "workout_schedule": "5 days/week",
    })
    assert response.status_code == 200
    assert "7-Day" in response.text
    assert "TEST001" in response.text
    assert "Test User" in response.text

def test_feedback_page_get():
    response = client.get("/feedback?user_id=TEST001")
    assert response.status_code == 200
    assert "Refine your workout plan" in response.text
    assert "TEST001" in response.text

def test_submit_feedback_not_found():
    response = client.post("/submit-feedback", data={
        "user_id": "NONEXISTENT",
        "feedback": "Add more cardio",
    })
    assert response.status_code == 404
    assert "User ID not found" in response.text

def test_submit_feedback_success():
    # Ensure user exists first
    client.post("/generate-workout", data={
        "username": "Test User",
        "user_id": "TEST001",
        "age": 25,
        "weight": 70,
        "goal": "general wellness",
        "intensity": "medium",
        "experience_level": "beginner",
        "workout_schedule": "5 days/week",
    })
    response = client.post("/submit-feedback", data={
        "user_id": "TEST001",
        "feedback": "Add more cardio",
    })
    assert response.status_code == 200
    assert "Your plan was updated using your feedback" in response.text

def test_admin_login_wrong_password():
    response = client.post("/admin/login", data={"password": "wrong-password"})
    assert response.status_code == 401
    assert "Invalid admin password" in response.text

def test_admin_flow_and_view_users():
    # Unauthenticated redirect
    unauth_resp = client.get("/view-all-users", follow_redirects=False)
    assert unauth_resp.status_code == 303
    assert unauth_resp.headers["location"] == "/admin/login"

    # Admin Login
    login_resp = client.post("/admin/login", data={"password": "test-password"}, follow_redirects=False)
    assert login_resp.status_code == 303
    assert login_resp.headers["location"] == "/view-all-users"

    # View users with admin session
    view_resp = client.get("/view-all-users")
    assert view_resp.status_code == 200
    assert "Users &amp; Plans" in view_resp.text or "Users & Plans" in view_resp.text

    # API users list
    api_users_resp = client.get("/api/users")
    assert api_users_resp.status_code == 200
    assert "users" in api_users_resp.json()

    # Logout
    logout_resp = client.post("/admin/logout", follow_redirects=False)
    assert logout_resp.status_code == 303
    assert logout_resp.headers["location"] == "/"

def test_delete_user():
    # Generate user
    client.post("/generate-workout", data={
        "username": "User to Delete",
        "user_id": "DEL001",
        "age": 30,
        "weight": 80,
        "goal": "strength",
        "intensity": "high",
        "experience_level": "intermediate",
        "workout_schedule": "6 days/week",
    })

    # Login admin
    client.post("/admin/login", data={"password": "test-password"})

    # Delete user
    del_resp = client.post("/admin/users/DEL001/delete", follow_redirects=False)
    assert del_resp.status_code == 303
    assert del_resp.headers["location"] == "/view-all-users"

def test_api_generate_and_feedback():
    gen_resp = client.post("/api/generate", json={
        "username": "API User",
        "user_id": "API001",
        "age": 28,
        "weight": 75,
        "goal": "muscle gain",
        "intensity": "high",
        "experience_level": "intermediate",
        "workout_schedule": "5 days/week",
    })
    assert gen_resp.status_code == 200
    data = gen_resp.json()
    assert data["user_id"] == "API001"
    assert len(data["workout_plan"]["days"]) == 7

    fb_resp = client.post("/api/feedback", json={
        "user_id": "API001",
        "feedback": "More focus on arms",
    })
    assert fb_resp.status_code == 200
    fb_data = fb_resp.json()
    assert fb_data["user_id"] == "API001"
