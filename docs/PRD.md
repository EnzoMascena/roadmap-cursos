# PRD — Product Requirements Document — Senda

> **Qué es:** el QUÉ y el POR QUÉ de Senda: para quién, qué problema resuelve, qué hace y qué
> **no** hace. La tecnología está en el [TRD](TRD.md); las pantallas, en el [APPFlow](APPFlow.md).

## 1. Resumen ejecutivo

Senda es una webapp donde una comunidad de estudiantes arma, entre todos, un catálogo de cursos
gratuitos de cualquier plataforma. Cada usuario aporta cursos con datos estructurados (categoría,
docentes, si da certificado, si exige examen, si lo avala una organización) y declara si lo tomó;
un administrador valida cada aporte antes de publicarlo. Sobre ese catálogo validado, cada usuario
arma su **roadmap personal** y marca su avance curso por curso.

## 2. Objetivos y métricas de éxito

| Objetivo | Cómo sabemos que lo logramos |
|----------|------------------------------|
| Catálogo comunitario confiable y variado | ≥ 70 % de los aportes terminan `publicado`; el catálogo tiene cursos en ≥ 6 de las 10 categorías; ningún curso publicado duplicado por URL |
| Moderación ágil | mediana de tiempo entre aporte y validación < 48 h (fecha de alta vs `validado_en`) |
| El roadmap se usa para planificar | ≥ 50 % de los usuarios registrados tiene al menos 3 cursos en su roadmap; ≥ 1 ítem pasa a `completado` por usuario activo por mes |
| Aportes con información honesta | 100 % de los aportes tiene la declaración de toma respondida (regla del sistema); % de cursos aportados por alguien que lo tomó, visible en métricas internas |

> Las métricas se calculan con consultas sobre la base (`cursos`, `roadmap_items`): el MVP no
> incluye herramientas de analítica.

## 3. Personas

### Persona 1 — Lucía, estudiante que busca (rol `usuario`)

- **Contexto:** 20 años, cursa 2.º año de Ingeniería en Sistemas. Usa el celular para casi todo
  y la notebook para estudiar.
- **Motivaciones:** complementar la facultad con cursos gratuitos que den certificado para el CV;
  tener un plan claro en vez de 30 pestañas abiertas.
- **Frustraciones hoy:** encuentra cursos en grupos de WhatsApp que después no encuentra; no sabe
  si un curso pide examen o da certificado hasta que se anota; abandona porque no ve su progreso.
- **Historias tipo:** "Quiero ver cursos de bases de datos que den certificado." · "Quiero
  armar mi ruta para el verano y tachar lo que voy terminando."

### Persona 2 — Martín, el que ya hizo los cursos (rol `usuario`, aportante)

- **Contexto:** 25 años, trabaja como developer junior y estudia; hizo muchos cursos online y es
  quien recomienda cursos en los grupos de la facultad.
- **Motivaciones:** compartir lo que le sirvió en un lugar ordenado, con su opinión implícita de
  "yo lo hice".
- **Frustraciones hoy:** sus recomendaciones se pierden en el chat; le preguntan siempre lo mismo.
- **Historias tipo:** "Hice este curso de Docker y quiero que quede para los que vienen." ·
  "Quiero saber si mi aporte ya está publicado o por qué me lo rechazaron."

### Persona 3 — Paula, moderadora de la comunidad (rol `admin`)

- **Contexto:** ayudante de cátedra; dedica unos minutos por día a revisar aportes.
- **Motivaciones:** que el catálogo tenga cursos reales, gratuitos y bien descriptos.
- **Frustraciones hoy:** no hay forma de filtrar recomendaciones de baja calidad ni links muertos.
- **Historias tipo:** "Quiero ver los aportes pendientes del más viejo al más nuevo." · "Si
  rechazo un aporte, quiero explicarle el motivo a quien lo cargó."

## 4. User stories

> **P0** = el MVP no funciona sin esto (se entrega el lunes 26/10). **P1** = siguiente iteración.
> Los criterios son verificables desde la UI con los datos de seed del [README](../README.md).

| ID | Prioridad | Historia | Criterios de aceptación |
|----|-----------|----------|-------------------------|
| US-001 | P0 | Como **visitante**, quiero ver el catálogo comunitario paginado y filtrarlo por categoría o buscar por texto, para descubrir cursos sin registrarme | - [ ] Dado que visito `/catalogo`, veo la primera página con hasta 12 cursos `publicado`, del más reciente al más antiguo<br>- [ ] Dado que hay más de 12 cursos, aparece el paginador y al cambiar de página la URL refleja `?page=N`<br>- [ ] Dado que elijo una categoría o escribo un texto (2 a 100 caracteres), veo solo los cursos que coinciden y la página vuelve a 1<br>- [ ] Dado que no hay resultados, veo un empty state con CTA "Aportá un curso"<br>- [ ] Nunca veo cursos `en_revision` ni `rechazado` |
| US-002 | P0 | Como **visitante**, quiero ver el detalle de un curso, para decidir si me sirve antes de ir a la plataforma | - [ ] Dado que entro a `/catalogo/:id` de un curso publicado, veo título, plataforma, categoría, tema, versión, año, docentes, cuestionarios, examen, certificado, aval (con organización) y si el aportante lo tomó<br>- [ ] El botón "Ir al curso" abre la URL externa en una pestaña nueva<br>- [ ] Dado un id inexistente o no publicado, veo la pantalla "Curso no encontrado" |
| US-003 | P0 | Como **visitante**, quiero registrarme con nombre, email y contraseña, para aportar cursos y tener mi roadmap | - [ ] Dado datos válidos (nombre 2 a 80, email válido, contraseña de 8 a 64 caracteres con al menos una letra y un número), se crea la cuenta y paso a `/login` con el aviso "Cuenta creada"<br>- [ ] Dado un email ya registrado, veo el error en el campo email<br>- [ ] La contraseña nunca se guarda en claro (bcrypt) |
| US-004 | P0 | Como **usuario**, quiero iniciar y cerrar sesión de forma segura, para acceder a mis funciones | - [ ] Dado credenciales válidas, ingreso y vuelvo a la ruta que quería visitar (o a `/catalogo`)<br>- [ ] Dado credenciales inválidas, veo "Email o contraseña incorrectos" sin revelar cuál falló<br>- [ ] Dado más de 5 intentos en un minuto desde la misma IP, veo "Demasiados intentos, probá en N segundos" (HTTP 429)<br>- [ ] Dado que presiono "Salir", vuelvo a `/` y las rutas protegidas me piden login |
| US-005 | P0 | Como **usuario** que olvidó su contraseña, quiero recuperarla por mail, para no perder mi cuenta | - [ ] Dado que pido recuperación con un email, siempre veo el mismo mensaje ("Si el email existe, te enviamos un enlace"), exista o no<br>- [ ] Dado un email registrado, llega un mail (Mailpit, `localhost:8025`) con un enlace a `/recuperar/nueva?token=…`<br>- [ ] Dado el enlace dentro de los 30 minutos, defino una nueva contraseña y puedo ingresar con ella<br>- [ ] Dado un token vencido o ya usado, veo "El enlace venció o ya fue usado" y un CTA para pedir otro |
| US-006 | P0 | Como **usuario**, quiero aportar un curso gratuito con todos sus datos y declarar si lo tomé, para enriquecer el catálogo | - [ ] El formulario pide: URL, plataforma, categoría (lista), tema, título, versión, año de edición, docentes, cuestionarios, examen, certificado, aval (+ organización si es "sí") y "¿Lo tomaste?" (sí/no, sin opción preseleccionada)<br>- [ ] Dado un campo inválido, veo el error junto al campo y no pierdo lo cargado<br>- [ ] Dado una URL ya en revisión o publicada, veo "Este curso ya fue aportado"<br>- [ ] Dado un envío válido, veo "Aporte enviado a revisión" y llego al detalle de mi aporte con estado `en_revision` |
| US-007 | P0 | Como **usuario**, quiero ver mis aportes con su estado, para saber si fueron publicados o por qué se rechazaron | - [ ] Dado que entro a `/mis-aportes`, veo mis aportes paginados (12 por página) con chip de estado, del más nuevo al más viejo<br>- [ ] Puedo filtrar por estado<br>- [ ] Dado un aporte `rechazado`, en su detalle veo el motivo del rechazo<br>- [ ] No puedo ver aportes `en_revision` ni `rechazado` de otros usuarios (403) |
| US-008 | P0 | Como **admin**, quiero revisar los aportes pendientes y aprobarlos o rechazarlos con motivo, para mantener la calidad del catálogo | - [ ] Dado que entro a `/validacion`, veo los aportes `en_revision` paginados, del más antiguo al más nuevo<br>- [ ] Dado que apruebo, el curso pasa a `publicado` y aparece en `/catalogo`<br>- [ ] Dado que rechazo, debo escribir un motivo de 10 a 500 caracteres; el curso pasa a `rechazado`<br>- [ ] Dado un usuario sin rol admin, `/validacion` no es accesible (403 en la API, aviso y redirección en la UI) |
| US-009 | P0 | Como **usuario**, quiero agregar un curso del catálogo a mi roadmap, para planificar mi aprendizaje | - [ ] Dado un curso publicado, el botón "Agregar a mi roadmap" lo suma al final de mi roadmap con estado `pendiente`<br>- [ ] Dado que ya está en mi roadmap, la card y el detalle lo indican ("En tu roadmap") y no lo puedo agregar de nuevo<br>- [ ] Dado que no tengo sesión, el botón me lleva a `/login` y al volver puedo agregarlo |
| US-010 | P0 | Como **usuario**, quiero gestionar mi roadmap, para registrar mi avance | - [ ] Dado que entro a `/roadmap`, veo mis cursos paginados (12 por página) en orden, con su estado<br>- [ ] Puedo cambiar el estado a `pendiente`, `en_curso` o `completado` y el cambio persiste al recargar<br>- [ ] Puedo quitar un curso con confirmación<br>- [ ] Puedo filtrar por estado<br>- [ ] Dado un roadmap vacío, veo un empty state con CTA "Explorar el catálogo" |
| US-011 | P1 | Como **usuario**, quiero reordenar los cursos de mi roadmap, para reflejar en qué orden los voy a hacer | - [ ] Cada ítem tiene "Subir" y "Bajar"; el nuevo orden persiste<br>- [ ] El primero no puede subir y el último no puede bajar |
| US-012 | P1 | Como **usuario**, quiero corregir y reenviar un aporte rechazado, para no cargarlo de cero | - [ ] Dado un aporte `rechazado` propio, puedo editarlo y reenviarlo; vuelve a `en_revision` y se limpia el motivo<br>- [ ] No puedo editar aportes `en_revision` ni `publicado` (409) |

## 5. Requisitos funcionales

| ID | Requisito | Historia relacionada |
|----|-----------|----------------------|
| RF-001 | Listar cursos `publicado` paginados, filtrables por categoría y por texto (título, tema, plataforma, docentes) | US-001 |
| RF-002 | Mostrar el detalle completo de un curso publicado, incluida la declaración de toma | US-002 |
| RF-003 | Registrar usuarios con nombre, email único y contraseña hasheada con bcrypt | US-003 |
| RF-004 | Autenticar con email y contraseña y emitir un token de acceso con vencimiento | US-004 |
| RF-005 | Limitar los intentos de login por IP (rate limiting) | US-004 |
| RF-006 | Solicitar recuperación de contraseña, enviar un enlace con token de un solo uso y permitir definir una contraseña nueva | US-005 |
| RF-007 | Registrar aportes de cursos con todos los metadatos de la SPEC, plataforma y declaración de toma, en estado `en_revision` | US-006 |
| RF-008 | Rechazar aportes con URL duplicada entre cursos `en_revision` y `publicado` | US-006 |
| RF-009 | Listar los aportes propios paginados y con filtro por estado, y ver el detalle de cada uno | US-007 |
| RF-010 | Listar aportes pendientes y registrar la decisión de validación (aprobar / rechazar con motivo) solo para `admin` | US-008 |
| RF-011 | Agregar un curso publicado al roadmap del usuario, sin duplicados | US-009 |
| RF-012 | Listar el roadmap paginado, cambiar el estado de un ítem y quitarlo | US-010 |
| RF-013 | Indicar en catálogo y detalle si un curso ya está en el roadmap del usuario autenticado | US-009 |
| RF-014 | Reordenar ítems del roadmap (P1) | US-011 |
| RF-015 | Editar y reenviar un aporte rechazado (P1) | US-012 |

## 6. Requisitos no funcionales

| ID | Requisito | Notas |
|----|-----------|-------|
| RNF-001 | Todos los listados paginados (API y pantallas), `page_size` por defecto 12 y máximo 100 | heredado de SPEC clase |
| RNF-002 | Mobile-first con mejora progresiva: usable desde 360 px de ancho | heredado de SPEC clase |
| RNF-003 | Menú sándwich por debajo de 840 px | heredado de SPEC clase |
| RNF-004 | Contraseñas con bcrypt (costo 12); nunca se loggean ni se devuelven | heredado de SPEC clase |
| RNF-005 | Rate limiting en login: 5 intentos/min por IP | heredado de SPEC clase; valor: decisión propia |
| RNF-006 | Accesibilidad WCAG 2.1 AA en contraste, foco visible y navegación por teclado | decisión propia, ver [UX-UI §6](UX-UI.md#6-accesibilidad-mínima-no-negociable) |
| RNF-007 | El catálogo responde en < 500 ms (p95) con 1.000 cursos publicados en el entorno local | decisión propia; índices en [BackendSchema §1.2](BackendSchema.md#12-tablas) |
| RNF-008 | Todo el entorno levanta con un solo `docker compose up` en una máquina limpia | consigna Instancia B |
| RNF-009 | Interfaz en español rioplatense neutro (vos), mensajes de error comprensibles | decisión propia |

## 7. Reglas de negocio

| ID | Regla | Fuente |
|----|-------|--------|
| BR-001 | Un curso aportado no aparece en el catálogo comunitario hasta ser validado (`publicado`) | SPEC clase |
| BR-002 | Quien aporta un curso declara obligatoriamente si lo tomó o no; la respuesta se muestra en el detalle | SPEC clase |
| BR-003 | Solo el rol `admin` valida aportes; rechazar exige un motivo de 10 a 500 caracteres | decisión propia |
| BR-004 | El roadmap es personal y privado: nadie ve ni modifica el roadmap de otro usuario | decisión propia |
| BR-005 | Una URL normalizada no puede repetirse entre cursos `en_revision` y `publicado`; un rechazo libera la URL | decisión propia |
| BR-006 | Solo cursos `publicado` pueden agregarse al roadmap; un curso no puede estar dos veces en el mismo roadmap | decisión propia |
| BR-007 | Un curso nuevo en el roadmap entra al final, con estado `pendiente` | decisión propia |
| BR-008 | Si el aval es "sí", el nombre de la organización es obligatorio; si es "no", se descarta | decisión propia |
| BR-009 | El año de edición va de 1990 al año actual | decisión propia |
| BR-010 | Solo cursos gratuitos: el formulario lo declara y el admin rechaza cursos pagos | SPEC clase ("cursos gratuitos") |

## 8. Fuera de alcance (out of scope)

- Cursos pagos, pagos, suscripciones y cualquier integración con medios de pago.
- Certificados emitidos por Senda.
- Login social, 2FA y verificación de email al registrarse.
- Comentarios, calificaciones, reseñas, likes, seguidores o perfiles públicos.
- Roadmaps públicos, compartibles o plantillas de roadmap.
- Verificación automática de que una URL siga activa (scraping o chequeos periódicos).
- Edición o despublicación de cursos publicados; ABM de categorías; gestión de usuarios y roles
  desde la UI (el admin se crea por seed).
- Notificaciones por mail fuera de la recuperación de contraseña.
- App móvil nativa, PWA/offline e internacionalización.
- Despliegue productivo; el alcance es el entorno de desarrollo con Docker Compose.

## 9. Supuestos y decisiones sobre la SPEC de clase

- **Validación por moderador (`admin`)** en lugar de votación comunitaria: el MVP arranca sin masa
  crítica de usuarios. → [SPEC §8 #1](SPEC.md#8-vacíos-de-la-spec-de-clase-y-decisiones-tomadas)
- **"Incluir en su catálogo" = agregar al roadmap personal.** No existe un "catálogo personal"
  separado: el roadmap cumple ese rol y además registra el avance. → [SPEC §8 #3](SPEC.md#8-vacíos-de-la-spec-de-clase-y-decisiones-tomadas)
- **Se agrega el campo plataforma/proveedor** ("y demás datos necesarios" del borrador de clase):
  es lo primero que un estudiante quiere saber de un curso. → [SPEC §8 #13](SPEC.md#8-vacíos-de-la-spec-de-clase-y-decisiones-tomadas)
- **Supuesto:** la gratuidad la declara el aportante y la controla el admin; el sistema no puede
  verificarla automáticamente.
- **Supuesto:** el volumen del MVP es chico (cientos de cursos, decenas de usuarios); no se
  necesita búsqueda full-text dedicada.

## 10. Preguntas abiertas

| Pregunta | Impacto | Estado |
|----------|---------|--------|
| ¿Los aportes expiran si nadie los valida? | medio | decidida: no expiran en el MVP; el panel ordena del más antiguo al más nuevo para que no queden olvidados |
| ¿Mostramos en el catálogo cuántos usuarios tienen el curso en su roadmap? | bajo | abierta → candidata a P2 (no compromete el modelo: se obtiene con un `COUNT` sobre `roadmap_items`) |
| ¿Puede un admin validar su propio aporte? | bajo | decidida: sí en el MVP (hay un solo admin por seed); con más moderadores se agregaría la restricción |
| ¿Qué pasa con los roadmaps si un curso se despublica? | medio | decidida: despublicar está fuera de alcance; si se agrega, los ítems quedarían marcados como "no disponible" |

---

**Referencias:**
- Atlassian — Plantilla PRD: https://www.atlassian.com/software/confluence/templates/product-requirements
- Lenny Rachitsky — Plantilla de requirements: https://www.atlassian.com/software/confluence/templates/requirements
