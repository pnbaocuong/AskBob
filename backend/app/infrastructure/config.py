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

    # Performance tuning
    db_pool_size: int = int(os.getenv("DB_POOL_SIZE", "10"))
    db_max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    db_pool_timeout: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    db_pool_recycle: int = int(os.getenv("DB_POOL_RECYCLE", "1800"))

    # CORS
    allowed_origins: list[str] = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()]

    # Pagination
    default_page_size: int = int(os.getenv("DEFAULT_PAGE_SIZE", "20"))
    max_page_size: int = int(os.getenv("MAX_PAGE_SIZE", "100"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
