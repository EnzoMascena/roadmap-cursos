import styles from './Paginador.module.css'

// Paginador de la base mobile (UX-UI §4.4): ‹ Anterior · Página N de M · Siguiente ›
export default function Paginador({ page, pages, onChange }) {
  if (pages <= 1) return null

  return (
    <nav className={styles.paginador} aria-label="Paginación">
      <button type="button" className={styles.boton} onClick={() => onChange(page - 1)} disabled={page <= 1}>
        <span className="material-symbols-rounded" aria-hidden="true">
          chevron_left
        </span>
        Anterior
      </button>
      <span className={styles.actual} aria-current="page">
        Página {page} de {pages}
      </span>
      <button type="button" className={styles.boton} onClick={() => onChange(page + 1)} disabled={page >= pages}>
        Siguiente
        <span className="material-symbols-rounded" aria-hidden="true">
          chevron_right
        </span>
      </button>
    </nav>
  )
}
