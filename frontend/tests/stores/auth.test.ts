/**
 * Auth store unit tests.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { mockFetch, localStorageMock } from '../setup'
import { useAuthStore } from '../../app/stores/auth'

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

describe('Auth Store', () => {
  let auth: ReturnType<typeof useAuthStore>

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    mockFetch.mockClear()
    localStorageMock.clear()
    auth = useAuthStore()
  })

  // Initial state
  it('starts unauthenticated with null user and token', () => {
    expect(auth.user).toBeNull()
    expect(auth.accessToken).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
    expect(auth.loading).toBe(false)
  })

  // isAuthenticated getter
  it('isAuthenticated is true when user and token are both set', () => {
    auth.user = mockUser
    auth.accessToken = 'valid.jwt.token'
    expect(auth.isAuthenticated).toBe(true)
  })

  it('isAuthenticated is false when user is set but token is null', () => {
    auth.user = mockUser
    auth.accessToken = null
    expect(auth.isAuthenticated).toBe(false)
  })

  it('isAuthenticated is false when token is set but user is null', () => {
    auth.user = null
    auth.accessToken = 'some.token'
    expect(auth.isAuthenticated).toBe(false)
  })

  // login()
  it('login sets user and accessToken on success', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({
        user: mockUser,
        access_token: 'test.jwt.token',
      }),
    })

    await auth.login({ email: 'fan@jambulani.com', password: 'StrongPass123!' })

    expect(auth.user).toEqual(mockUser)
    expect(auth.accessToken).toBe('test.jwt.token')
    expect(auth.isAuthenticated).toBe(true)
    expect(localStorageMock.setItem).toHaveBeenCalled()
  })

  it('login calls the correct API endpoint', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ user: mockUser, access_token: 'tok' }),
    })

    await auth.login({ email: 'fan@jambulani.com', password: 'StrongPass123!' })

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/auth/login/',
      expect.objectContaining({ 
        method: 'POST',
        credentials: 'include',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      }),
    )
  })

  it('login throws on API error and does not set user', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: () => Promise.resolve({ email: ['Invalid credentials.'] }),
    })

    await expect(
      auth.login({ email: 'wrong@jambulani.com', password: 'BadPass!' })
    ).rejects.toBeTruthy()

    expect(auth.user).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
  })

  it('login resets loading to false after success', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ user: mockUser, access_token: 'tok' }),
    })

    await auth.login({ email: 'fan@jambulani.com', password: 'StrongPass123!' })

    expect(auth.loading).toBe(false)
  })

  it('login resets loading to false after failure', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: () => Promise.resolve({}),
    })

    try {
      await auth.login({ email: 'x@x.com', password: 'bad' })
    } catch (error) {
      // Expected error
    }

    expect(auth.loading).toBe(false)
  })

  // register()
  it('register sets user and accessToken on success', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: () => Promise.resolve({
        user: mockUser,
        access_token: 'new.jwt.token',
      }),
    })

    await auth.register({
      email: 'fan@jambulani.com',
      first_name: 'Fan',
      last_name: 'Supporter',
      password: 'StrongPass123!',
      password_confirm: 'StrongPass123!',
    })

    expect(auth.user).toEqual(mockUser)
    expect(auth.accessToken).toBe('new.jwt.token')
    expect(auth.isAuthenticated).toBe(true)
  })

  it('register calls the correct API endpoint', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: () => Promise.resolve({ user: mockUser, access_token: 'tok' }),
    })

    await auth.register({
      email: 'fan@jambulani.com',
      first_name: 'Fan',
      last_name: 'Supporter',
      password: 'StrongPass123!',
      password_confirm: 'StrongPass123!',
    })

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/auth/register/',
      expect.objectContaining({ method: 'POST' }),
    )
  })

  // logout()
  it('logout clears user, token and initialized flag', async () => {
    auth.user = mockUser
    auth.accessToken = 'some.token'
    auth.initialized = true

    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(null),
    })

    await auth.logout()

    expect(auth.user).toBeNull()
    expect(auth.accessToken).toBeNull()
    expect(auth.initialized).toBe(false)
    expect(auth.isAuthenticated).toBe(false)
    expect(localStorageMock.removeItem).toHaveBeenCalled()
  })

  it('logout clears state even if API call fails', async () => {
    auth.user = mockUser
    auth.accessToken = 'some.token'

    mockFetch.mockRejectedValueOnce(new Error('Network error'))

    await auth.logout()

    expect(auth.user).toBeNull()
    expect(auth.accessToken).toBeNull()
  })

  it('logout calls the correct API endpoint', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(null),
    })

    await auth.logout()

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/auth/logout/',
      expect.objectContaining({ method: 'POST' }),
    )
  })
})