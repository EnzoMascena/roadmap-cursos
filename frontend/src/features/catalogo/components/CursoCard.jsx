import styles from './CursoCard.module.css'

const BADGES = [
  { campo: 'tiene_cuestionarios', icono: 'quiz', texto: 'Cuestionarios' },
  { campo: 'requiere_examen', icono: 'assignment', texto: 'Examen' },
  { campo: 'extiende_certificado', icono: 'workspace_premium', texto: 'Certificado' },
  { campo: 'avalado_por_organizacion', icono: 'verified', texto: 'Aval' },
]

// Card de curso (UX-UI §4.3). En M2 pasa a ser un link al detalle del curso.
export default function CursoCard({ curso }) {
  const badges = BADGES.filter((badge) => curso[badge.campo])

  return (
    <article className={styles.card}>
      <span className={styles.chip}>{curso.categoria.nombre}</span>
      <h2 className={styles.titulo}>{curso.titulo}</h2>
      <p className={styles.meta}>
        {curso.plataforma} · {curso.anio_edicion}
      </p>
      <p className={styles.docentes}>{curso.docentes}</p>
      {badges.length > 0 && (
        <ul className={styles.badges} aria-label="Características">
          {badges.map((badge) => (
            <li key={badge.campo} className={styles.badge}>
              <span className="material-symbols-rounded" aria-hidden="true">
                {badge.icono}
              </span>
              {badge.texto}
            </li>
          ))}
        </ul>
      )}
    </article>
  )
}
