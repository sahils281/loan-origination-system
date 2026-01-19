from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "Loan Origination System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    PROCESSOR_THREAD_POOL_SIZE: int = 5
    PROCESSING_DELAY_MIN: int = 2
    PROCESSING_DELAY_MAX: int = 5

    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
