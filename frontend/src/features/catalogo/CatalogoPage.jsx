import { useState } from 'react'
import Paginador from '../../compartido/ui/Paginador.jsx'
import CursoCard from './components/CursoCard.jsx'
import { useCursos } from './hooks/useCursos.js'
import { TAMANIO_PAGINA } from './api.js'
import styles from './CatalogoPage.module.css'

// Catálogo comunitario (APPFlow §3): consume GET /api/v1/cursos con sus 4 estados.
export default function CatalogoPage() {
  const [page, setPage] = useState(1)
  const { status, data, error, reintentar } = useCursos(page)

  return (
    <section aria-labelledby="titulo-catalogo">
      <header className={styles.encabezado}>
        <h1 id="titulo-catalogo" className={styles.titulo}>
          Catálogo comunitario
        </h1>
        <p className={styles.bajada}>Cursos gratuitos aportados por la comunidad y validados.</p>
      </header>

      {status === 'loading' && <Cargando />}

      {status === 'error' && (
        <EstadoMensaje icono="cloud_off" titulo="No pudimos cargar los cursos" texto={error.message}>
          <button type="button" className={styles.botonSecundario} onClick={reintentar}>
            Reintentar
          </button>
        </EstadoMensaje>
      )}

      {status === 'empty' && data.total > 0 && (
        <EstadoMensaje icono="search_off" titulo="Esta página no tiene cursos" texto="Probá volviendo a la primera página.">
          <button type="button" className={styles.botonSecundario} onClick={() => setPage(1)}>
            Volver a la página 1
          </button>
        </EstadoMensaje>
      )}

      {status === 'empty' && data.total === 0 && (
        <EstadoMensaje
          icono="menu_book"
          titulo="Todavía no hay cursos publicados"
          texto="Cuando la comunidad aporte cursos y se validen, van a aparecer acá."
        />
      )}

      {status === 'ok' && (
        <>
          <p className={styles.contador}>
            Mostrando {(data.page - 1) * data.page_size + 1}–{(data.page - 1) * data.page_size + data.items.length} de{' '}
            {data.total}
          </p>
          <ul className={styles.grilla}>
            {data.items.map((curso) => (
              <li key={curso.id}>
                <CursoCard curso={curso} />
              </li>
            ))}
          </ul>
          <Paginador page={data.page} pages={data.pages} onChange={setPage} />
        </>
      )}
    </section>
  )
}

function Cargando() {
  return (
    <div aria-busy="true">
      <span className={styles.visualmenteOculto}>Cargando cursos…</span>
      <ul className={styles.grilla} aria-hidden="true">
        {Array.from({ length: Math.min(TAMANIO_PAGINA, 6) }, (_, indice) => (
          <li key={indice} className={styles.skeleton} />
        ))}
      </ul>
    </div>
  )
}

function EstadoMensaje({ icono, titulo, texto, children }) {
  return (
    <div className={styles.estado} role="status">
      <span className={`material-symbols-rounded ${styles.estadoIcono}`} aria-hidden="true">
        {icono}
      </span>
      <h2 className={styles.estadoTitulo}>{titulo}</h2>
      <p className={styles.estadoTexto}>{texto}</p>
      {children}
    </div>
  )
}
