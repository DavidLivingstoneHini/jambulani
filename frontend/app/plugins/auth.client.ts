/**
 * Client-side plugin: silently restore auth state and initialize cart on every page load.
 * Runs before the first route render so the middleware sees the correct auth state.
 */
export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()
  const cartStore = useCartStore()

  await authStore.initOnClient()
  await cartStore.fetchCart()
})
