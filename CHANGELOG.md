# Changelog

Todos los cambios relevantes de Senda se registran en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto usa
[Versionado Semántico](https://semver.org/lang/es/) (`0.y.z` mientras el producto es inestable).

## [Unreleased]

### Added

- Flujo de Git con `main` (releases taggeadas), `dev` (integración) y ramas `feat/T{N}-…` / `fix/…`.
- Estructura de carpetas por dominio (Screaming Architecture) en `backend/app` y `frontend/src/features`.
- `.env.example` con las variables de desarrollo y este `CHANGELOG.md`.
- Backend mínimo con FastAPI + uv: `GET /health`, `GET /api/v1/health` (chequea la base) y `GET /api/v1/cursos` paginado, con cursos de ejemplo en memoria.
- Frontend mínimo con React + Vite + pnpm: pantalla de catálogo que consume `GET /api/v1/cursos`, con estados de carga, error y vacío, paginador y proxy `/api` hacia el backend.

### Changed

- TRD §4.1: el flujo de Git pasa de GitHub Flow adaptado a `main`/`dev` con releases versionadas.
- BackendSchema §3.6: se documenta `GET /health` y el error `503 BD_NO_DISPONIBLE`.

[Unreleased]: https://github.com/EnzoMascena/roadmap-cursos/compare/main...dev
