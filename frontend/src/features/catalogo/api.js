import { apiGet } from '../../compartido/api/cliente.js'

export const TAMANIO_PAGINA = 12

// GET /api/v1/cursos → { items, total, page, page_size, pages } (BackendSchema §3.2)
export function listarCursos({ page = 1, pageSize = TAMANIO_PAGINA, signal } = {}) {
  return apiGet('/cursos', { params: { page, page_size: pageSize }, signal })
}
