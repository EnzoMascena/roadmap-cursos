// Cliente HTTP único: arma la URL, hace el fetch y traduce el envelope de errores
// {"error": {"code", "message", "details"}} del backend (TRD TD-008).
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'

export class ApiError extends Error {
  constructor(status, code, message, details = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.details = details
  }
}

function armarQuery(params = {}) {
  const definidos = Object.entries(params).filter(([, valor]) => valor !== undefined && valor !== null && valor !== '')
  return definidos.length ? `?${new URLSearchParams(definidos)}` : ''
}

export async function apiGet(path, { params, signal } = {}) {
  let respuesta
  try {
    respuesta = await fetch(`${BASE_URL}${path}${armarQuery(params)}`, {
      headers: { Accept: 'application/json' },
      signal,
    })
  } catch (error) {
    if (error.name === 'AbortError') throw error
    throw new ApiError(0, 'SIN_CONEXION', 'No pudimos conectar con el servidor.')
  }

  const cuerpo = await respuesta.json().catch(() => null)
  if (!respuesta.ok) {
    const error = cuerpo?.error
    throw new ApiError(
      respuesta.status,
      error?.code ?? 'ERROR_HTTP',
      error?.message ?? 'El servidor no pudo responder. Probá de nuevo en unos segundos.',
      error?.details ?? null,
    )
  }
  return cuerpo
}
