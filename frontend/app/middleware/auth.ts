/**
 * Global route middleware.
 * Protects routes that require authentication.
 * Redirects to /login with a `redirect` query param for post-login navigation.
 */
export default defineNuxtRouteMiddleware(async (to) => {
  if (!process.client) return

  const authStore = useAuthStore()

  if (!authStore.initialized) {
    await authStore.initOnClient()
  }

  const protectedRoutes = ['/account', '/checkout']
  const requiresAuth = protectedRoutes.some(route => to.path.startsWith(route))

  if (requiresAuth && !authStore.isAuthenticated) {
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath },
    })
  }

  const authOnlyRoutes = ['/login', '/register']
  if (authOnlyRoutes.includes(to.path) && authStore.isAuthenticated) {
    return navigateTo('/')
  }
})
