/**
 * Core API composable for making authenticated requests to the backend.
 * Handles auth token injection and error normalization.
 */
export function useApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string

  async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...((options?.headers as Record<string, string>) ?? {}),
    }

    // Inject auth token on client only (token is never available server-side)
    if (process.client) {
      try {
        const authStore = useAuthStore()
        if (authStore.accessToken) {
          headers['Authorization'] = `Bearer ${authStore.accessToken}`
        }
      } catch {
        // Store might not be available in all contexts — safe to skip
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
