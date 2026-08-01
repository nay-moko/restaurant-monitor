from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Restaurant Floor Monitoring"
    DATABASE_URL: str
    SYNC_DATABASE_URL: str

    # "127.0.0.1" rather than "localhost": on this Windows/Memurai setup,
    # redis.asyncio's DNS resolution of "localhost" returns the IPv6 "::1"
    # candidate first, and Memurai only listens on IPv4 -- connect() then
    # hangs until timeout before ever trying the v4 address. Using the
    # literal loopback IP sidesteps the resolution order entirely.
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    class Config:
        env_file = Path(__file__).parent.parent.parent.parent / ".env"

settings = Settings()
