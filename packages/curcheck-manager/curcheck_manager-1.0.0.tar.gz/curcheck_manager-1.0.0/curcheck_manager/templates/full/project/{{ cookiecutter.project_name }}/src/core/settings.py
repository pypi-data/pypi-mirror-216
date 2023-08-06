""" Сборка переменных окружения из dotenv """

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "sqlite://sqlite3.db"

    class Config:
        case_sensitive = True
        env_file = "~/env.env"


settings = Settings()
