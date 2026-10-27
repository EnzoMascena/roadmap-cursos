# Senda

> WebApp de gestión de comunidad de cursos: catálogo comunitario de cursos gratuitos, validado
> por moderadores, + roadmaps personales de aprendizaje.
>
> **Estado:** 🚧 Desarrollo (Instancia B) — scaffold v0.1.0: catálogo de ejemplo con backend, frontend y Docker Compose.

**Stack:** React 19 + Vite + pnpm · FastAPI + uv · PostgreSQL 18.6 · Docker Compose (dev)

---

## Cómo levantar

Requisitos: **Git** y **Docker** con Docker Compose (versiones registradas en el
[TRD §1](docs/TRD.md#1-stack-y-versiones-exactas): Docker 29.6.2 · Compose 5.1.4).

```bash
git clone https://github.com/EnzoMascena/roadmap-cursos.git
cd roadmap-cursos
cp .env.example .env
docker compose up
```

La primera vez construye las imágenes (tarda unos minutos). Cuando los 3 servicios están arriba:

| Qué | URL | Qué tenés que ver |
|-----|-----|-------------------|
| Frontend | http://localhost:5173 | el catálogo con 6 cursos de ejemplo |
| Backend | http://localhost:8000/health | `{"status":"ok"}` |
| API del catálogo | http://localhost:8000/api/v1/cursos | la primera página del catálogo en JSON |
| API + base de datos | http://localhost:8000/api/v1/health | `{"status":"ok","db":"ok"}` (si da `503`, PostgreSQL todavía está arrancando: esperá unos segundos) |
| Documentación de la API | http://localhost:8000/docs | Swagger UI de FastAPI |
| PostgreSQL | `localhost:5432` | usuario, clave y base: `senda` |

- **Frenar:** `Ctrl+C` y después `docker compose down` (con `-v` también borra los datos de la base).
- **Si cambian dependencias** (`pyproject.toml` o `package.json`): `docker compose up --build`.
- **Ver el estado vacío del catálogo:** `SEED_DEMO=false` en el `.env` y `docker compose up -d backend`.
- **Puerto ocupado** (`port is already allocated`): frená el otro servicio (`docker ps` para verlo)
  o cambiá `POSTGRES_PORT`, `BACKEND_PORT` o `FRONTEND_PORT` en el `.env`.

<details>
<summary>Sin Docker (opcional)</summary>

- **Backend** (requiere uv): `cd backend && uv sync && uv run uvicorn app.main:app --reload`
  → http://localhost:8000/health
- **Frontend** (requiere Node 20.19+ o 22.12+ y pnpm 12): `cd frontend && pnpm install && pnpm dev`
  → http://localhost:5173 (el proxy `/api` apunta a `http://localhost:8000`)

</details>

## Qué hace

Cualquier estudiante puede aportar un curso gratuito de cualquier plataforma, con sus datos
(categoría, docentes, si da certificado, si exige examen, si lo avala una organización) y
declarando si lo tomó. Un administrador valida cada aporte y, al aprobarlo, el curso entra al
catálogo comunitario, público y paginado. Desde ahí, cada usuario arma su roadmap personal y
marca su avance: pendiente, en curso o completado.

## Documentación

| Documento | Responde la pregunta | Link |
|-----------|----------------------|------|
| SPEC | ¿Qué nos pidieron construir y qué decidimos nosotros? | [docs/SPEC.md](docs/SPEC.md) |
| PRD | ¿Para quién, qué problema resuelve, qué hace y qué NO hace? | [docs/PRD.md](docs/PRD.md) |
| TRD | ¿Cómo lo construimos técnicamente y por qué? | [docs/TRD.md](docs/TRD.md) |
| UX-UI | ¿Cómo se ve, se siente y se comporta? | [docs/UX-UI.md](docs/UX-UI.md) |
| APPFlow | ¿Qué pantallas hay y cómo se navega? | [docs/APPFlow.md](docs/APPFlow.md) |
| BackendSchema | ¿Qué datos persistimos y qué API expone? | [docs/BackendSchema.md](docs/BackendSchema.md) |
| Implementation Plan | ¿En qué orden construimos y qué significa "hecho"? | [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) |

**Orden de lectura sugerido:** SPEC → PRD → APPFlow → BackendSchema → TRD → UX-UI → Implementation Plan.

## Cómo revisar este repo

- Los `.md` se renderizan solos en GitHub, incluidos los diagramas Mermaid (`flowchart`,
  `erDiagram`, `stateDiagram`).
- La historia muestra la evolución de la SPEC: `git log --reverse --oneline -- docs/SPEC.md`
  (primer commit = SPEC de clase tal cual; después, el refinamiento).
- El flujo de Git se ve con `git log --graph --oneline --all`: ramas `feat/T{N}-…` mergeadas a
  `dev` y releases de `dev` a `main` con tag (detalle en
  [TRD §4.1](docs/TRD.md#41-flujo-de-git--main-dev-y-releases-versionadas)).
- Las versiones publicadas se listan con `git tag` y se describen en el [CHANGELOG](CHANGELOG.md).
- Preview local: VS Code con `Ctrl+Shift+V`.

## Estado del trabajo

| Instancia | Contenido | Estado |
|-----------|-----------|--------|
| A — Documentación | repo + 7 documentos | ✅ entregada el 23/10/2026 |
| B — Desarrollo del MVP | ejecución del [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) (US-001 a US-010) | 🚧 en curso |
| Clase 27/10 | flujo `main`/`dev`, scaffold y release `v0.1.0` | 🚧 en curso |

## Versionado

- **Flujo de Git:** `main` solo tiene releases taggeadas (`vX.Y.Z`); `dev` integra el trabajo;
  cada ticket se hace en `feat/T{N}-descripcion-corta` (o `fix/descripcion-corta`), que nace de
  `dev` y vuelve a `dev` con `git merge --no-ff`. Un release lleva `dev` a `main` con tag anotado y
  el [CHANGELOG](CHANGELOG.md) actualizado. La Instancia A (documentación) se hizo antes con
  GitHub Flow adaptado. Detalle en el [TRD §4](docs/TRD.md#4-convenciones).
- **Versionado:** [SemVer](https://semver.org/lang/es/), en `0.y.z` mientras el producto es inestable.
- **Convención de commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `docker:`,
  `chore:`, `refactor:`), también en los merge commits.

---

## Referencias de aprendizaje

### Markdown

| Recurso | Para qué |
|---------|----------|
| [Markdown Guide — sintaxis básica](https://www.markdownguide.org/basic-syntax/) | encabezados, listas, énfasis, imágenes |
| [Markdown Guide — cheat sheet](https://www.markdownguide.org/cheat-sheet/) | tablas, task lists, bloques de código |
| [CommonMark — referencia](https://commonmark.org/help/) | la especificación cuando hay dudas |
| [GitHub — Writing on GitHub](https://docs.github.com/en/get-started/writing-on-github) | GFM, tablas, checklists |
| [GitHub — Mermaid en Markdown](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) | diagramas que renderizan en el repo |

### Por tipo de documento

| Documento | Recurso |
|-----------|---------|
| PRD | [Atlassian — Plantilla PRD](https://www.atlassian.com/software/confluence/templates/product-requirements) · [Lenny Rachitsky — plantilla](https://www.atlassian.com/software/confluence/templates/requirements) |
| TRD | [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/) |
| UX-UI | [NN/g — Front-End Style-Guides](https://www.nngroup.com/articles/front-end-style-guides/) · [NN/g — Design Systems 101](https://www.nngroup.com/articles/design-systems-101/) · [Material Design 3](https://m3.material.io/) · [Material Symbols](https://fonts.google.com/icons) |
| APPFlow | [NN/g — IA vs. Sitemaps](https://www.nngroup.com/articles/information-architecture-sitemaps/) · [NN/g — User Journeys vs. User Flows](https://www.nngroup.com/articles/user-journeys-vs-user-flows/) |
| BackendSchema | [Mermaid — ER Diagrams](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) · [PostgreSQL — Conceptual Model](https://www.postgresql.org/docs/current/datamodel.html) |
| Implementation Plan | [Atlassian — Plantilla de plan de proyecto](https://www.atlassian.com/software/confluence/templates/project-plan) · [Shape Up](https://basecamp.com/shapeup/) |

---

## Licencia / uso

Trabajo Práctico — Desarrollo de Software, UTN FR La Plata, 2026 · Enzo Mario Mascena.
