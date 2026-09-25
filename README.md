# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite web application that uses Google's Gemini API to generate personalized 7-day workout plans, nutrition/recovery tips, and feedback-based plan updates.

## Architecture

- **Frontend:** HTML + Jinja2 + CSS
- **Backend:** FastAPI + Uvicorn
- **AI:** Google Gen AI Python SDK
- **Workout/update model:** `gemini-3.6-flash` by default
- **Nutrition tip model:** `gemini-3.6-flash` by default
- **Database:** SQLite + SQLAlchemy
- **Validation:** Pydantic
- **Admin:** Session-protected dashboard
- **API:** FastAPI JSON endpoints under `/api`

The model names are environment variables, so they can be changed without editing Python.

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   ├── demo_data.py
│   ├── utils.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── result.html
│   │   ├── feedback.html
│   │   ├── admin_login.html
│   │   └── all_users.html
│   └── static/
│       └── style.css
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## VS Code setup – Windows

### 1. Open the project

Extract/open the `FitBuddy` folder in VS Code.

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate it

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks scripts, use Command Prompt:

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Gemini

Copy:

```text
.env.example
```

to:

```text
.env
```

Open `.env` and add your Gemini API key:

```env
GOOGLE_API_KEY=your_real_key_here
```

The Gemini API key should be created in Google AI Studio. Never commit `.env` to Git.

### 6. Run

```powershell
uvicorn app.main:app --reload
```

Open:

- App: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health
- Admin login: http://127.0.0.1:8000/admin/login

## First test

1. Open the home page.
2. Enter:
   - Name: Kabila
   - User ID: FB001
   - Age: 21
   - Weight: 65
   - Goal: Muscle gain
   - Intensity: Medium
   - Experience: Beginner
   - Schedule: 5 days/week
3. Click **Generate My 7-Day Plan**.
4. Confirm 7 day cards and a nutrition/recovery tip appear.
5. Open **Feedback**.
6. Use `FB001`.
7. Enter feedback such as:
   `Add more cardio and keep two recovery days.`
8. Confirm the revised plan appears.
9. Open **Admin**, sign in with the `ADMIN_PASSWORD` from `.env`, and confirm the user, original plan, updated plan and feedback are visible.

## Test without a Gemini API key

For UI/database testing only, set:

```env
DEMO_MODE=true
```

Then restart Uvicorn. Demo mode generates deterministic sample plans locally. Set it back to `false` when testing the real Gemini integration.

## API examples

### Generate

POST `/api/generate`

```json
{
  "username": "Kabila",
  "user_id": "FB001",
  "age": 21,
  "weight": 65,
  "goal": "muscle gain",
  "intensity": "medium",
  "experience_level": "beginner",
  "workout_schedule": "5 days/week"
}
```

### Feedback

POST `/api/feedback`

```json
{
  "user_id": "FB001",
  "feedback": "Add more cardio and keep two recovery days."
}
```

### Health

GET `/health`

```json
{"status":"ok","service":"fitbuddy"}
```

## Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `GOOGLE_API_KEY` | Gemini API key | empty |
| `GEMINI_WORKOUT_MODEL` | Workout/update model | `gemini-2.5-pro` |
| `GEMINI_TIP_MODEL` | Nutrition/recovery model | `gemini-2.5-flash` |
| `DATABASE_URL` | SQLAlchemy DB URL | local SQLite |
| `ADMIN_PASSWORD` | Admin dashboard password | `change-me` |
| `SESSION_SECRET` | Session signing secret | `change-this-session-secret` |
| `DEMO_MODE` | Disable real Gemini calls for local UI tests | `false` |

## Notes

- SQLite database `fitbuddy.db` is created automatically on first startup.
- Original plans are preserved when feedback updates are generated.
- The latest updated plan is stored separately from the original.
- The application does not provide medical diagnosis or treatment.
- For production deployment, use HTTPS, a strong session secret/password, a production database, and a managed secret store.

## Troubleshooting

### `GOOGLE_API_KEY is not configured`
Check `.env`, make sure the key is on one line, and restart Uvicorn.

### Gemini model access error
The default models are configurable. If your Google account/API project does not have access to the configured model, change `GEMINI_WORKOUT_MODEL` and/or `GEMINI_TIP_MODEL` to an available Gemini model.

### PowerShell activation error
Use Command Prompt or run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

then activate the environment again.

### Database reset
Stop the server and delete `fitbuddy.db`. Start the server again and the schema will be recreated.
