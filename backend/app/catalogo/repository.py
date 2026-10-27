"""Acceso a datos del catálogo.

v0.1.0 (scaffold): repositorio EN MEMORIA con cursos de ejemplo. En M2 (tareas 2.1 a 2.4)
se reemplaza por uno sobre PostgreSQL con la misma interfaz, así el service y el router
no cambian.
"""

from functools import lru_cache

from app.config import get_settings

# Lista cerrada de categorías (BackendSchema §1.2). En M2 vive en la tabla `categorias`.
CATEGORIAS: dict[int, str] = {
    1: "Programación",
    2: "Bases de datos",
    3: "Desarrollo web",
    4: "Ciencia de datos e IA",
    5: "Redes e infraestructura",
    6: "Ciberseguridad",
    7: "Diseño UX/UI",
    8: "Matemática y estadística",
    9: "Idiomas",
    10: "Gestión y negocios",
}

# Datos de ejemplo: cursos y docentes ficticios, solo para probar el scaffold.
CURSOS_DEMO: list[dict] = [
    {
        "id": 1, "titulo": "Introducción a SQL", "plataforma": "Coursera", "categoria_id": 2,
        "tema": "Consultas SELECT, JOIN y agregaciones", "anio_edicion": 2025,
        "docentes": "Ana Pérez, Juan Gómez", "tiene_cuestionarios": True, "requiere_examen": False,
        "extiende_certificado": True, "avalado_por_organizacion": True,
        "estado": "publicado", "validado_en": "2026-10-20T14:00:00Z",
    },
    {
        "id": 2, "titulo": "Python desde cero", "plataforma": "YouTube", "categoria_id": 1,
        "tema": "Variables, funciones y estructuras de datos", "anio_edicion": 2024,
        "docentes": "Carla Ruiz", "tiene_cuestionarios": False, "requiere_examen": False,
        "extiende_certificado": False, "avalado_por_organizacion": False,
        "estado": "publicado", "validado_en": "2026-10-21T10:30:00Z",
    },
    {
        "id": 3, "titulo": "HTML y CSS para principiantes", "plataforma": "freeCodeCamp", "categoria_id": 3,
        "tema": "Maquetado responsive mobile-first", "anio_edicion": 2025,
        "docentes": "Lucas Fernández", "tiene_cuestionarios": True, "requiere_examen": True,
        "extiende_certificado": True, "avalado_por_organizacion": False,
        "estado": "publicado", "validado_en": "2026-10-22T09:15:00Z",
    },
    {
        "id": 4, "titulo": "Fundamentos de redes", "plataforma": "edX", "categoria_id": 5,
        "tema": "Modelo OSI, TCP/IP y direccionamiento", "anio_edicion": 2024,
        "docentes": "Marina Sosa", "tiene_cuestionarios": True, "requiere_examen": True,
        "extiende_certificado": True, "avalado_por_organizacion": True,
        "estado": "publicado", "validado_en": "2026-10-23T16:45:00Z",
    },
    {
        "id": 5, "titulo": "Introducción a la ciberseguridad", "plataforma": "edX", "categoria_id": 6,
        "tema": "Amenazas comunes y buenas prácticas", "anio_edicion": 2025,
        "docentes": "Diego Martínez, Sofía López", "tiene_cuestionarios": True, "requiere_examen": True,
        "extiende_certificado": False, "avalado_por_organizacion": True,
        "estado": "publicado", "validado_en": "2026-10-24T11:20:00Z",
    },
    {
        "id": 6, "titulo": "Estadística para ciencia de datos", "plataforma": "YouTube", "categoria_id": 8,
        "tema": "Probabilidad, distribuciones y regresión", "anio_edicion": 2023,
        "docentes": "Paula Romero", "tiene_cuestionarios": False, "requiere_examen": False,
        "extiende_certificado": False, "avalado_por_organizacion": False,
        "estado": "publicado", "validado_en": "2026-10-25T18:05:00Z",
    },
    # Estos dos NO deben aparecer en el catálogo (BR-001): sirven para probar el filtro.
    {
        "id": 7, "titulo": "Docker para desarrolladores", "plataforma": "YouTube", "categoria_id": 5,
        "tema": "Imágenes, contenedores y Compose", "anio_edicion": 2026,
        "docentes": "Tomás Acosta", "tiene_cuestionarios": False, "requiere_examen": False,
        "extiende_certificado": False, "avalado_por_organizacion": False,
        "estado": "en_revision", "validado_en": None,
    },
    {
        "id": 8, "titulo": "Curso intensivo de React", "plataforma": "Udemy", "categoria_id": 3,
        "tema": "Componentes, hooks y estado", "anio_edicion": 2025,
        "docentes": "Valeria Núñez", "tiene_cuestionarios": True, "requiere_examen": False,
        "extiende_certificado": True, "avalado_por_organizacion": False,
        "estado": "rechazado", "validado_en": "2026-10-24T12:00:00Z",
    },
]

CAMPOS_DE_BUSQUEDA = ("titulo", "tema", "plataforma", "docentes")


class CursoRepositoryEnMemoria:
    def __init__(self, cursos: list[dict]):
        self._cursos = cursos

    def listar_publicados(
        self, *, categoria_id: int | None, q: str | None, offset: int, limit: int
    ) -> tuple[list[dict], int]:
        """Devuelve (cursos de la página, total) de los cursos publicados que coinciden."""
        cursos = [curso for curso in self._cursos if curso["estado"] == "publicado"]
        if categoria_id is not None:
            cursos = [curso for curso in cursos if curso["categoria_id"] == categoria_id]
        if q:
            termino = q.casefold()
            cursos = [
                curso for curso in cursos
                if any(termino in curso[campo].casefold() for campo in CAMPOS_DE_BUSQUEDA)
            ]
        cursos.sort(key=lambda curso: curso["validado_en"], reverse=True)
        return cursos[offset : offset + limit], len(cursos)


@lru_cache
def get_repositorio() -> CursoRepositoryEnMemoria:
    return CursoRepositoryEnMemoria(CURSOS_DEMO if get_settings().seed_demo else [])
