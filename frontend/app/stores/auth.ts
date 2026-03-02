import { defineStore } from 'pinia'

interface AuthUser {
  id: number
  email: string
  first_name: string
  last_name: string
  full_name: string
  phone: string | null
  is_staff: boolean
}

interface AuthResponse {
  user: AuthUser
  access_token: string
}

interface RegisterPayload {
  email: string
  first_name: string
  last_name: string
  password: string
  password_confirm: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as AuthUser | null,
    accessToken: null as string | null,
    loading: false,
    initialized: false,
  }),

  getters: {
    isAuthenticated: (state): boolean => !!state.user && !!state.accessToken,
  },

  actions: {
    async initOnClient() {
      if (!process.client || this.initialized) return
      this.initialized = true

      try {
        const config = useRuntimeConfig()
        const baseURL = config.public.apiBase as string
        const res = await fetch(`${baseURL}/auth/token/refresh/`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
        })
        if (res.ok) {
          const data = await res.json() as AuthResponse
          this.user = data.user
          this.accessToken = data.access_token
        }
      } catch {
        // Silent fail — user simply not authenticated
      }
    },

    async login(email: string, password: string): Promise<AuthResponse> {
      this.loading = true
      try {
        const config = useRuntimeConfig()
        const baseURL = config.public.apiBase as string
        const res = await fetch(`${baseURL}/auth/login/`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        })
        if (!res.ok) {
          const err = await res.json().catch(() => ({}))
          throw err
        }
        const data = await res.json() as AuthResponse
        this.user = data.user
        this.accessToken = data.access_token
        return data
      } finally {
        this.loading = false
      }
    },

    async register(payload: RegisterPayload): Promise<AuthResponse> {
      this.loading = true
      try {
        const config = useRuntimeConfig()
        const baseURL = config.public.apiBase as string
        const res = await fetch(`${baseURL}/auth/register/`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
        if (!res.ok) {
          const err = await res.json().catch(() => ({}))
          throw err
        }
        const data = await res.json() as AuthResponse
        this.user = data.user
        this.accessToken = data.access_token
        return data
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        const config = useRuntimeConfig()
        const baseURL = config.public.apiBase as string
        await fetch(`${baseURL}/auth/logout/`, {
          method: 'POST',
          credentials: 'include',
        })
      } catch {
        // Silent fail
      } finally {
        this.user = null
        this.accessToken = null
        this.initialized = false
      }
    },
  },
})
