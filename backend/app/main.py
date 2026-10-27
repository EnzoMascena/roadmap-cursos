"""Punto de entrada de la API de Senda: crea la app, registra handlers y monta routers."""

import logging

from fastapi import FastAPI

from app.catalogo.router import router as catalogo_router
from app.compartido.db import base_disponible
from app.compartido.errores import registrar_handlers, respuesta_error

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Senda API",
    version="0.1.0",
    description="Catálogo comunitario de cursos gratuitos y roadmaps personales.",
)
registrar_handlers(app)


@app.get("/health", tags=["salud"], summary="La API está viva")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/health", tags=["salud"], summary="La API y la base de datos responden")
def health_con_base():
    if not base_disponible():
        return respuesta_error(503, "BD_NO_DISPONIBLE", "No hay conexión con la base de datos.")
    return {"status": "ok", "db": "ok"}


app.include_router(catalogo_router, prefix="/api/v1")
