import { useCallback, useEffect, useState } from 'react'
import { listarCursos } from '../api.js'

// Pide una página del catálogo y expone su estado: loading | ok | empty | error.
// Cada pedido tiene una "clave" (página + reintento): mientras la respuesta guardada
// no corresponde a la clave actual, el estado es loading.
export function useCursos(page) {
  const [intento, setIntento] = useState(0)
  const [resultado, setResultado] = useState({ clave: null, data: null, error: null })
  const clave = `${page}:${intento}`

  useEffect(() => {
    const controlador = new AbortController()
    listarCursos({ page, signal: controlador.signal })
      .then((data) => setResultado({ clave, data, error: null }))
      .catch((error) => {
        if (error.name !== 'AbortError') setResultado({ clave, data: null, error })
      })
    return () => controlador.abort()
  }, [clave, page])

  const reintentar = useCallback(() => setIntento((n) => n + 1), [])

  let status = 'ok'
  if (resultado.clave !== clave) status = 'loading'
  else if (resultado.error) status = 'error'
  else if (resultado.data.items.length === 0) status = 'empty'

  return { status, data: resultado.data, error: resultado.error, reintentar }
}
