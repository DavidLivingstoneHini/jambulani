/**
 * Core API composable for making authenticated requests to the backend.
 * Handles auth token injection and error normalization.
 */
export function useApi() {
  // Handle test environment
  if (typeof useRuntimeConfig === 'undefined') {
    return {
      apiFetch: async <T>(endpoint: string, options?: RequestInit): Promise<T> => {
        const mockFetch = global.fetch || (() => Promise.resolve(new Response()))
        const res = await mockFetch(`http://localhost:8000/api/v1${endpoint}`, {
          credentials: 'include',
          ...options,
          headers: {
            'Content-Type': 'application/json',
            ...(options?.headers || {})
          }
        })
        
        if (!res.ok) {
          const error = await res.json().catch(() => ({}))
          throw error
        }
        
        if (res.status === 204) return null as T
        return res.json() as Promise<T>
      },
      baseURL: 'http://localhost:8000/api/v1'
    }
  }

  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string

  async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...((options?.headers as Record<string, string>) ?? {}),
    }

    // Inject auth token on client only
    if (process.client) {
      try {
        const authStore = useAuthStore()
        if (authStore.accessToken) {
          headers['Authorization'] = `Bearer ${authStore.accessToken}`
        }
      } catch {
      }
    }

    const res = await fetch(`${baseURL}${endpoint}`, {
      credentials: 'include',
      ...options,
      headers,
    })

    if (!res.ok) {
      const error = await res.json().catch(() => ({}))
      throw error
    }

    if (res.status === 204) return null as T
    return res.json() as Promise<T>
  }

  return { apiFetch, baseURL }
}