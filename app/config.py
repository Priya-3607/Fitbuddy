from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    google_api_key: str = ""
    gemini_workout_model: str = "gemini-3.6-flash"
    gemini_tip_model: str = "gemini-3.6-flash"
    database_url: str = f"sqlite:///{(BASE_DIR / 'fitbuddy.db').as_posix()}"
    admin_password: str = "change-me"
    session_secret: str = "change-this-session-secret"
    demo_mode: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()
