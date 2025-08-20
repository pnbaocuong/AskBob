import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Settings:
    app_name: str = os.getenv("APP_NAME", "AskBobAI")
    environment: str = os.getenv("APP_ENV", "development")

    secret_key: str = os.getenv("SECRET_KEY", "change_this_in_real_env")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    database_url_async: str = os.getenv("DATABASE_URL", "")
    database_url_sync: str = os.getenv("SYNC_DATABASE_URL", "")


@lru_cache
def get_settings() -> Settings:
    return Settings()
