/**
 * useApi composable unit tests.
 *
 * Tests: correct URL construction, auth header injection,
 * credentials:include, error throwing on non-ok responses,
 * and null return for 204 No Content.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

vi.stubGlobal('useRuntimeConfig', () => ({
  public: { apiBase: 'http://localhost:8000/api/v1' },
}))

vi.stubGlobal('useAuthStore', () => ({ accessToken: null }))

Object.defineProperty(globalThis, 'process', {
  value: { client: true },
  writable: true,
  configurable: true,
})

describe('useApi — apiFetch', () => {
  let useApi: typeof import('../../app/composables/useApi').useApi

  beforeEach(async () => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    const mod = await import('../../app/composables/useApi')
    useApi = mod.useApi
  })

  it('constructs the full URL from apiBase + endpoint', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true, status: 200,
      json: () => Promise.resolve({ result: 'ok' }),
    })
    vi.stubGlobal('fetch', fetchMock)

    const { apiFetch } = useApi()
    await apiFetch('/products/')

    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/products/',
      expect.any(Object),
    )
  })

  it('always sends credentials: include', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true, status: 200,
      json: () => Promise.resolve({}),
    })
    vi.stubGlobal('fetch', fetchMock)

    const { apiFetch } = useApi()
    await apiFetch('/products/')

    const [, options] = fetchMock.mock.calls[0]
    expect(options.credentials).toBe('include')
  })

  it('sets Content-Type: application/json by default', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true, status: 200,
      json: () => Promise.resolve({}),
    })
    vi.stubGlobal('fetch', fetchMock)

    const { apiFetch } = useApi()
    await apiFetch('/products/')

    const [, options] = fetchMock.mock.calls[0]
    expect(options.headers['Content-Type']).toBe('application/json')
  })

  it('injects Authorization header when auth token is available', async () => {
    vi.stubGlobal('useAuthStore', () => ({ accessToken: 'my.jwt.token' }))

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true, status: 200,
      json: () => Promise.resolve({}),
    })
    vi.stubGlobal('fetch', fetchMock)

    const { apiFetch } = useApi()
    await apiFetch('/products/')

    const [, options] = fetchMock.mock.calls[0]
    expect(options.headers['Authorization']).toBe('Bearer my.jwt.token')
  })

  it('does not inject Authorization header when no token', async () => {
    vi.stubGlobal('useAuthStore', () => ({ accessToken: null }))

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true, status: 200,
      json: () => Promise.resolve({}),
    })
    vi.stubGlobal('fetch', fetchMock)

    const { apiFetch } = useApi()
    await apiFetch('/products/')

    const [, options] = fetchMock.mock.calls[0]
    expect(options.headers['Authorization']).toBeUndefined()
  })

  it('throws the parsed error body when response is not ok', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false, status: 400,
      json: () => Promise.resolve({ detail: 'Bad request.' }),
    }))

    const { apiFetch } = useApi()

    await expect(apiFetch('/products/')).rejects.toMatchObject({
      detail: 'Bad request.',
    })
  })

  it('returns null for 204 No Content responses', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true, status: 204,
      json: () => Promise.resolve(null),
    }))

    const { apiFetch } = useApi()
    const result = await apiFetch('/cart/clear/')

    expect(result).toBeNull()
  })

  it('returns parsed JSON for successful responses', async () => {
    const payload = { id: 1, name: 'Bayern Kit' }
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true, status: 200,
      json: () => Promise.resolve(payload),
    }))

    const { apiFetch } = useApi()
    const result = await apiFetch('/products/1/')

    expect(result).toEqual(payload)
  })

  it('merges caller-provided headers with defaults', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true, status: 200,
      json: () => Promise.resolve({}),
    })
    vi.stubGlobal('fetch', fetchMock)

    const { apiFetch } = useApi()
    await apiFetch('/products/', {
      headers: { 'X-Custom-Header': 'my-value' },
    })

    const [, options] = fetchMock.mock.calls[0]
    expect(options.headers['X-Custom-Header']).toBe('my-value')
    expect(options.headers['Content-Type']).toBe('application/json')
  })
})