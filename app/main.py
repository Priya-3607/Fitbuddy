from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path

from .routes import router
from .database import init_db
from .config import settings

BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="AI-powered 7-day workout planning and feedback application using Gemini.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    max_age=60 * 60 * 8,
    same_site="lax",
    https_only=False,  # Set True when deployed behind HTTPS.
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(router)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
