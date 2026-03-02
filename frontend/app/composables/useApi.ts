/**
 * General-purpose fetch composable.
 * Automatically attaches the access token when available.
 * Transparently retries once after a silent refresh on 401.
 */
export function useApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase as string

  async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const authStore = useAuthStore()

    const buildHeaders = () => {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...(options?.headers as Record<string, string> | undefined),
      }
      if (authStore.accessToken) {
        headers['Authorization'] = `Bearer ${authStore.accessToken}`
      }
      return headers
    }

    const doFetch = (headers: Record<string, string>) =>
      fetch(`${baseURL}${endpoint}`, { credentials: 'include', ...options, headers })

    let res = await doFetch(buildHeaders())

    // Transparent silent-refresh on 401
    if (res.status === 401) {
      const refreshed = await authStore.silentRefresh()
      if (refreshed) {
        res = await doFetch(buildHeaders())
      }
    }

    if (!res.ok) {
      const error = await res.json().catch(() => ({}))
      throw { status: res.status, data: error }
    }

    if (res.status === 204) return undefined as T
    return res.json()
  }

  return { apiFetch, baseURL }
}
