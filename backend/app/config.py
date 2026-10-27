"""Configuración de la API, leída de variables de entorno (TRD §4.4)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # En Docker Compose el host es "postgres"; corriendo local, localhost.
    database_url: str = "postgresql+psycopg://senda:senda@localhost:5432/senda"
    # Carga los cursos de ejemplo. Con SEED_DEMO=false el catálogo arranca vacío.
    seed_demo: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
