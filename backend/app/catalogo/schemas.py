"""Schemas de respuesta del catálogo (BackendSchema §3, objeto CursoResumen)."""

from pydantic import BaseModel


class CategoriaRef(BaseModel):
    id: int
    nombre: str


class CursoResumen(BaseModel):
    id: int
    titulo: str
    plataforma: str
    categoria: CategoriaRef
    anio_edicion: int
    docentes: str
    tiene_cuestionarios: bool
    requiere_examen: bool
    extiende_certificado: bool
    avalado_por_organizacion: bool
    # null cuando la request no trae token; se completa con el roadmap (M4).
    en_mi_roadmap: bool | None = None
