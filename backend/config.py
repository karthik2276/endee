"""
backend/config.py
-----------------
All settings loaded from .env via pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    endee_db_path: str = "./data/complaints.jsonl"
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "google/flan-t5-base"
    llm_max_new_tokens: int = 256
    search_top_k: int = 5
    cors_origin: str = "http://localhost:5173"


settings = Settings()
