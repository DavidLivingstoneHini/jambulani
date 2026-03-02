/**
 * Utility composable that safely accesses a Pinia store only on the client side.
 * Prevents SSR hydration mismatches for stores that depend on browser APIs.
 *
 * @example
 * const { getStore } = useClientStore()
 * const cart = getStore(() => useCartStore())
 */
export function useClientStore() {
  function getStore<T>(storeAccessor: () => T): T | null {
    if (process.client) {
      return storeAccessor()
    }
    return null
  }

  return { getStore }
}
