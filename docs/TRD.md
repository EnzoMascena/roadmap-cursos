# TRD — Technical Requirements Document — Senda

> **Qué es:** el CÓMO técnico de Senda: stack, decisiones con sus alternativas, arquitectura,
> estructura de carpetas y convenciones (incluido el flujo de Git). El producto está en el
> [PRD](PRD.md); el orden de construcción, en el [Implementation Plan](IMPLEMENTATION_PLAN.md).

## 1. Stack y versiones exactas

Versiones verificadas en npm y PyPI el 23/10/2026. Quedan fijadas en `pnpm-lock.yaml`, `uv.lock`
e imágenes Docker al crear el scaffold (M0).

| Capa | Elección | Versión exacta | Por qué |
|------|----------|----------------|---------|
| Frontend | React + React DOM | 19.3.1 | fijado por la SPEC (React 19, última estable) |
| Frontend | Vite + `@vitejs/plugin-react` | 8.3.5 + 6.1.2 | fijado por la SPEC; dev server rápido con proxy a la API |
| Frontend | pnpm (vía corepack) | 12.15.0 | fijado por la SPEC; se declara en `packageManager` |
| Frontend | React Router | 7.18.4 | ruteo SPA con rutas anidadas y guards; se elige la rama 7.x, estable y muy documentada |
| Frontend | Node.js (runtime en contenedor) | 22 LTS (`node:22-alpine`) | Vite 8 requiere Node ≥ 20.19 / 22.12 |
| Backend | FastAPI | 0.158.2 | fijado por la SPEC (referencia de la cátedra al 21/10/2026) |
| Backend | uv | 0.13.5 | fijado por la SPEC; `uv.lock` reproducible |
| Backend | Python (runtime en contenedor) | 3.13 (`python:3.13-slim`) | versión estable soportada por todas las dependencias |
| Backend | Uvicorn | 0.54.0 | servidor ASGI con `--reload` para desarrollo |
| ORM / driver | SQLAlchemy + psycopg (binary) | 2.1.6 + 3.3.6 | ORM maduro con tipado 2.x; driver oficial de PostgreSQL para Python 3 |
| Migraciones | Alembic | 1.20.1 | migraciones versionadas en el repo (ver TD-009) |
| Validación | Pydantic + pydantic-settings + email-validator | 2.14.1 + 2.16.1 + 2.3.0 | schemas de request/response y configuración por variables de entorno |
| Seguridad | bcrypt + PyJWT | 5.0.0 + 2.15.1 | hash de contraseñas (TD-003) y tokens de acceso (TD-001) |
| Rate limiting | slowapi | 0.1.10 | límites por IP declarativos sobre endpoints de FastAPI (TD-006) |
| BD | PostgreSQL | 18.6 (`postgres:18.6`) | fijado por SPEC |
| Mail (dev) | Mailpit | tag `v1.x` exacto se fija en la tarea 0.2 | SMTP de prueba con bandeja web (TD-007); herramienta auxiliar, no forma parte del stack de la SPEC |
| Infra (dev) | Docker Engine + Docker Compose | 29.6.2 · 5.1.4 | entorno reproducible con un solo comando |

> FastAPI se fija en **0.158.2** aunque PyPI ya publica versiones posteriores: es la referencia de
> la SPEC y mantiene el entorno comparable con el de la cátedra. Subir de versión entra como ticket
> `chore(deps)` con su propia rama.

## 2. Decisiones técnicas

| # | Decisión | Alternativas consideradas | Elegida | Por qué |
|---|----------|---------------------------|---------|---------|
| TD-001 | Autenticación | JWT stateless / sesión server-side con cookie / OAuth externo | **JWT de acceso** (HS256, 60 min) enviado como `Authorization: Bearer`; guardado en `sessionStorage`; sin refresh token; logout en el cliente | API sin estado y simple de probar con curl/Postman. `sessionStorage` acota la exposición a la pestaña. Contra: no se puede revocar un token antes de que venza; se acepta por el vencimiento corto. |
| TD-002 | Paginación | offset + total / cursor-based | **Offset**: `page` (≥ 1) y `page_size` (1 a 100, default 12); respuesta `{items, total, page, page_size, pages}` en **todos** los listados | El paginador numérico estilo Google necesita el total y saltar a una página. Con el volumen del MVP el costo de `OFFSET` es despreciable. Default 12 porque divide justo en grillas de 1, 2 y 3 columnas. |
| TD-003 | Hash de contraseñas | bcrypt / argon2id / scrypt | **bcrypt**, costo 12, con la librería `bcrypt` directa | Cumple el mínimo de la SPEC con una librería mantenida (passlib está abandonada). Costo 12 ≈ 250 ms por hash: caro para fuerza bruta, tolerable en login. Límite de 72 bytes de bcrypt → la contraseña se valida de 8 a 64 caracteres y ≤ 72 bytes. argon2id es más fuerte pero suma una dependencia que el MVP no necesita. |
| TD-004 | Modelo de "mi roadmap" | tabla intermedia con estado / array o JSONB en el usuario | **Tabla `roadmap_items`** (usuario, curso, orden, estado) con `UNIQUE (usuario_id, curso_id)` | Integridad referencial, paginación y filtros por SQL, y la regla de "sin duplicados" la garantiza la base. |
| TD-005 | Roles y autorización | columna `rol` / tabla de roles y permisos | **Columna `rol`** (`usuario` o `admin`) + dependencias `get_usuario_actual` y `require_admin` | Solo hay dos roles; una tabla de permisos sería sobreingeniería. 401 sin token o token inválido, 403 con rol insuficiente o recurso ajeno. |
| TD-006 | Rate limiting | slowapi (memoria) / middleware propio / Redis o proxy reverso | **slowapi** con almacenamiento en memoria, por IP: login 5/min, solicitud de recuperación 3 cada 15 min → `429` con `Retry-After` | Cumple la SPEC con poco código. Limitación conocida: el contador vive en el proceso (1 worker en dev) y se reinicia con el contenedor; con varias instancias se movería a Redis (fuera de alcance). |
| TD-007 | Envío del mail de recuperación | log en consola / proveedor SMTP real / SMTP de prueba | **Mailpit** en el compose; envío con `smtplib` (stdlib) | Ciclo completo verificable desde la UI sin credenciales reales. Token `secrets.token_urlsafe(32)`, se guarda solo su SHA-256, vence a los 30 min y es de un solo uso. La solicitud siempre responde 202 (no revela si el email existe). |
| TD-008 | Formato de errores de API | envelope propio / RFC 7807 problem+json | **Envelope propio** `{"error": {"code", "message", "details"}}`, también para los 422 de validación (handler propio) | Un solo formato para todo el frontend; `code` estable en MAYÚSCULAS para decidir en la UI sin parsear textos. |
| TD-009 | Acceso a datos y esquema | SQLAlchemy + Alembic / SQLModel / SQL crudo + scripts | **SQLAlchemy 2.1 (sync) + Alembic**; seed idempotente en `app/seed.py` | Migraciones versionadas en git (el esquema cambia por commits revisables). Sync en vez de async: más simple de depurar y suficiente para el volumen del MVP. |
| TD-010 | Estado y datos en el frontend | hooks propios + `fetch` / TanStack Query / Redux | **Hooks propios** (`usePaginatedQuery`, `useMutation`) + `SessionContext` | Pocas dependencias y hooks testeables con Vitest el 27/10. La sesión es el único estado global. |
| TD-011 | Estilos | CSS propio con custom properties + CSS Modules / Tailwind / MUI | **CSS propio**: tokens globales en `styles/tokens.css` + un `*.module.css` por componente | Mapea 1:1 con la guía [UX-UI](UX-UI.md) y hace verificable la regla mobile-first (las media queries están a la vista). MUI daría la estética Material pero esconde el responsive y pesa demasiado. |
| TD-012 | Duplicados de URL | sin control / `UNIQUE` simple / índice único parcial | **Índice único parcial** sobre `url_normalizada` `WHERE estado <> 'rechazado'` + chequeo previo en el service | La base garantiza BR-005 incluso con dos envíos simultáneos, y un rechazo libera la URL. |

## 3. Arquitectura

### 3.1 Patrón y capas

Screaming Architecture + arquitectura en capas:

```mermaid
flowchart LR
    HTTP["Router (HTTP)"] --> SVC["Service (reglas de negocio)"]
    SVC --> REPO["Repository (acceso a datos)"]
    REPO --> DB[("PostgreSQL 18.6")]
    SVC --> MODELS["Models y schemas"]
```

- **Router:** recibe HTTP, valida el input con Pydantic, resuelve dependencias (sesión, rol) y
  delega. Sin lógica de negocio.
- **Service:** reglas de negocio (BR-001 a BR-010) como funciones testeables: reciben datos y
  repositorios, no conocen HTTP. Lanzan errores de dominio (`ErrorDeDominio` con `code` y
  `status`), que un handler global traduce al envelope de TD-008.
- **Repository:** única puerta a la base (SQLAlchemy). Sin reglas de negocio.
- **La estructura de carpetas habla del dominio:** al abrir `backend/app/` se lee identidad,
  catálogo, aportes, validación y roadmap, no "controllers/services/models".

### 3.2 Estructura de carpetas (la que se va a crear en la Instancia B)

```
roadmap-cursos/
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── migrations/                  # Alembic: env.py + versions/
│   ├── app/
│   │   ├── main.py                  # crea la app, monta routers y handlers
│   │   ├── config.py                # Settings (pydantic-settings) desde variables de entorno
│   │   ├── seed.py                  # categorías, admin y datos demo (idempotente)
│   │   ├── compartido/              # lo transversal, sin reglas de negocio
│   │   │   ├── db.py                # engine, sesión, Base
│   │   │   ├── errores.py           # ErrorDeDominio + handlers del envelope
│   │   │   ├── paginacion.py        # Page[T], parámetros page/page_size
│   │   │   └── correo.py            # envío SMTP (Mailpit en dev)
│   │   ├── identidad/               # registro, login, sesión, recuperación
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   ├── models.py            # Usuario, TokenRecuperacion
│   │   │   ├── schemas.py
│   │   │   ├── seguridad.py         # bcrypt + JWT + dependencias de sesión y rol
│   │   │   └── rate_limit.py        # limiter de slowapi
│   │   ├── catalogo/                # cursos publicados y categorías (lectura pública)
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   ├── models.py            # Curso, Categoria (dueño de la tabla cursos)
│   │   │   └── schemas.py
│   │   ├── aportes/                 # alta de cursos por la comunidad + mis aportes
│   │   │   ├── router.py
│   │   │   ├── service.py           # normalización de URL, duplicados, reglas del aval
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── validacion/              # moderación: pendientes y decisión (solo admin)
│   │   │   ├── router.py
│   │   │   ├── service.py           # transiciones en_revision → publicado/rechazado
│   │   │   └── schemas.py
│   │   └── roadmap/                 # roadmap personal
│   │       ├── router.py
│   │       ├── service.py
│   │       ├── repository.py
│   │       ├── models.py            # RoadmapItem
│   │       └── schemas.py
│   └── tests/                       # se implementa el 27/10 (ver Implementation Plan §5)
├── frontend/
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── vite.config.js               # proxy /api → backend:8000
│   ├── Dockerfile
│   └── src/
│       ├── main.jsx
│       ├── app/                     # shell: router, layout, guards, sesión
│       │   ├── App.jsx
│       │   ├── router.jsx
│       │   ├── Layout.jsx           # header + drawer + contenido + snackbar
│       │   ├── RequiereSesion.jsx
│       │   ├── RequiereAdmin.jsx
│       │   └── SessionContext.jsx
│       ├── compartido/
│       │   ├── api/cliente.js       # fetch + token + envelope de errores
│       │   ├── hooks/               # usePaginatedQuery, useMutation
│       │   └── ui/                  # Boton, CampoTexto, Select, Chip, Paginador, Dialogo, Snackbar, Skeleton, EstadoVacio
│       ├── features/
│       │   ├── identidad/           # LoginPage, RegistroPage, RecuperarPage, NuevaPasswordPage
│       │   ├── catalogo/            # HomePage, CatalogoPage, DetalleCursoPage, CursoCard, Filtros
│       │   ├── aportes/             # AportarPage, MisAportesPage, DetalleAportePage, FormularioAporte
│       │   ├── validacion/          # PendientesPage, RevisionPage
│       │   └── roadmap/             # RoadmapPage, RoadmapItem
│       │   # cada feature: components/, hooks/, api.js
│       └── styles/
│           ├── tokens.css           # variables de UX-UI §2.4
│           └── base.css             # reset, tipografía, layout base sin media queries
├── docker-compose.yml
├── .env.example
├── README.md
└── docs/
```

### 3.3 Servicios Docker (entorno de desarrollo)

| Servicio | Imagen/base | Puerto | Rol |
|----------|-------------|--------|-----|
| postgres | `postgres:18.6` | 5432 | base de datos; volumen `pgdata` montado en `/var/lib/postgresql` (cambio de PostgreSQL 18) |
| backend | `python:3.13-slim` + uv 0.13.5 | 8000 | API FastAPI con `--reload`; al iniciar corre `alembic upgrade head` y el seed |
| frontend | `node:22-alpine` + pnpm 12.15.0 | 5173 | Vite dev server (`host: true`) con proxy `/api` → `http://backend:8000` |
| mailpit | `axllent/mailpit` | 8025 (web) · 1025 (SMTP, interno) | bandeja de los mails de recuperación |

```mermaid
flowchart LR
    BROWSER["Navegador :5173"] --> FE["frontend (Vite)"]
    FE -- "/api/*" --> BE["backend FastAPI :8000"]
    BE --> PG[("postgres :5432")]
    BE -- "SMTP :1025" --> MP["mailpit"]
    BROWSER -. "bandeja :8025" .-> MP
```

- `backend` espera a `postgres` con `depends_on: condition: service_healthy` (healthcheck básico
  con `pg_isready`).
- Código montado como volumen para hot reload; `node_modules` y `.venv` quedan en volúmenes del
  contenedor para no pisarse con los del host.
- Todas las variables tienen valor por defecto de desarrollo en el compose (`${VAR:-default}`),
  así `docker compose up` funciona en una máquina limpia sin crear `.env`.

> En la clase del 27/10 estos Dockerfiles evolucionan a multi-stage. Por ahora, lo mínimo que levanta.

## 4. Convenciones

### 4.1 Flujo de Git — main, dev y releases versionadas

> **Cambio de flujo (27/10/2026, consigna de la clase):** la documentación de la Instancia A se
> hizo con GitHub Flow adaptado (ramas `docs/<documento>` mergeadas directo a `main`). Desde el
> scaffold v0.1.0 el proyecto usa este flujo, con una rama de integración `dev` y releases
> taggeadas. La historia anterior queda como está.

```mermaid
gitGraph
    commit id: "docs Instancia A"
    branch dev
    checkout dev
    branch T1-scaffold
    commit id: "chore: scaffold"
    checkout dev
    merge T1-scaffold
    branch T2-backend
    commit id: "feat: backend"
    checkout dev
    merge T2-backend
    commit id: "docs: changelog"
    checkout main
    merge dev tag: "v0.1.0"
```

| Rama | Nace de | Contiene | Se mergea a |
|------|---------|----------|-------------|
| `main` | — (raíz) | solo releases taggeadas `vX.Y.Z` con el `CHANGELOG.md` actualizado | — |
| `dev` | `main` (una sola vez) | integración: todo lo que entra al próximo release | `main`, solo en un release |
| `feat/T{N}-descripcion-corta` | `dev` | una feature o un ticket (N = número de ticket) | `dev` |
| `fix/descripcion-corta` | `dev` | un fix | `dev` |

- **`main` no se toca:** nunca recibe commits directos ni merges de `feat/*` o `fix/*`. Solo
  recibe `dev` en el momento de un release, siempre con tag.
- **Ramas de trabajo:** nacen de `dev` y vuelven a `dev` con `git merge --no-ff` (el merge commit
  deja la rama visible en la historia). Después se borran con `git branch -d <rama>`.
- **Merge commits convencionales:** `<tipo>: merge feat/T{N}-… into dev` (el tipo es el del
  ticket) y `chore(release): merge dev into main for vX.Y.Z`.
- **Release** (ejemplo `v0.1.0`):
  1. todas las ramas del release mergeadas a `dev`, sin ramas `feat/*` huérfanas;
  2. en `dev`: el `CHANGELOG.md` pasa lo de `[Unreleased]` a `[vX.Y.Z] - AAAA-MM-DD` y el
     [Implementation Plan](IMPLEMENTATION_PLAN.md) marca las tareas cerradas
     (`docs: finalize changelog for vX.Y.Z`);
  3. `git switch main && git merge --no-ff dev -m "chore(release): merge dev into main for vX.Y.Z"`;
  4. `git tag -a vX.Y.Z -m "release: …"` y `git push origin main dev --tags`.
- **Versionado semántico:** `v0.y.z` mientras el producto es inestable. MINOR (`v0.X.0`):
  features nuevas compatibles · PATCH (`v0.y.Z`): fixes sin features · MAJOR (`vX.0.0`): cambio
  que rompe compatibilidad (por ejemplo, de la API).
- **CHANGELOG:** `CHANGELOG.md` en la raíz con formato
  [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/); categorías `Added`, `Changed`,
  `Fixed` y `Removed`, solo las que tengan contenido. Cada ticket suma su línea en `[Unreleased]`.
- **Quién revisa:** trabajo individual → auto-revisión antes de cada merge (`git diff dev...<rama>`
  y el "Hecho cuando…" de la tarea en el plan). Las observaciones del docente entran como `fix/…`
  o como un ticket nuevo.

### 4.2 Commits

- [Conventional Commits 1.0](https://www.conventionalcommits.org/es/v1.0.0/): `tipo(scope): descripción`,
  en inglés, modo imperativo, ≤ 72 caracteres, sin punto final. Cuerpo opcional y breve.
- **Tipos:** `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `docker`.
- **Scopes:** los dominios (`identidad`, `catalogo`, `aportes`, `validacion`, `roadmap`) y
  `infra`, `ui`, `deps`, o el documento (`spec`, `prd`, `trd`, `ux-ui`, `appflow`, `schema`, `plan`).
- Ejemplos: `docs(prd): add user stories with acceptance criteria` ·
  `feat(identidad): add login rate limit with slowapi` · `fix(roadmap): reject duplicate course`.
- Prohibido: `wip`, `cambios`, `update`, `fix stuff` o mensajes que no digan qué cambió.

### 4.3 Errores de API (TD-008)

Todas las respuestas de error usan el mismo envelope:

```json
{
  "error": {
    "code": "CURSO_DUPLICADO",
    "message": "Este curso ya fue aportado.",
    "details": null
  }
}
```

Errores de validación (422), con el detalle por campo para mostrarlo junto al input:

```json
{
  "error": {
    "code": "VALIDACION",
    "message": "Hay datos inválidos.",
    "details": [{ "campo": "anio_edicion", "mensaje": "Debe estar entre 1990 y 2026." }]
  }
}
```

El catálogo completo de `code` está en [BackendSchema §3](BackendSchema.md#3-api-rest).

### 4.4 Variables de entorno

| Variable | Ejemplo (default de desarrollo) | Obligatoria | Descripción |
|----------|---------------------------------|-------------|-------------|
| `DATABASE_URL` | `postgresql+psycopg://senda:senda@postgres:5432/senda` | sí | conexión de SQLAlchemy |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | `senda` / `senda` / `senda` | sí | inicialización del contenedor de PostgreSQL |
| `JWT_SECRET` | `dev-cambiar-en-serio` | sí | clave de firma HS256 (en dev tiene default; nunca se reutiliza fuera de dev) |
| `JWT_EXPIRES_MINUTES` | `60` | no | vencimiento del token de acceso |
| `FRONTEND_URL` | `http://localhost:5173` | sí | base del enlace de recuperación que va en el mail |
| `SMTP_HOST` / `SMTP_PORT` | `mailpit` / `1025` | sí | servidor SMTP (Mailpit en dev) |
| `MAIL_FROM` | `Senda <no-reply@senda.local>` | no | remitente de los mails |
| `RESET_TOKEN_MINUTES` | `30` | no | vencimiento del token de recuperación |
| `LOGIN_RATE_LIMIT` | `5/minute` | no | límite de slowapi para `POST /auth/login` |
| `RECOVERY_RATE_LIMIT` | `3/15minutes` | no | límite para `POST /auth/recuperacion` |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` / `ADMIN_NOMBRE` | `admin@senda.local` / `Admin1234` / `Moderación Senda` | sí (seed) | primer usuario admin que crea el seed si no existe |
| `SEED_DEMO` | `true` | no | carga usuarios y cursos de demostración |
| `VITE_API_BASE_URL` | `/api/v1` | no | base de la API en el frontend (pasa por el proxy de Vite) |

### 4.5 Logging y excepciones

- Logging estándar de Python a stdout (lo junta `docker compose logs`), nivel `INFO` en dev.
- Un middleware registra método, ruta, status y duración de cada request.
- **Nunca** se loggean contraseñas, tokens (JWT o de recuperación) ni el header `Authorization`.
- Los services lanzan `ErrorDeDominio(code, message, status)`; handlers globales lo traducen al
  envelope. Las excepciones no previstas devuelven `500` con `code: "ERROR_INTERNO"` y se loggean
  con stack trace.

## 5. Requisitos no funcionales técnicos (traducción de las restricciones)

| Restricción (SPEC) | Cómo se cumple | Dónde se verifica |
|--------------------|----------------|-------------------|
| Paginación de listados | TD-002 en todos los endpoints de listado (cursos, categorías, mis aportes, pendientes, roadmap) | `GET /api/v1/cursos?page=2&page_size=12` y paginador en cada pantalla de listado ([APPFlow §3](APPFlow.md#3-fichas-de-pantalla)) |
| Mobile-first con mejora progresiva | tokens + CSS base sin media queries; solo `@media (min-width: 600px)` y `(min-width: 840px)` | [UX-UI §3](UX-UI.md#3-estrategia-mobile-first-con-mejora-progresiva); `grep -rn "@media" frontend/src` solo devuelve `min-width` |
| Menú sándwich | componente `Header` + `NavigationDrawer` con `aria-expanded` y `aria-controls`, visible < 840 px | [UX-UI §4.5](UX-UI.md#45-menú-sándwich-navigation-drawer) · [APPFlow §5](APPFlow.md#5-estados-globales-de-la-app) |
| Screaming Architecture | árbol de §3.2: carpetas por dominio en back (`app/<dominio>`) y front (`features/<dominio>`) | revisión del repo |
| Rate limiting en login | TD-006 | 6 logins fallidos seguidos → el sexto responde `429` |
| bcrypt como mínimo | TD-003 | `SELECT password_hash FROM usuarios` empieza con `$2b$12$` |

## 6. Riesgos técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| PostgreSQL 18 cambió la ruta de datos del contenedor: un volumen en `/var/lib/postgresql/data` falla o no persiste | media | alto | montar el volumen en `/var/lib/postgresql` (§3.3) y probar `docker compose down && up` en la tarea 0.2 |
| El rate limiter en memoria se reinicia con el contenedor y no sirve con varios workers | alta | bajo | aceptado para dev (1 worker); documentado en TD-006; Redis si se escala |
| bcrypt 5 lanza error con contraseñas de más de 72 bytes | media | medio | validar longitud en bytes en el schema antes de hashear (TD-003) |
| Hot reload de Vite o Uvicorn no detecta cambios dentro de Docker | media | medio | `host: true`; si el sistema de archivos no notifica, `server.watch.usePolling` |
| Versiones nuevas (Vite 8, pnpm 12) con cambios respecto de tutoriales conocidos | media | medio | versiones fijadas en lockfiles; ante un bloqueo, bajar de versión menor queda documentado como ticket `chore(deps)` |
| El tiempo de la Instancia B (fin de semana) no alcanza para todos los P0 | media | alto | plan ordenado por dependencias con estimaciones; P1 separado en M5; seed con datos para probar cada historia sin cargar a mano |

---

**Referencia:**
- Design Docs at Google (el clásico de los design docs, con énfasis en trade-offs):
  https://www.industrialempathy.com/posts/design-docs-at-google/
