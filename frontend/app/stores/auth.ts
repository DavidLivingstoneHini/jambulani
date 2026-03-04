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

interface LoginPayload {
  email: string
  password: string
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

      const storedToken = localStorage.getItem('access_token')
      const storedUser = localStorage.getItem('user')
      
      if (storedToken && storedUser) {
        try {
          this.accessToken = storedToken
          this.user = JSON.parse(storedUser)
          return
        } catch (e) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('user')
        }
      }

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
          
          // Store in localStorage for persistence
          localStorage.setItem('access_token', data.access_token)
          localStorage.setItem('user', JSON.stringify(data.user))
        }
      } catch (error) {
        console.error('Failed to refresh token:', error)
      }
    },

    async login(payload: LoginPayload): Promise<AuthResponse> {
      this.loading = true
      try {
        const config = useRuntimeConfig()
        const baseURL = config.public.apiBase as string
        
        console.log('Logging in with:', payload.email)
        
        const res = await fetch(`${baseURL}/auth/login/`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
        
        const data = await res.json()
        
        if (!res.ok) {
          console.error('Login failed:', data)
          throw data
        }
        
        console.log('Login successful:', data)
        
        this.user = data.user
        this.accessToken = data.access_token
        
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        
        return data
      } catch (error) {
        console.error('Login error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async register(payload: RegisterPayload): Promise<AuthResponse> {
      this.loading = true
      try {
        const config = useRuntimeConfig()
        const baseURL = config.public.apiBase as string
        
        console.log('Registering with:', payload.email)
        
        const res = await fetch(`${baseURL}/auth/register/`, {
          method: 'POST',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
        
        const data = await res.json()
        
        if (!res.ok) {
          console.error('Registration failed:', data)
          throw data
        }
        
        console.log('Registration successful:', data)
        
        this.user = data.user
        this.accessToken = data.access_token
        
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        
        return data
      } catch (error) {
        console.error('Registration error:', error)
        throw error
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
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.user = null
        this.accessToken = null
        this.initialized = false
        
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
      }
    },

    async updateProfile(data: Partial<AuthUser>) {
      if (!this.user) throw new Error('Not authenticated')
      
      const config = useRuntimeConfig()
      const baseURL = config.public.apiBase as string
      
      const res = await fetch(`${baseURL}/auth/me/`, {
        method: 'PATCH',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.accessToken}`
        },
        body: JSON.stringify(data),
      })
      
      if (!res.ok) {
        const error = await res.json()
        throw error
      }
      
      const updatedUser = await res.json()
      this.user = updatedUser
      
      // Update stored user
      localStorage.setItem('user', JSON.stringify(updatedUser))
      
      return updatedUser
    },

    async changePassword(data: { current_password: string; new_password: string; new_password_confirm: string }) {
      if (!this.user) throw new Error('Not authenticated')
      
      const config = useRuntimeConfig()
      const baseURL = config.public.apiBase as string
      
      const res = await fetch(`${baseURL}/auth/password/change/`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.accessToken}`
        },
        body: JSON.stringify(data),
      })
      
      if (!res.ok) {
        const error = await res.json()
        throw error
      }
      
      await this.logout()
      
      return await res.json()
    },
  },
})
