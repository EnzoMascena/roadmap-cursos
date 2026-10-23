# Senda

> WebApp de gestión de comunidad de cursos: catálogo comunitario de cursos gratuitos, validado
> por moderadores, + roadmaps personales de aprendizaje.
>
> **Estado:** 📚 Documentación (Instancia A) — desarrollo pendiente de aprobación docente.

**Stack:** React 19 + Vite + pnpm · FastAPI + uv · PostgreSQL 18.6 · Docker Compose (dev)

---

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
- El flujo de Git se ve con `git log --graph --oneline --all`: una rama por documento, mergeada
  con `--no-ff` a `main` (detalle en [TRD §4.1](docs/TRD.md#41-flujo-de-git--github-flow-adaptado)).
- Preview local: VS Code con `Ctrl+Shift+V`.

## Estado del trabajo

| Instancia | Contenido | Estado |
|-----------|-----------|--------|
| A — Documentación | repo + 7 documentos | ✅ enviada a aprobación el 23/10/2026 |
| B — Desarrollo del MVP | ejecución del [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) (US-001 a US-010) | ⏳ pendiente de aprobación |
| C — Clase 27/10 | testing, Docker multi-stage, gestión del cambio | ⏳ |

> Las instrucciones para levantar el proyecto (`docker compose up`, URLs, usuarios de prueba) se
> agregan en la Instancia B (tarea 6.1 del plan).

## Versionado

- **Flujo de Git:** GitHub Flow adaptado. `main` siempre entregable y sin commits directos (salvo
  el primer commit con la SPEC original, exigido por la consigna). Cada documento o tarea del plan
  se trabaja en una rama corta (`docs/<documento>`, `feat/<modulo>-<tarea>`, `fix/…`, `docker/…`,
  `chore/…`) que vuelve a `main` con `git merge --no-ff`. Detalle en el
  [TRD §4](docs/TRD.md#4-convenciones).
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
