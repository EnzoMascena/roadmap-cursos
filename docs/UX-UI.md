# UX-UI — Guía visual de estilos — Senda

> **Qué es:** la gramática visual de Senda: tokens, componentes, estados y accesibilidad. Es el
> conjunto de reglas con el que se construye cada pantalla **antes** de escribir CSS. Qué pantallas
> existen y cómo se navega está en el [APPFlow](APPFlow.md).
> **Inspiración fijada por la SPEC:** Google / Material 3 — limpieza, espacio en blanco, azul
> primario de Google, sombras sutiles, radios amplios y componentes con estados definidos.
> Los valores salen de la paleta de productos Google y de las especificaciones de Material 3,
> adaptados a Senda.

## 1. Principios

1. **El curso es el protagonista.** Cada pantalla responde una pregunta sobre cursos (¿cuál me
   sirve?, ¿en qué estado está?, ¿qué sigue en mi ruta?). Lo que no ayuda a responderla, sobra.
2. **Blanco primero, color con intención.** Fondo blanco como Google Search; el azul `#1a73e8`
   se reserva para la acción principal de cada pantalla y el color semántico solo para estados.
3. **Mobile primero, se mejora hacia arriba.** El layout base se diseña para 360 px y las media
   queries solo agregan columnas o navegación; nunca reparan la base.
4. **Ningún estado sin diseñar.** Cargando, vacío, error, deshabilitado y "sin permiso" están
   definidos acá antes de programar.
5. **Accesible por defecto.** Contraste AA medido, foco siempre visible y todo operable con teclado.

## 2. Design tokens

### 2.1 Paleta de colores

Ratios calculados con la fórmula de luminancia relativa de WCAG 2.1 (los mismos que da
https://webaim.org/resources/contrastchecker/).

| Token | Valor | Uso | Contraste AA |
|-------|-------|-----|--------------|
| `--color-primary` | `#1a73e8` | botón primario (relleno), anillo de foco, ítem activo, iconos activos | blanco sobre primario: 4.51:1 ✓ (texto 14 px 500) |
| `--color-primary-hover` | `#1967d2` | hover del botón primario | — |
| `--color-primary-pressed` | `#185abc` | estado `active` del botón primario | — |
| `--color-on-primary` | `#ffffff` | texto e iconos sobre primario | 4.51:1 ✓ |
| `--color-primary-container` | `#e8f0fe` | chip seleccionado, ítem activo del drawer, chip "en curso" | — |
| `--color-on-primary-container` | `#174ea6` | texto sobre `primary-container` | 6.85:1 ✓ |
| `--color-link` | `#1967d2` | links y botones de texto (más oscuro que el primario para tener margen de contraste) | vs blanco 5.37:1 ✓ · vs `#f8f9fa` 5.09:1 ✓ |
| `--color-background` | `#ffffff` | fondo de página | — |
| `--color-surface` | `#ffffff` | cards, header, drawer, diálogos | — |
| `--color-surface-variant` | `#f8f9fa` | barra de filtros, pie, fondo de skeleton | — |
| `--color-surface-hover` | `#f1f3f4` | hover de filas, ítems y botones de texto | — |
| `--color-text` | `#202124` | texto principal | vs blanco 16.1:1 ✓ |
| `--color-text-muted` | `#5f6368` | metadatos, ayudas de campo, texto secundario | vs blanco 6.05:1 ✓ · vs `#f1f3f4` 5.44:1 ✓ |
| `--color-outline` | `#80868b` | borde de inputs, checkboxes y radios (componentes interactivos) | vs blanco 3.68:1 ✓ (≥ 3:1 no-texto) |
| `--color-outline-variant` | `#dadce0` | divisores y bordes decorativos de cards | decorativo (1.37:1, no transmite información) |
| `--color-success` / `--color-success-container` / `--color-on-success-container` | `#188038` / `#e6f4ea` / `#137333` | snackbar de éxito, chips "publicado" y "completado" | `#137333` sobre `#e6f4ea`: 5.24:1 ✓ |
| `--color-warning` / `--color-warning-container` / `--color-on-warning-container` | `#f9ab00` / `#fef7e0` / `#a05800` | chip "en revisión", avisos (el amarillo puro solo en iconos y bordes) | `#a05800` sobre `#fef7e0`: 5.04:1 ✓ |
| `--color-error` / `--color-error-container` / `--color-on-error-container` | `#d93025` / `#fce8e6` / `#c5221f` | errores de validación, botón peligroso, chip "rechazado" | `#d93025` vs blanco 4.77:1 ✓ · `#c5221f` sobre `#fce8e6`: 4.92:1 ✓ |
| `--color-neutral-container` / `--color-on-neutral-container` | `#f1f3f4` / `#3c4043` | chip "pendiente" | 9.4:1 ✓ |
| `--color-inverse-surface` / `--color-on-inverse-surface` / `--color-inverse-primary` | `#3c4043` / `#ffffff` / `#8ab4f8` | snackbar y su acción | blanco 10.47:1 ✓ · `#8ab4f8` 4.97:1 ✓ |
| `--color-scrim` | `rgba(32, 33, 36, .6)` | fondo detrás de drawer y diálogos | — |

> Decisión respecto del primario: `#1a73e8` sobre `#f8f9fa` da 4.27:1 (no llega a AA), por eso
> el texto azul usa `--color-link` (`#1967d2`) y el fondo de página es blanco.

### 2.2 Tipografía

Escala tipográfica de Material 3 con **Roboto** (Google Fonts, `font-display: swap`).

| Token | Familia | Tamaño / line-height / peso | Uso |
|-------|---------|-----------------------------|-----|
| `--font-family-base` | `"Roboto", system-ui, -apple-system, "Segoe UI", sans-serif` | — | toda la interfaz |
| `--font-family-mono` | `"Roboto Mono", ui-monospace, monospace` | — | URLs en el formulario y el detalle |
| `--text-label-sm` | base | 12px / 16px / 500 | chips, badges, contador del paginador |
| `--text-label` | base | 14px / 20px / 500, `letter-spacing: .1px` | botones, labels de campos, ítems del drawer |
| `--text-body-sm` | base | 14px / 20px / 400 | metadatos de cards, ayudas y errores de campo |
| `--text-body` | base | 16px / 24px / 400 | párrafos, inputs |
| `--text-title` | base | 16px / 24px / 500 | título de card y de ítem de roadmap |
| `--text-title-lg` | base | 22px / 28px / 400 | títulos de pantalla en mobile |
| `--text-headline` | base | 28px / 36px / 400 | títulos de pantalla ≥ 840 px, hero de Home |

### 2.3 Espaciado, radios, sombras, z-index y movimiento

| Token | Valor | Uso |
|-------|-------|-----|
| `--space-1` … `--space-8` | 4, 8, 12, 16, 24, 32, 48, 64 px | ritmo de 4 px; gutter de grilla `--space-4` |
| `--radius-xs` | 4px | campos de texto y selects (outlined de Material 3) |
| `--radius-sm` | 8px | chips, snackbar |
| `--radius-md` | 12px | cards de curso, ítems de roadmap |
| `--radius-lg` | 16px | panel del drawer (lado derecho), contenedor de filtros |
| `--radius-xl` | 28px | diálogos |
| `--radius-full` | 9999px | botones (pill), icon buttons, paginador |
| `--shadow-1` | `0 1px 2px rgba(60, 64, 67, .3), 0 1px 3px 1px rgba(60, 64, 67, .15)` | cards en reposo, header al hacer scroll |
| `--shadow-2` | `0 1px 2px rgba(60, 64, 67, .3), 0 2px 6px 2px rgba(60, 64, 67, .15)` | hover de card, botón primario en hover |
| `--shadow-3` | `0 4px 8px 3px rgba(60, 64, 67, .15), 0 1px 3px rgba(60, 64, 67, .3)` | drawer abierto, diálogos, snackbar |
| `--z-header` / `--z-drawer` / `--z-dialog` / `--z-snackbar` | 100 / 200 / 300 / 400 | orden de capas |
| `--motion-fast` / `--motion-medium` | 150ms / 250ms, `cubic-bezier(.2, 0, 0, 1)` | hover y foco / drawer y diálogos |
| `--container-max` | 1200px | ancho máximo del contenido |
| `--header-height` | 64px | alto del header |

### 2.4 Bloque de variables listo para copiar

```css
:root {
  /* Color */
  --color-primary: #1a73e8;
  --color-primary-hover: #1967d2;
  --color-primary-pressed: #185abc;
  --color-on-primary: #ffffff;
  --color-primary-container: #e8f0fe;
  --color-on-primary-container: #174ea6;
  --color-link: #1967d2;
  --color-background: #ffffff;
  --color-surface: #ffffff;
  --color-surface-variant: #f8f9fa;
  --color-surface-hover: #f1f3f4;
  --color-text: #202124;
  --color-text-muted: #5f6368;
  --color-outline: #80868b;
  --color-outline-variant: #dadce0;
  --color-success: #188038;
  --color-success-container: #e6f4ea;
  --color-on-success-container: #137333;
  --color-warning: #f9ab00;
  --color-warning-container: #fef7e0;
  --color-on-warning-container: #a05800;
  --color-error: #d93025;
  --color-error-container: #fce8e6;
  --color-on-error-container: #c5221f;
  --color-neutral-container: #f1f3f4;
  --color-on-neutral-container: #3c4043;
  --color-inverse-surface: #3c4043;
  --color-on-inverse-surface: #ffffff;
  --color-inverse-primary: #8ab4f8;
  --color-scrim: rgba(32, 33, 36, .6);

  /* Tipografía */
  --font-family-base: "Roboto", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-family-mono: "Roboto Mono", ui-monospace, monospace;
  --text-label-sm: 500 0.75rem/1rem var(--font-family-base);
  --text-label: 500 0.875rem/1.25rem var(--font-family-base);
  --text-body-sm: 400 0.875rem/1.25rem var(--font-family-base);
  --text-body: 400 1rem/1.5rem var(--font-family-base);
  --text-title: 500 1rem/1.5rem var(--font-family-base);
  --text-title-lg: 400 1.375rem/1.75rem var(--font-family-base);
  --text-headline: 400 1.75rem/2.25rem var(--font-family-base);

  /* Espaciado */
  --space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 16px;
  --space-5: 24px; --space-6: 32px; --space-7: 48px; --space-8: 64px;

  /* Forma y elevación */
  --radius-xs: 4px;  --radius-sm: 8px;  --radius-md: 12px;
  --radius-lg: 16px; --radius-xl: 28px; --radius-full: 9999px;
  --shadow-1: 0 1px 2px rgba(60, 64, 67, .3), 0 1px 3px 1px rgba(60, 64, 67, .15);
  --shadow-2: 0 1px 2px rgba(60, 64, 67, .3), 0 2px 6px 2px rgba(60, 64, 67, .15);
  --shadow-3: 0 4px 8px 3px rgba(60, 64, 67, .15), 0 1px 3px rgba(60, 64, 67, .3);

  /* Capas, movimiento y layout */
  --z-header: 100; --z-drawer: 200; --z-dialog: 300; --z-snackbar: 400;
  --motion-fast: 150ms cubic-bezier(.2, 0, 0, 1);
  --motion-medium: 250ms cubic-bezier(.2, 0, 0, 1);
  --container-max: 1200px;
  --header-height: 64px;
}

@media (prefers-reduced-motion: reduce) {
  :root { --motion-fast: 0ms linear; --motion-medium: 0ms linear; }
}
```

> `prefers-reduced-motion` es una preferencia del usuario, no un breakpoint de tamaño: no
> contradice la regla mobile-first.

## 3. Estrategia mobile-first con mejora progresiva

> Regla de la SPEC: la base **no** usa media queries; `@media (min-width: …)` solo agrega o mejora.
> Se usan los breakpoints de Material 3 (compact < 600 · medium 600–839 · expanded ≥ 840) y
> **solo** dos media queries de ancho en todo el proyecto.

| Capa | Dónde aplica | Qué define |
|------|--------------|------------|
| **Base (sin media queries)** | todos los viewports, diseñada a 360 px | 1 columna; header con hamburguesa + logo + acción de sesión; drawer como navegación; grilla de cards apiladas; listados como cards (no tablas); filtros en un bloque plegable "Filtros"; formularios a ancho completo; botones de acción principal a ancho completo; padding lateral `--space-4`; títulos `--text-title-lg`; áreas táctiles ≥ 48 px en ítems de lista y de navegación |
| `@media (min-width: 600px)` | tablet / ventanas medianas | grilla de cursos de 2 columnas; filtros siempre visibles en una fila (búsqueda + select de categoría); formularios a 2 columnas para campos cortos (versión / año, plataforma / categoría); botones de acción al ancho de su contenido, alineados a la derecha; padding lateral `--space-5` |
| `@media (min-width: 840px)` | desktop | navegación horizontal en el header y hamburguesa oculta; grilla de 3 columnas; "Mis aportes" y "Pendientes de validación" como tabla real; contenedor centrado `max-width: var(--container-max)`; detalle de curso a 2 columnas (datos + panel de acciones fijo); títulos `--text-headline` |

Regla de verificación: `grep -rn "@media" frontend/src` solo devuelve `min-width: 600px`,
`min-width: 840px` y `prefers-reduced-motion`. Nunca `max-width`.

## 4. Componentes (anatomía + estados)

> Por cada componente: anatomía, tokens y **todos** sus estados. El foco visible es igual en
> todos los interactivos: `outline: 2px solid var(--color-primary); outline-offset: 2px`, solo
> con `:focus-visible`.

### 4.1 Botón (primario / secundario / texto / peligro)

- **Anatomía común:** alto 40px, padding horizontal 24px (16px a la izquierda si lleva icono de
  18px), `--radius-full`, `--text-label`. En la base, el botón de acción principal de un
  formulario ocupa el ancho completo.
- **Primario (filled):** fondo `--color-primary`, texto `--color-on-primary`. Uno solo por pantalla.
- **Secundario (outlined):** borde 1px `--color-outline`, texto `--color-link`, fondo transparente.
- **Texto:** sin borde ni fondo, texto `--color-link`, padding 12px. Para acciones de baja jerarquía.
- **Peligro:** variante texto con `--color-error`; siempre pide confirmación en un diálogo (4.6).

| Estado | Primario | Secundario / texto |
|--------|----------|--------------------|
| `default` | como la anatomía | como la anatomía |
| `hover` | fondo `--color-primary-hover` + `--shadow-1` | fondo `--color-surface-hover` |
| `focus-visible` | anillo de foco común | anillo de foco común |
| `active` | fondo `--color-primary-pressed`, sin sombra | fondo `--color-primary-container` |
| `disabled` | fondo `rgba(32,33,36,.12)`, texto `rgba(32,33,36,.38)`, `cursor: not-allowed`, `aria-disabled="true"` | texto `rgba(32,33,36,.38)` |
| `loading` | spinner de 18px en lugar del icono, texto "Enviando…", deshabilitado y `aria-busy="true"` | igual |

- **Icon button:** 48×48 de área táctil, icono 24px `--color-text-muted`, `--radius-full`; hover
  `--color-surface-hover`; siempre con `aria-label`.

### 4.2 Campo de formulario (input / select / textarea)

- **Outlined de Material 3:** alto 56px, borde 1px `--color-outline`, `--radius-xs`, padding
  16px, texto `--text-body`. **Label siempre visible arriba del campo** (`--text-label`,
  `--color-text`); no se usa placeholder como label. Ayuda debajo en `--text-body-sm`
  `--color-text-muted`. Los obligatorios se marcan con " *" y el formulario lo aclara arriba.
- **Select:** mismo marco, icono `arrow_drop_down` a la derecha; es un `<select>` nativo (accesible
  y con buen comportamiento en mobile).
- **Textarea** (motivo de rechazo): alto mínimo 120px, contador "N/500" a la derecha de la ayuda.

| Estado | Visual |
|--------|--------|
| `default` | borde 1px `--color-outline` |
| `hover` | borde 1px `--color-text` |
| `focus` | borde 2px `--color-primary` (padding compensado 1px para que no salte el texto) |
| `filled` | igual a `default`, con valor en `--color-text` |
| `error` | borde 2px `--color-error`; mensaje debajo con icono `error` en `--color-error`, vinculado con `aria-describedby` y `aria-invalid="true"`; el foco va al primer campo con error al enviar |
| `disabled` | fondo `--color-surface-variant`, borde `--color-outline-variant`, texto `rgba(32,33,36,.38)` |

### 4.3 Card de curso

- **Anatomía:** superficie `--color-surface`, borde 1px `--color-outline-variant`, `--radius-md`,
  `--shadow-1`, padding `--space-4`, gap interno `--space-2`. Toda la card es un link al detalle
  (un único `<a>` que envuelve el título; el resto de la card extiende el área clickeable sin
  anidar elementos interactivos).
- **Contenido, de arriba hacia abajo:** chip de categoría (4.10) · título `--text-title` (máximo
  2 líneas con `line-clamp`) · plataforma y año en `--text-body-sm` `--color-text-muted` ·
  docentes (1 línea, con elipsis) · fila de badges con icono Material Symbols 18px + texto
  `--text-label-sm`: `quiz` Cuestionarios, `assignment` Examen, `workspace_premium` Certificado,
  `verified` Aval. Solo se muestran los que aplican.
- **Estados:**
  - `default`: como la anatomía.
  - `hover`: `--shadow-2`, título subrayado, `cursor: pointer`.
  - `focus-visible`: anillo de foco común sobre toda la card.
  - `en mi roadmap` (seleccionada): borde 2px `--color-primary` + badge `check_circle` "En tu roadmap"
    con `--color-primary-container` / `--color-on-primary-container` (dato `en_mi_roadmap` de la API).
  - `loading`: skeleton con la misma silueta (4.8).

### 4.4 Lista / tabla paginada y paginador

- **Base (< 840 px):** cada fila es una card apilada con la misma información que la tabla
  (título, plataforma, chip de estado, fecha, acción). Sin scroll horizontal.
- **≥ 840 px:** tabla real (`<table>` con `<caption>` visualmente oculto y `<th scope="col">`),
  filas de 52px, divisor 1px `--color-outline-variant`, hover `--color-surface-hover`.
- **Paginador estilo Google**, centrado debajo del listado:
  `‹ Anterior · 1 2 3 … 9 · Siguiente ›`. Cada número es un botón circular de 40px
  (`--radius-full`); la página actual con fondo `--color-primary-container`, texto
  `--color-on-primary-container` y `aria-current="page"`. En la base solo se ven
  `‹ · Página N de M · ›`; a partir de 600 px se ven los números (hasta 5 + extremos).
  Debajo, `--text-label-sm` `--color-text-muted`: "Mostrando 13–24 de 47".
- **Estados del listado:** `loading` (skeleton de 6 ítems) · `ok` · `empty` (4.8) ·
  `error` (banner con "Reintentar", 4.7) · página fuera de rango (empty state con
  "Volver a la página 1").
- La página, los filtros y la búsqueda viven en la URL (`?page=2&categoria=3&q=sql`) para que
  "Atrás" y los links compartidos funcionen.

### 4.5 Menú sándwich (navigation drawer)

- **Disparador:** icon button `menu` a la izquierda del header, visible por debajo de 840px,
  `aria-label="Abrir menú"`, `aria-expanded`, `aria-controls="menu-principal"`.
- **Panel:** `<nav id="menu-principal" aria-label="Principal">` modal, ancho
  `min(320px, 85vw)`, `--color-surface`, `--shadow-3`, esquinas derechas `--radius-lg`, entra
  desde la izquierda con `transform` y `--motion-medium`; detrás, `--color-scrim`.
- **Contenido:** encabezado con logo y botón `close` · ítems de 56px con icono 24px + `--text-label`:
  Inicio (`home`), Catálogo (`menu_book`), Aportar curso (`add_circle`), Mis aportes
  (`inventory_2`), Mi roadmap (`route`), Validación (`fact_check`, solo admin) · divisor ·
  bloque de sesión: "Ingresar" y "Crear cuenta", o el nombre del usuario y "Salir" (`logout`).
  Los ítems que requieren sesión llevan a login si no la hay.
- **Ítem activo:** fondo `--color-primary-container`, texto `--color-on-primary-container`,
  `aria-current="page"`, forma `--radius-full`.
- **Estados:** `cerrado` (`aria-expanded="false"`, panel con `inert`) · `abierto`
  (`aria-expanded="true"`, scroll del body bloqueado).
- **Cierre:** tocar un ítem, botón `close`, tecla `Esc`, click en el scrim.
- **Foco:** al abrir va al primer ítem y queda atrapado en el panel; al cerrar vuelve al botón
  hamburguesa.

### 4.6 Modal (diálogo)

- **Anatomía:** `<dialog>` nativo con `showModal()` (trae foco atrapado y `Esc`), ancho
  `min(560px, 100vw - 32px)`, `--radius-xl`, padding `--space-5`, `--shadow-3`, scrim
  `--color-scrim`. Título `--text-title-lg`, texto `--text-body` `--color-text-muted`, acciones
  alineadas a la derecha: botón de texto "Cancelar" + acción principal.
- **Usos:** confirmar "Quitar del roadmap" (acción peligro) y "Rechazar aporte" (con textarea de
  motivo obligatorio).
- **Estados:** `cerrado` · `abierto` · `enviando` (acción en `loading`, Cancelar deshabilitado) ·
  `error` (mensaje inline arriba de las acciones; el diálogo no se cierra).
- Al cerrar, el foco vuelve al botón que lo abrió.

### 4.7 Toast (snackbar) y banner de error

- **Snackbar:** fondo `--color-inverse-surface`, texto `--color-on-inverse-surface`
  `--text-body-sm`, `--radius-sm`, `--shadow-3`, padding 14px 16px, ancho mínimo 288px.
  Posición: abajo y centrado a 16px de los bordes (base); abajo a la izquierda desde 840 px.
  `role="status"` (éxito, info) o `role="alert"` (error). Uno a la vez; el nuevo reemplaza al anterior.
  - **Tipos:** éxito (icono `check_circle` en `--color-inverse-primary`), error (icono `error`),
    info. Duración: 4 s; 8 s si tiene acción ("Deshacer" al quitar del roadmap, "Reintentar" en
    errores de red). Se pausa con hover o foco.
- **Banner de error de pantalla:** cuando falla la carga de un listado o detalle, reemplaza al
  contenido: icono `cloud_off` 48px, título "No pudimos cargar los cursos", bajada con el motivo y
  botón secundario "Reintentar".

### 4.8 Skeleton y Empty state

- **Skeleton:** bloques `--color-surface-hover` con la silueta del contenido final (card, fila,
  detalle) y animación de pulso de opacidad (1 → .5) de 1.5 s; sin animación con
  `prefers-reduced-motion`. Contenedor con `aria-busy="true"` y texto oculto "Cargando…".
- **Empty state:** centrado, icono Material Symbols 64px `--color-text-muted`, título
  `--text-title`, bajada `--text-body-sm` y un CTA primario. Textos por pantalla:

  | Pantalla | Título | CTA |
  |----------|--------|-----|
  | Catálogo sin resultados | "No encontramos cursos con esos filtros" | "Limpiar filtros" · "Aportá un curso" |
  | Mi roadmap vacío | "Tu roadmap está vacío" | "Explorar el catálogo" |
  | Mis aportes vacío | "Todavía no aportaste cursos" | "Aportar el primero" |
  | Validación sin pendientes | "No hay aportes pendientes" | — (icono `task_alt`) |

### 4.9 Controles de selección (radio y checkbox)

- **Radio group** para "¿Tomaste este curso?" (sí / no): `<fieldset>` + `<legend>`, sin opción
  preseleccionada (BR-002); cada opción con área táctil de 48px; círculo 20px, borde 2px
  `--color-outline`; seleccionado: `--color-primary` con punto interno. Error: legend y mensaje
  en `--color-error`.
- **Checkbox** para cuestionarios, examen, certificado y aval: cuadro 18px, `--radius-xs` 2px,
  borde 2px `--color-outline`; marcado: fondo `--color-primary` con `check` blanco. Si "Lo avala
  una organización" se marca, aparece debajo el campo obligatorio "Organización".
- **Estados:** `default` · `hover` (halo 40px `--color-surface-hover`) · `focus-visible` (anillo
  común) · `checked` · `disabled` · `error`.

### 4.10 Chips (categoría, filtro y estado)

- **Chip de categoría** (en cards y detalle, no interactivo): alto 24px, `--radius-sm`,
  `--text-label-sm`, fondo `--color-surface-variant`, texto `--color-text-muted`.
- **Chips de filtro** (Home, accesos rápidos por categoría): alto 32px, borde 1px `--color-outline`,
  `--radius-sm`; seleccionado: fondo `--color-primary-container`, sin borde, icono `check` 18px.
- **Chip de estado** (con icono 16px, para no depender solo del color):

  | Estado | Fondo / texto | Icono | Texto |
  |--------|---------------|-------|-------|
  | `en_revision` | `--color-warning-container` / `--color-on-warning-container` | `schedule` | En revisión |
  | `publicado` | `--color-success-container` / `--color-on-success-container` | `check_circle` | Publicado |
  | `rechazado` | `--color-error-container` / `--color-on-error-container` | `cancel` | Rechazado |
  | `pendiente` | `--color-neutral-container` / `--color-on-neutral-container` | `radio_button_unchecked` | Pendiente |
  | `en_curso` | `--color-primary-container` / `--color-on-primary-container` | `play_circle` | En curso |
  | `completado` | `--color-success-container` / `--color-on-success-container` | `task_alt` | Completado |

### 4.11 Ítem de roadmap

- **Anatomía:** card horizontal, `--radius-md`, borde 1px `--color-outline-variant`, padding
  `--space-4`: número de orden en círculo de 32px (`--color-surface-variant`, `--text-label`) ·
  título (link al detalle) y plataforma · chip de estado · select "Estado" (pendiente / en curso /
  completado) · icon button `delete` "Quitar" (peligro). P1: icon buttons `arrow_upward` /
  `arrow_downward` para reordenar.
- **Base:** el select de estado y las acciones van en una segunda fila; ≥ 600 px todo en una fila.
- **Estados:** `default` · `actualizando` (select deshabilitado + spinner 16px) · `completado`
  (título en `--color-text-muted` e icono `task_alt`) · `error` (snackbar y el select vuelve al
  valor anterior).

### 4.12 Header

- Sticky, alto `--header-height`, fondo `--color-surface`; `--shadow-1` solo cuando la página
  tiene scroll. Base: hamburguesa + logo "Senda" (icono `route` en `--color-primary` + texto
  `--text-title-lg`) + a la derecha "Ingresar" (botón de texto) o avatar con inicial.
- ≥ 840 px: hamburguesa oculta; navegación horizontal con los mismos ítems del drawer como
  botones de texto (`--text-label`, activo con subrayado de 3px `--color-primary` y
  `aria-current="page"`); a la derecha "Aportar curso" (secundario), avatar o "Ingresar".

## 5. Layout y navegación

- **Header:** sticky (4.12). En mobile: hamburguesa + logo + sesión. En desktop: logo + navegación
  horizontal + "Aportar curso" + sesión.
- **Contenedor:** ancho completo con padding lateral `--space-4` (base) y `--space-5` (≥ 600 px);
  desde 840 px, `max-width: var(--container-max)` centrado. Separación vertical entre secciones
  `--space-6`.
- **Grilla de cursos:** `display: grid; gap: var(--space-4)`, 1 / 2 / 3 columnas según §3.
- **Pantallas** (detalle de navegación en el [APPFlow](APPFlow.md)):
  - **Home:** hero con buscador estilo Google (input de 48px, `--radius-full`, icono `search`) que
    lleva a `/catalogo?q=…`, chips de categorías y "Últimos cursos publicados" (6 cards).
  - **Catálogo:** barra de búsqueda + filtro de categoría, grilla de cards y paginador.
  - **Detalle de curso:** encabezado con chip de categoría y título; ficha de datos en lista de
    definiciones (`<dl>`); panel de acciones con "Ir al curso" (`open_in_new`) y
    "Agregar a mi roadmap".
  - **Formularios** (login, registro, recuperación, aportar): una columna centrada de máximo 560px;
    el de aporte agrupado en secciones con `<fieldset>`: "Datos del curso", "Características",
    "Tu experiencia".
  - **Mis aportes, Validación, Mi roadmap:** título + filtros por estado + listado paginado (4.4/4.11).

## 6. Accesibilidad mínima (no negociable)

- [x] Contraste AA medido en §2.1: texto ≥ 4.5:1 en todas las combinaciones de la paleta.
- [x] Bordes de controles interactivos ≥ 3:1: `--color-outline` (`#80868b`) 3.68:1 sobre blanco;
      `--color-outline-variant` se usa solo en elementos decorativos.
- [x] Los estados no dependen solo del color: todos los chips de estado llevan icono y texto.
- [ ] `:focus-visible` visible en todo elemento interactivo (anillo de 2px `--color-primary` con offset).
- [ ] Menú sándwich con `aria-expanded` / `aria-controls`, foco atrapado y restaurado al cerrar.
- [ ] `prefers-reduced-motion: reduce` desactiva animaciones de drawer, diálogos y skeleton.
- [ ] Imágenes con `alt`; iconos decorativos con `aria-hidden="true"`; icon buttons con `aria-label`.
- [ ] Errores de formulario asociados al campo con `aria-describedby` y `aria-invalid`; resumen
      de errores anunciado con `role="alert"` al enviar.
- [ ] Un solo `<h1>` por pantalla y jerarquía de títulos sin saltos; landmarks `header`, `nav`, `main`.
- [ ] Link "Saltar al contenido" como primer elemento enfocable.
- [ ] `lang="es"` en el documento; zoom al 200 % sin pérdida de contenido.

> Las casillas sin marcar se verifican sobre la implementación (Instancia B) con teclado y
> Lighthouse; las marcadas ya están garantizadas por los tokens de esta guía.

## 7. Iconografía y assets

- **Set elegido:** [Material Symbols Rounded](https://fonts.google.com/icons) por variable font
  de Google Fonts (`FILL 0`, `wght 400`, `GRAD 0`, `opsz 24`).
- **Por qué:** es el set de Google, coherente con la inspiración de la SPEC; una sola fuente
  cubre todos los iconos y se tiñe con `color` heredado.
- **Tamaño por defecto:** 24px en navegación e icon buttons; 20px dentro de botones; 18px en
  badges y chips; 64px en empty states. Color: hereda del texto, salvo estados (§4.10).
- **Logo:** wordmark "Senda" en Roboto 500 con el icono `route` en `--color-primary`; sin imagen raster.
- **Imágenes:** no se usan fotos de stock ni imágenes de cursos (evita derechos y peso). El
  favicon es el icono `route` en SVG.
- **Fuentes:** Roboto (400, 500), Roboto Mono (400) y Material Symbols Rounded desde Google Fonts
  con `display=swap`.

---

**Referencias:**
- NN/g — Front-End Style-Guides (definición y checklist): https://www.nngroup.com/articles/front-end-style-guides/
- NN/g — Design Systems 101: https://www.nngroup.com/articles/design-systems-101/
- Material Design 3 (inspiración): https://m3.material.io/
