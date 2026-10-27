"""Paginación offset para todos los listados (TRD TD-002).

Respuesta: {"items": [...], "total": N, "page": n, "page_size": n, "pages": n}
"""

from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

PAGE_SIZE_DEFAULT = 12
PAGE_SIZE_MAX = 100


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


def calcular_offset(page: int, page_size: int) -> int:
    return (page - 1) * page_size


def armar_pagina(items: list[T], total: int, page: int, page_size: int) -> Page[T]:
    return Page[T](
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=ceil(total / page_size) if total else 0,
    )
