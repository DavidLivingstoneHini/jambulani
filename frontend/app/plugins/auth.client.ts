/**
 * Client-side plugin: silently restore auth state on every page load/refresh.
 * Runs before the first route render so the middleware sees the correct state.
 */
export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()
  await authStore.initialize()
})
