# SPEC — Senda

> **Qué es este documento:** la versión refinada de la SPEC de clase (21/10/2026).
> La SPEC original está versionada **tal cual** en el primer commit del repo
> (`git log --reverse --oneline -- docs/SPEC.md` muestra la evolución original → refinamiento).
> Mismos requisitos, ambigüedades resueltas y cada decisión trazable a su documento
> (producto → [PRD](PRD.md), técnica → [TRD](TRD.md), datos/API → [BackendSchema](BackendSchema.md)).

## 1. Identidad del producto

- **Nombre propio:** **Senda**
- **Una línea:** para estudiantes que aprenden con cursos gratuitos dispersos en muchas plataformas ·
  Senda reúne un catálogo validado por la comunidad y un roadmap personal de aprendizaje ·
  para que dejen de buscar y empiecen a avanzar.

## 2. Problema

Quien estudia sistemas (o cualquier carrera) y quiere complementar con cursos gratuitos se encuentra
con una oferta enorme y fragmentada: Coursera, edX, YouTube, Google Skillshop, cursos de universidades,
programas estatales. Cada plataforma tiene su buscador, sus criterios y su letra chica: no es obvio
si un curso da certificado, si exige examen o si lo avala alguna organización.

Hoy eso se resuelve con listas sueltas en grupos de WhatsApp, marcadores del navegador o planillas
personales. Esa información se pierde, se repite y no tiene garantía: nadie sabe si el link sigue
activo ni si quien lo recomienda realmente hizo el curso.

Una comunidad cambia la ecuación: cada estudiante que ya hizo un curso puede aportarlo con datos
estructurados (y declarar si lo tomó), un moderador lo valida y el curso pasa a un catálogo común
y buscable. Sobre ese catálogo, cada persona arma su propio roadmap y registra su avance.

## 3. Visión

En 12 meses, Senda es el lugar donde un estudiante de La Plata (y de cualquier lado) entra, filtra
por categoría, encuentra cursos gratuitos con sus condiciones claras —certificado, examen, aval— y
los suma a una ruta personal que va completando. El catálogo crece por aportes de la propia
comunidad, con una moderación que mantiene la calidad, y cada curso muestra cuánta gente lo tomó.

## 4. Alcance

### Dentro

- Cuenta de usuario: registro, login (con rate limiting), logout y recuperación de contraseña
  con ciclo completo (solicitud → enlace con token por mail → nueva contraseña).
- Aporte de cursos gratuitos con todos los datos mínimos de la SPEC + plataforma + declaración
  obligatoria de si el aportante lo tomó.
- Validación de aportes por un rol **administrador**: aprobar o rechazar con motivo.
- Catálogo comunitario público y paginado, con filtro por categoría y búsqueda por texto.
- Detalle de curso con enlace externo a la plataforma de origen.
- "Mis aportes": estado de cada aporte y motivo de rechazo.
- Roadmap personal: agregar cursos del catálogo, cambiar su estado (pendiente / en curso /
  completado) y quitarlos. Reordenar queda como P1.
- Interfaz mobile-first con mejora progresiva, menú sándwich, estética Google/Material y
  paginación en todos los listados.

### Fuera (out of scope explícito)

- Cursos pagos, pagos o suscripciones de cualquier tipo.
- Certificados emitidos por Senda.
- Login social (Google, GitHub), 2FA y verificación de email al registrarse.
- Comentarios, calificaciones, reseñas, likes o seguidores.
- Roadmaps públicos, compartibles o plantillas de roadmap.
- Verificación automática de URLs (scraping o chequeo periódico de que el enlace siga activo).
- Edición o despublicación de cursos ya publicados; ABM de categorías (vienen por seed); gestión
  de usuarios y roles desde la UI.
- Notificaciones por mail fuera de la recuperación de contraseña.
- App móvil nativa, PWA/offline e internacionalización (solo español).
- Despliegue productivo: el alcance es el entorno de desarrollo con Docker Compose.

## 5. Reglas de producto clave

| # | Regla | Origen |
|---|-------|--------|
| BR-001 | Todo curso aportado entra en estado `en_revision` y solo llega al catálogo comunitario cuando un administrador lo aprueba (`publicado`). | SPEC clase ("todo curso aportado y **validado** pasa al catálogo") |
| BR-002 | La declaración "¿tomaste este curso?" es obligatoria y explícita (sin valor por defecto) y se muestra en el detalle del curso. | SPEC clase + decisión propia |
| BR-003 | Validar es exclusivo del rol `admin`. Rechazar exige un motivo (10 a 500 caracteres) que el aportante ve en "Mis aportes". | decisión propia |
| BR-004 / BR-006 | El roadmap es personal y privado: cada usuario ve y modifica solo el suyo; solo admite cursos `publicado` y no admite el mismo curso dos veces. | decisión propia |
| BR-005 | Una misma URL (normalizada) no puede estar dos veces entre los cursos `en_revision` o `publicado`; un aporte rechazado libera la URL. | decisión propia → [BackendSchema §4](BackendSchema.md#4-decisiones-del-esquema) |

> Los IDs son los del [PRD §7](PRD.md#7-reglas-de-negocio), donde vive el detalle completo (BR-001 a BR-010).

## 6. Stack registrado (versiones exactas con las que se va a desarrollar)

El entorno de desarrollo corre **dentro de Docker**: las versiones de runtime y librerías quedan
fijadas en imágenes y lockfiles (versiones verificadas en npm y PyPI el 23/10/2026).

| Capa | Tecnología | Versión exacta | Dónde queda fijada |
|------|------------|----------------|--------------------|
| Frontend | React + React DOM | 19.3.1 | `frontend/package.json` + `pnpm-lock.yaml` |
| Frontend | Vite | 8.3.5 | `frontend/package.json` |
| Frontend | pnpm | 12.15.0 | `packageManager` en `package.json` (corepack) |
| Frontend | Node.js (runtime) | 22 LTS | imagen `node:22-alpine` |
| Backend | FastAPI | 0.158.2 | `backend/pyproject.toml` + `uv.lock` |
| Backend | uv | 0.13.5 | imagen `ghcr.io/astral-sh/uv:0.13.5` |
| Backend | Python (runtime) | 3.13 | imagen `python:3.13-slim` |
| Base de datos | PostgreSQL | 18.6 | imagen `postgres:18.6` |
| Infra (dev) | Docker Engine | 29.6.2 | máquina del desarrollador |
| Infra (dev) | Docker Compose | 5.1.4 | máquina del desarrollador |

> FastAPI: se fija **0.158.2**, la referencia de la SPEC de clase, aunque PyPI ya publica
> versiones posteriores. Así el entorno es comparable con el de la cátedra; actualizar entra
> como ticket `chore(deps)`. Detalle de librerías y el porqué de cada una en el [TRD §1](TRD.md#1-stack-y-versiones-exactas).

## 7. Restricciones técnicas heredadas de la SPEC de clase

| # | Restricción | Cómo la vamos a cumplir |
|---|-------------|-------------------------|
| 1 | Mobile-first con mejora progresiva: base sin media queries; `@media (min-width: …)` solo para agregar/mejorar | CSS base para 360 px sin media queries; solo `@media (min-width: 600px)` y `@media (min-width: 840px)` (breakpoints de Material 3) para agregar columnas y navegación horizontal. Ver [UX-UI §3](UX-UI.md#3-estrategia-mobile-first-con-mejora-progresiva). |
| 2 | Paginación de todas las consultas de listado y de sus tablas | Paginación offset (`page`, `page_size`) con `total` y `pages` en **todos** los endpoints de listado, incluidas categorías. Ver [TRD TD-002](TRD.md#2-decisiones-técnicas). |
| 3 | Menú sándwich en mobile | Navigation drawer accesible por debajo de 840 px; en desktop la navegación pasa al header. Ver [UX-UI §4.5](UX-UI.md#45-menú-sándwich-navigation-drawer). |
| 4 | Screaming Architecture | Carpetas por dominio en back y front: `identidad/`, `catalogo/`, `aportes/`, `validacion/`, `roadmap/`. Ver [TRD §3.2](TRD.md#32-estructura-de-carpetas-la-que-se-va-a-crear-en-la-instancia-b). |
| 5 | Apariencia inspirada en Google | Tokens concretos de la paleta Google (azul `#1a73e8`, grises `#202124`/`#5f6368`), Roboto, Material Symbols, radios y elevaciones Material 3. Ver [UX-UI §2](UX-UI.md#2-design-tokens). |

## 8. Vacíos de la SPEC de clase y decisiones tomadas

| # | Vacío detectado en la SPEC | Opciones consideradas | Decisión | Dónde se desarrolla |
|---|----------------------------|-----------------------|----------|---------------------|
| 1 | ¿Quién valida los cursos aportados? | auto-moderación / validación por docente-moderador / votación comunitaria | Un rol `admin` (moderador) aprueba o rechaza. La votación necesita masa crítica de usuarios que el MVP no tiene. | [PRD BR-001/BR-003](PRD.md#7-reglas-de-negocio) · [TRD TD-005](TRD.md#2-decisiones-técnicas) |
| 2 | ¿Hay roles? | sin roles / `usuario` + `admin` / roles granulares | Dos roles: `usuario` y `admin`. El primer admin se crea por seed con variables de entorno. | [PRD §3](PRD.md#3-personas) · [BackendSchema §1.2](BackendSchema.md#12-tablas) |
| 3 | ¿Qué es exactamente "incluir en mi catálogo"? | catálogo personal separado del roadmap / ítem del roadmap | Es agregar el curso al **roadmap personal**, como ítem con orden y estado (pendiente / en curso / completado). | [PRD US-009/US-010](PRD.md#4-user-stories) · [TRD TD-004](TRD.md#2-decisiones-técnicas) |
| 4 | ¿La búsqueda es por texto, filtro o ambos? | solo filtro / solo texto / ambos | Ambos: filtro por categoría + texto libre sobre título, tema, plataforma y docentes. | [PRD US-001](PRD.md#4-user-stories) · [BackendSchema §3.2](BackendSchema.md#32-catálogo-cursos-y-categorías) |
| 5 | ¿Qué estados tiene un aporte? | con borrador / sin borrador | `en_revision` → `publicado` o `rechazado`. Sin borradores: el formulario se envía completo. | [BackendSchema §2](BackendSchema.md#2-estados-del-ciclo-de-vida-del-curso) |
| 6 | ¿Qué pasa con un aporte rechazado? | se borra / queda visible para el autor / se puede reenviar | Queda visible para su autor con el motivo. Editar y reenviar es P1. La URL se libera para un nuevo aporte. | [PRD US-007/US-012](PRD.md#4-user-stories) |
| 7 | ¿Cómo se evita cargar el mismo curso dos veces? | sin control / por título / por URL | Por URL normalizada (minúsculas en esquema y host, sin barra final ni parámetros `utm_*`). | [PRD BR-005](PRD.md#7-reglas-de-negocio) · [BackendSchema §4](BackendSchema.md#4-decisiones-del-esquema) |
| 8 | "¿Lo avala una organización?" ¿solo sí/no? | booleano / booleano + nombre | Booleano + nombre de la organización, obligatorio si el aval es "sí". | [BackendSchema §1.2](BackendSchema.md#12-tablas) |
| 9 | ¿Cómo se modelan los docentes o disertantes? | entidad propia N:M / texto libre | Texto libre (hasta 300 caracteres, separados por coma). Una entidad `docente` queda fuera del MVP. | [BackendSchema §4](BackendSchema.md#4-decisiones-del-esquema) |
| 10 | ¿Cómo llega el enlace de recuperación de contraseña en desarrollo? | log del backend / servicio SMTP real / SMTP de prueba | SMTP de prueba **Mailpit** dentro del compose (bandeja web en `localhost:8025`). Token de un solo uso, 30 minutos. | [TRD TD-007](TRD.md#2-decisiones-técnicas) · [APPFlow Flujo 5](APPFlow.md#flujo-5--recuperar-la-contraseña) |
| 11 | ¿Qué límite concreto tiene el rate limiting? | por IP / por cuenta / ambos | 5 intentos por minuto por IP en `POST /auth/login` y 3 cada 15 minutos por IP en la solicitud de recuperación → `429` con `Retry-After`. | [TRD TD-006](TRD.md#2-decisiones-técnicas) |
| 12 | ¿bcrypt u otro algoritmo? | bcrypt / argon2id / scrypt | bcrypt con costo 12 (mínimo exigido, librería madura); argon2id evaluado y descartado para el MVP. | [TRD TD-003](TRD.md#2-decisiones-técnicas) |
| 13 | ¿Hay datos extra del curso? ("y demás datos necesarios" del borrador) | ninguno / plataforma / duración, idioma, nivel | Se agrega **plataforma o proveedor** (obligatorio). Duración, idioma y nivel quedan fuera. | [BackendSchema §1.2](BackendSchema.md#12-tablas) |
| 14 | ¿Logout? | endpoint de logout con lista negra / logout en el cliente | Logout en el cliente (se descarta el token); el token vence a los 60 minutos. | [TRD TD-001](TRD.md#2-decisiones-técnicas) |

## 9. Historia de la SPEC (autoregistro de cambios)

| Fecha | Cambio | Por qué |
|-------|--------|---------|
| 20/10/2026 | SPEC de clase redactada en el pizarrón del aula | — |
| 21/10/2026 | La cátedra publica la SPEC oficial corregida (FastAPI ref. 0.158.2 en lugar de 0.143.3 del borrador) | formalización por correo |
| 23/10/2026 | Primer commit del repo: SPEC oficial tal cual | regla de la consigna §4.3 |
| 23/10/2026 | Refinamiento: identidad (Senda), alcance dentro/fuera, reglas clave, stack con versiones, §8 con 14 decisiones sobre vacíos | resolver ambigüedades antes de construir |
