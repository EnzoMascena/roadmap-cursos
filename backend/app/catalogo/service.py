"""Reglas de negocio del catálogo. Sin HTTP ni SQL: recibe el repositorio y datos."""

from app.catalogo.repository import CATEGORIAS, CursoRepositoryEnMemoria
from app.catalogo.schemas import CategoriaRef, CursoResumen
from app.compartido.errores import ErrorDeDominio
from app.compartido.paginacion import Page, armar_pagina, calcular_offset


def listar_catalogo(
    repositorio: CursoRepositoryEnMemoria,
    *,
    page: int,
    page_size: int,
    categoria_id: int | None = None,
    q: str | None = None,
) -> Page[CursoResumen]:
    """Catálogo comunitario: solo cursos publicados (BR-001), del más reciente al más antiguo."""
    if categoria_id is not None and categoria_id not in CATEGORIAS:
        raise ErrorDeDominio(
            "VALIDACION",
            "Hay datos inválidos.",
            status=422,
            details=[{"campo": "categoria_id", "mensaje": "La categoría no existe."}],
        )
    filas, total = repositorio.listar_publicados(
        categoria_id=categoria_id,
        q=q,
        offset=calcular_offset(page, page_size),
        limit=page_size,
    )
    return armar_pagina([_a_resumen(fila) for fila in filas], total, page, page_size)


def _a_resumen(fila: dict) -> CursoResumen:
    return CursoResumen(
        id=fila["id"],
        titulo=fila["titulo"],
        plataforma=fila["plataforma"],
        categoria=CategoriaRef(id=fila["categoria_id"], nombre=CATEGORIAS[fila["categoria_id"]]),
        anio_edicion=fila["anio_edicion"],
        docentes=fila["docentes"],
        tiene_cuestionarios=fila["tiene_cuestionarios"],
        requiere_examen=fila["requiere_examen"],
        extiende_certificado=fila["extiende_certificado"],
        avalado_por_organizacion=fila["avalado_por_organizacion"],
    )
