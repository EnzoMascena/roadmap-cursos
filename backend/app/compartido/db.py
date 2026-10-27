"""Conexión a PostgreSQL con SQLAlchemy (TRD TD-009).

El engine no abre ninguna conexión hasta que se usa: la API arranca aunque la base
todavía no esté lista. Las tablas y migraciones llegan con Alembic (tarea 0.4).
"""

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings

logger = logging.getLogger("senda")

engine = create_engine(
    get_settings().database_url,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 3},
)


def base_disponible() -> bool:
    """Hace un SELECT 1 para saber si la base responde."""
    try:
        with engine.connect() as conexion:
            conexion.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as error:
        logger.warning("La base de datos no responde: %s", error.__class__.__name__)
        return False
