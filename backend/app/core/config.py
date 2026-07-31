from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Restaurant Floor Monitoring"
    DATABASE_URL: str
    SYNC_DATABASE_URL: str

    class Config:
        env_file = Path(__file__).parent.parent.parent.parent / ".env"

settings = Settings()
