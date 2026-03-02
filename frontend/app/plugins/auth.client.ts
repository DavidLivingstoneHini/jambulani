/**
 * Client-side plugin: silently restore auth state and initialize cart on every page load.
 * Runs before the first route render so the middleware sees the correct auth state.
 */
export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()
  const cartStore = useCartStore()

  // Initialize auth first, then cart (cart may need auth token)
  await authStore.initOnClient()
  await cartStore.fetchCart()
})
