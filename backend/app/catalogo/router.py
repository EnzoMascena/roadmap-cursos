"""Endpoints del catálogo (BackendSchema §3.2). Reciben HTTP, validan y delegan al service."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.catalogo import service
from app.catalogo.repository import CursoRepositoryEnMemoria, get_repositorio
from app.catalogo.schemas import CursoResumen
from app.compartido.paginacion import PAGE_SIZE_DEFAULT, PAGE_SIZE_MAX, Page

router = APIRouter(tags=["catálogo"])


@router.get("/cursos", response_model=Page[CursoResumen], summary="Listar cursos publicados")
def listar_cursos(
    repositorio: Annotated[CursoRepositoryEnMemoria, Depends(get_repositorio)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=PAGE_SIZE_MAX)] = PAGE_SIZE_DEFAULT,
    categoria_id: Annotated[int | None, Query()] = None,
    q: Annotated[str | None, Query(min_length=2, max_length=100)] = None,
) -> Page[CursoResumen]:
    return service.listar_catalogo(
        repositorio, page=page, page_size=page_size, categoria_id=categoria_id, q=q
    )
