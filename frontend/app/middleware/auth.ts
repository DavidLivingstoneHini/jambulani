/**
 * Global route middleware.
 * Protects routes that require authentication.
 * Redirects to /login with a `redirect` query param for post-login navigation.
 */
export default defineNuxtRouteMiddleware(async (to) => {
  // Skip middleware on server
  if (import.meta.server) return

  const authStore = useAuthStore()

  if (!authStore.initialized) {
    await authStore.initOnClient()
  }

  const publicRoutes = ['/login', '/register', '/', '/products', '/products/[slug]']
  const isPublicRoute = publicRoutes.some(route => to.path.startsWith(route))

  // Protected routes that require auth
  const protectedRoutes = ['/account', '/checkout']
  const requiresAuth = protectedRoutes.some(route => to.path.startsWith(route))

  if (requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath },
    })
  }

  // If user is authenticated redirect to home
  if ((to.path === '/login' || to.path === '/register') && authStore.isAuthenticated) {
    return navigateTo('/')
  }
})