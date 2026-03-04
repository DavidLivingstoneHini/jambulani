/**
 * useApi composable unit tests.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { mockFetch } from '../setup'

// Import the actual useApi
import { useApi } from '../../app/composables/useApi'

describe('useApi — apiFetch', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    mockFetch.mockClear()
  })

  it('constructs the full URL from apiBase + endpoint', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ result: 'ok' }),
    })

    const { apiFetch } = useApi()
    await apiFetch('/products/')

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/products/',
      expect.objectContaining({
        credentials: 'include',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      }),
    )
  })

  it('always sends credentials: include', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({}),
    })

    const { apiFetch } = useApi()
    await apiFetch('/products/')

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        credentials: 'include'
      })
    )
  })

  it('sets Content-Type: application/json by default', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({}),
    })

    const { apiFetch } = useApi()
    await apiFetch('/products/')

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      })
    )
  })

  it('throws the parsed error body when response is not ok', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: () => Promise.resolve({ detail: 'Bad request.' }),
    })

    const { apiFetch } = useApi()

    await expect(apiFetch('/products/')).rejects.toMatchObject({
      detail: 'Bad request.',
    })
  })

  it('returns null for 204 No Content responses', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 204,
      json: () => Promise.resolve(null),
    })

    const { apiFetch } = useApi()
    const result = await apiFetch('/cart/clear/')

    expect(result).toBeNull()
  })

  it('returns parsed JSON for successful responses', async () => {
    const payload = { id: 1, name: 'Bayern Kit' }
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(payload),
    })

    const { apiFetch } = useApi()
    const result = await apiFetch('/products/1/')

    expect(result).toEqual(payload)
  })

  it('merges caller-provided headers with defaults', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({}),
    })

    const { apiFetch } = useApi()
    await apiFetch('/products/', {
      headers: { 'X-Custom-Header': 'my-value' },
    })

    expect(mockFetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: expect.objectContaining({
          'X-Custom-Header': 'my-value',
          'Content-Type': 'application/json'
        })
      })
    )
  })
})