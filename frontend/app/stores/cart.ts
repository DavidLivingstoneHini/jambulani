import { defineStore } from 'pinia'
import type { Cart } from '~/app/types'

export const useCartStore = defineStore('cart', () => {
  const cart = ref<Cart>({ items: [], total: '0.00', count: 0 })
  const isOpen = ref(false)
  const loading = ref(false)
  const { apiFetch } = useApi()

  async function fetchCart() {
    loading.value = true
    try {
      const data = await apiFetch<Cart>('/cart/')
      cart.value = data
    } catch (e) {
      console.error('Failed to fetch cart', e)
    } finally {
      loading.value = false
    }
  }

  async function addItem(payload: {
    product_id: number
    size: string
    quantity?: number
    custom_name?: string
    custom_number?: string
    patch_id?: number | null
  }) {
    loading.value = true
    try {
      await apiFetch('/cart/', {
        method: 'POST',
        body: JSON.stringify(payload),
      })
      await fetchCart()
      isOpen.value = true
    } finally {
      loading.value = false
    }
  }

  async function updateQuantity(itemId: number, quantity: number) {
    await apiFetch(`/cart/${itemId}/`, {
      method: 'PATCH',
      body: JSON.stringify({ quantity }),
    })
    await fetchCart()
  }

  async function removeItem(itemId: number) {
    await apiFetch(`/cart/${itemId}/`, { method: 'DELETE' })
    await fetchCart()
  }

  async function clearCart() {
    await apiFetch('/cart/clear/', { method: 'DELETE' })
    await fetchCart()
  }

  const itemCount = computed(() => cart.value.count)
  const cartTotal = computed(() => cart.value.total)

  return {
    cart,
    isOpen,
    loading,
    itemCount,
    cartTotal,
    fetchCart,
    addItem,
    updateQuantity,
    removeItem,
    clearCart,
  }
})
