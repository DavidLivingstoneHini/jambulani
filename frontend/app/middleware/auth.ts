/**
 * Global route middleware.
 * Protects routes that require authentication.
 * Redirects to /login with a `redirect` query param for post-login navigation.
 */
export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore()

  const protectedRoutes = ['/account', '/checkout']
  const requiresAuth = protectedRoutes.some(route => to.path.startsWith(route))

  if (requiresAuth && !authStore.isAuthenticated) {
    return navigateTo({
      path: '/login',
      query: { redirect: to.fullPath },
    })
  }

  // Redirect already-authenticated users away from auth pages
  const authOnlyRoutes = ['/login', '/register']
  if (authOnlyRoutes.includes(to.path) && authStore.isAuthenticated) {
    return navigateTo('/')
  }
})
