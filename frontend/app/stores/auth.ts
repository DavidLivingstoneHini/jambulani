/**
 * Auth store — manages the access token in memory (never localStorage),
 * the user profile, and silent token refresh.
 *
 * Security model:
 *  - Access token:  short-lived JWT, kept in memory only (not localStorage/sessionStorage)
 *  - Refresh token: HttpOnly cookie, sent automatically by the browser
 *  - On page reload: /auth/session/ is hit to restore state if access_token cookie exists,
 *    otherwise /auth/token/refresh/ is called to get a fresh access token silently.
 */
import { defineStore } from 'pinia'
import type { AuthUser, LoginPayload, RegisterPayload, AuthResponse } from '~/app/types'

export const useAuthStore = defineStore('auth', () => {
  // ── State ────────────────────────────────────────────────────────
  const user = ref<AuthUser | null>(null)
  const accessToken = ref<string | null>(null)   // in-memory only
  const loading = ref(false)
  const initialized = ref(false)                  // has the store attempted session restore?

  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string

  // ── Getters ──────────────────────────────────────────────────────
  const isAuthenticated = computed(() => !!user.value && !!accessToken.value)
  const isStaff = computed(() => user.value?.is_staff ?? false)

  // ── Internal helpers ─────────────────────────────────────────────
  async function _request<T>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string> | undefined),
    }
    if (accessToken.value) {
      headers['Authorization'] = `Bearer ${accessToken.value}`
    }
    const res = await fetch(`${baseURL}${endpoint}`, {
      credentials: 'include',   // send HttpOnly cookies
      ...options,
      headers,
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw { status: res.status, data: err }
    }
    if (res.status === 204) return undefined as T
    return res.json()
  }

  function _applyAuthResponse(data: AuthResponse) {
    user.value = data.user
    accessToken.value = data.access_token
  }

  function _clearAuth() {
    user.value = null
    accessToken.value = null
  }

  // ── Public actions ───────────────────────────────────────────────
  async function login(payload: LoginPayload) {
    loading.value = true
    try {
      const data = await _request<AuthResponse>('/auth/login/', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
      _applyAuthResponse(data)
      return data
    } finally {
      loading.value = false
    }
  }

  async function register(payload: RegisterPayload) {
    loading.value = true
    try {
      const data = await _request<AuthResponse>('/auth/register/', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
      _applyAuthResponse(data)
      return data
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await _request('/auth/logout/', { method: 'POST' })
    } catch {
      // Even if the request fails, clear local state
    } finally {
      _clearAuth()
    }
  }

  /**
   * Silent refresh — uses the HttpOnly refresh_token cookie.
   * Called automatically when the access token is missing/expired.
   */
  async function silentRefresh(): Promise<boolean> {
    try {
      const data = await _request<AuthResponse>('/auth/token/refresh/', { method: 'POST' })
      _applyAuthResponse(data)
      return true
    } catch {
      _clearAuth()
      return false
    }
  }

  /**
   * Called once on app mount. Tries to restore auth state from the
   * access_token cookie (set on login). Falls back to silent refresh.
   */
  async function initialize() {
    if (initialized.value) return
    initialized.value = true

    try {
      // Fast path: access token cookie still valid
      const data = await _request<{ user: AuthUser }>('/auth/session/')
      user.value = data.user
      // We don't get a new access token here, trigger a silent refresh to get one in memory
      await silentRefresh()
    } catch (e: any) {
      if (e?.status === 401) {
        // Try refresh flow
        await silentRefresh()
      } else {
        _clearAuth()
      }
    }
  }

  async function updateProfile(payload: Partial<AuthUser>) {
    const data = await _request<AuthUser>('/auth/me/', {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
    user.value = data
    return data
  }

  async function changePassword(payload: {
    current_password: string
    new_password: string
    new_password_confirm: string
  }) {
    await _request('/auth/password/change/', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
    _clearAuth()
  }

  return {
    user,
    accessToken,
    loading,
    initialized,
    isAuthenticated,
    isStaff,
    login,
    register,
    logout,
    silentRefresh,
    initialize,
    updateProfile,
    changePassword,
  }
})
