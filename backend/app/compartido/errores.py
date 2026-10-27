"""Errores de la API con un único formato (TRD TD-008).

Toda respuesta de error tiene la forma:
    {"error": {"code": "...", "message": "...", "details": ...}}
"""

import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("senda")

CODIGOS_POR_STATUS = {
    400: "SOLICITUD_INVALIDA",
    401: "NO_AUTENTICADO",
    403: "PROHIBIDO",
    404: "NO_ENCONTRADO",
    405: "METODO_NO_PERMITIDO",
    429: "DEMASIADOS_INTENTOS",
}

MENSAJES_POR_STATUS = {
    404: "No encontramos lo que buscás.",
    405: "Método no permitido para esta ruta.",
}


class ErrorDeDominio(Exception):
    """Error de una regla de negocio. Lo lanzan los services y lo traduce el handler."""

    def __init__(self, code: str, message: str, status: int = 400, details=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.details = details


def respuesta_error(status: int, code: str, message: str, details=None, headers=None) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"error": {"code": code, "message": message, "details": details}},
        headers=headers,
    )


def registrar_handlers(app: FastAPI) -> None:
    @app.exception_handler(ErrorDeDominio)
    async def error_de_dominio(_: Request, exc: ErrorDeDominio) -> JSONResponse:
        return respuesta_error(exc.status, exc.code, exc.message, exc.details)

    @app.exception_handler(StarletteHTTPException)
    async def error_http(_: Request, exc: StarletteHTTPException) -> JSONResponse:
        frase_estandar = HTTPStatus(exc.status_code).phrase
        if isinstance(exc.detail, str) and exc.detail != frase_estandar:
            mensaje = exc.detail
        else:
            mensaje = MENSAJES_POR_STATUS.get(exc.status_code, "No se pudo procesar la solicitud.")
        return respuesta_error(
            exc.status_code,
            CODIGOS_POR_STATUS.get(exc.status_code, "ERROR_HTTP"),
            mensaje,
            headers=getattr(exc, "headers", None),
        )

    @app.exception_handler(RequestValidationError)
    async def error_de_validacion(_: Request, exc: RequestValidationError) -> JSONResponse:
        detalles = [
            {
                "campo": ".".join(str(parte) for parte in error["loc"] if parte not in ("body", "query", "path")),
                "mensaje": error["msg"],
            }
            for error in exc.errors()
        ]
        return respuesta_error(422, "VALIDACION", "Hay datos inválidos.", detalles)

    @app.exception_handler(Exception)
    async def error_inesperado(request: Request, _: Exception) -> JSONResponse:
        logger.exception("Error no controlado en %s %s", request.method, request.url.path)
        return respuesta_error(500, "ERROR_INTERNO", "Ocurrió un error inesperado.")
