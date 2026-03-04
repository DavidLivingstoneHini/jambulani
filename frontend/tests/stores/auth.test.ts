/**
 * Auth store unit tests.
 *
 * The store uses raw fetch() and process.client internally.
 * We mock both so tests run in Node/happy-dom without a real server.
 *
 * Auth store login signature: login(email: string, password: string)
 * Auth store register signature: register(payload: RegisterPayload)
 * cartTotal getter returns: string (not number)
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

// Globals the store depends on

Object.defineProperty(globalThis, 'process', {
  value: { client: true },
  writable: true,
})

vi.stubGlobal('useRuntimeConfig', () => ({
  public: {
    apiBase: 'http://localhost:8000/api/v1',
    mediaBase: 'http://localhost:8000',
  },
}))

vi.stubGlobal('useAuthStore', () => ({ accessToken: null }))

// Fixtures
const mockUser = {
  id: 1,
  email: 'fan@jambulani.com',
  first_name: 'Fan',
  last_name: 'Supporter',
  full_name: 'Fan Supporter',
  phone: null,
  is_staff: false,
}

function mockFetchSuccess(body: unknown, status = 200) {
  return vi.fn().mockResolvedValue({
    ok: true,
    status,
    json: () => Promise.resolve(body),
  })
}

function mockFetchFailure(body: unknown, status = 400) {
  return vi.fn().mockResolvedValue({
    ok: false,
    status,
    json: () => Promise.resolve(body),
  })
}

// Tests

describe('Auth Store', () => {
  let useAuthStore: typeof import('../../app/stores/auth').useAuthStore

  beforeEach(async () => {
    setActivePinia(createPinia())
    vi.unstubAllGlobals()

    vi.stubGlobal('useRuntimeConfig', () => ({
      public: { apiBase: 'http://localhost:8000/api/v1' },
    }))
    vi.stubGlobal('useAuthStore', () => ({ accessToken: null }))
    Object.defineProperty(globalThis, 'process', {
      value: { client: true }, writable: true, configurable: true,
    })

    const mod = await import('../../app/stores/auth')
    useAuthStore = mod.useAuthStore
  })

  // Initial state

  it('starts unauthenticated with null user and token', () => {
    const auth = useAuthStore()
    expect(auth.user).toBeNull()
    expect(auth.accessToken).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
    expect(auth.loading).toBe(false)
  })

  // isAuthenticated getter

  it('isAuthenticated is true when user and token are both set', () => {
    const auth = useAuthStore()
    auth.user = mockUser
    auth.accessToken = 'valid.jwt.token'
    expect(auth.isAuthenticated).toBe(true)
  })

  it('isAuthenticated is false when user is set but token is null', () => {
    const auth = useAuthStore()
    auth.user = mockUser
    auth.accessToken = null
    expect(auth.isAuthenticated).toBe(false)
  })

  it('isAuthenticated is false when token is set but user is null', () => {
    const auth = useAuthStore()
    auth.user = null
    auth.accessToken = 'some.token'
    expect(auth.isAuthenticated).toBe(false)
  })

  // login()

  it('login sets user and accessToken on success', async () => {
    const auth = useAuthStore()
    vi.stubGlobal('fetch', mockFetchSuccess({
      user: mockUser,
      access_token: 'test.jwt.token',
    }))

    await auth.login('fan@jambulani.com', 'StrongPass123!')

    expect(auth.user?.email).toBe('fan@jambulani.com')
    expect(auth.accessToken).toBe('test.jwt.token')
    expect(auth.isAuthenticated).toBe(true)
  })

  it('login calls the correct API endpoint', async () => {
    const auth = useAuthStore()
    const fetchMock = mockFetchSuccess({ user: mockUser, access_token: 'tok' })
    vi.stubGlobal('fetch', fetchMock)

    await auth.login('fan@jambulani.com', 'StrongPass123!')

    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/auth/login/',
      expect.objectContaining({ method: 'POST' }),
    )
  })

  it('login sends credentials: include for cookie auth', async () => {
    const auth = useAuthStore()
    const fetchMock = mockFetchSuccess({ user: mockUser, access_token: 'tok' })
    vi.stubGlobal('fetch', fetchMock)

    await auth.login('fan@jambulani.com', 'StrongPass123!')

    expect(fetchMock).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({ credentials: 'include' }),
    )
  })

  it('login throws on API error and does not set user', async () => {
    const auth = useAuthStore()
    vi.stubGlobal('fetch', mockFetchFailure({ email: ['Invalid credentials.'] }))

    await expect(
      auth.login('wrong@jambulani.com', 'BadPass!')
    ).rejects.toBeTruthy()

    expect(auth.user).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
  })

  it('login resets loading to false after success', async () => {
    const auth = useAuthStore()
    vi.stubGlobal('fetch', mockFetchSuccess({ user: mockUser, access_token: 'tok' }))

    await auth.login('fan@jambulani.com', 'StrongPass123!')

    expect(auth.loading).toBe(false)
  })

  it('login resets loading to false after failure', async () => {
    const auth = useAuthStore()
    vi.stubGlobal('fetch', mockFetchFailure({}))

    await auth.login('x@x.com', 'bad').catch(() => {})

    expect(auth.loading).toBe(false)
  })

  // register()

  it('register sets user and accessToken on success', async () => {
    const auth = useAuthStore()
    vi.stubGlobal('fetch', mockFetchSuccess({
      user: mockUser,
      access_token: 'new.jwt.token',
    }, 201))

    await auth.register({
      email: 'fan@jambulani.com',
      first_name: 'Fan',
      last_name: 'Supporter',
      password: 'StrongPass123!',
      password_confirm: 'StrongPass123!',
    })

    expect(auth.user?.email).toBe('fan@jambulani.com')
    expect(auth.accessToken).toBe('new.jwt.token')
    expect(auth.isAuthenticated).toBe(true)
  })

  it('register calls the correct API endpoint', async () => {
    const auth = useAuthStore()
    const fetchMock = mockFetchSuccess({ user: mockUser, access_token: 'tok' }, 201)
    vi.stubGlobal('fetch', fetchMock)

    await auth.register({
      email: 'fan@jambulani.com',
      first_name: 'Fan',
      last_name: 'Supporter',
      password: 'StrongPass123!',
      password_confirm: 'StrongPass123!',
    })

    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/auth/register/',
      expect.objectContaining({ method: 'POST' }),
    )
  })

  it('register throws on duplicate email', async () => {
    const auth = useAuthStore()
    vi.stubGlobal('fetch', mockFetchFailure({
      email: ['An account with this email already exists.'],
    }))

    await expect(
      auth.register({
        email: 'dup@jambulani.com',
        first_name: 'A',
        last_name: 'B',
        password: 'StrongPass123!',
        password_confirm: 'StrongPass123!',
      })
    ).rejects.toBeTruthy()

    expect(auth.user).toBeNull()
  })

  // logout()

  it('logout clears user, token and initialized flag', async () => {
    const auth = useAuthStore()
    auth.user = mockUser
    auth.accessToken = 'some.token'
    auth.initialized = true

    vi.stubGlobal('fetch', mockFetchSuccess(null, 200))

    await auth.logout()

    expect(auth.user).toBeNull()
    expect(auth.accessToken).toBeNull()
    expect(auth.initialized).toBe(false)
    expect(auth.isAuthenticated).toBe(false)
  })

  it('logout clears state even if API call fails', async () => {
    const auth = useAuthStore()
    auth.user = mockUser
    auth.accessToken = 'some.token'

    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network error')))

    await auth.logout()

    expect(auth.user).toBeNull()
    expect(auth.accessToken).toBeNull()
  })

  it('logout calls the correct API endpoint', async () => {
    const auth = useAuthStore()
    const fetchMock = mockFetchSuccess(null, 200)
    vi.stubGlobal('fetch', fetchMock)

    await auth.logout()

    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/auth/logout/',
      expect.objectContaining({ method: 'POST' }),
    )
  })
})