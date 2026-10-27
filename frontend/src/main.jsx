import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './app/App.jsx'
import './styles/tokens.css'
import './styles/base.css'

// Los iconos se muestran recién cuando cargó la fuente de Material Symbols (base.css).
document.fonts
  ?.load('24px "Material Symbols Rounded"')
  .then((fuentes) => {
    if (fuentes.length > 0) document.documentElement.classList.add('iconos-listos')
  })
  .catch(() => {})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
