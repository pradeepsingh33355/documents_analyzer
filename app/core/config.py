from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL_NAME: str
    LANGUAGETOOL_URL: str | None = None
    STORAGE_PATH: str = str(Path.cwd() / "storage")
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50 MB
    VERSION: str
    API_V1_STR: str

    ACCESS_TOKEN_EXPIRE_DAYS: int
    JWT_ALGORITHM: str

    ADMIN_EMAIL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SECRET_KEY: str

    UPLOAD_DIR: str


class Config:
    env_file = ".env"


settings = Settings()
