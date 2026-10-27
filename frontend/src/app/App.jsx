import CatalogoPage from '../features/catalogo/CatalogoPage.jsx'
import styles from './App.module.css'

// Shell mínimo de v0.1.0: header + una pantalla. El router, el menú sándwich y el
// resto de las pantallas llegan con la tarea 0.5 del plan.
export default function App() {
  return (
    <>
      <a className="saltar-al-contenido" href="#contenido">
        Saltar al contenido
      </a>
      <header className={styles.header}>
        <span className={styles.marca}>
          <span className="material-symbols-rounded" aria-hidden="true">
            route
          </span>
          Senda
        </span>
      </header>
      <main id="contenido" className="contenedor">
        <CatalogoPage />
      </main>
    </>
  )
}
