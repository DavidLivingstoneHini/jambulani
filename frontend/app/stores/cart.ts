import { defineStore } from 'pinia'

interface CartProduct {
  id: number
  name: string
  slug: string
  price: string
  original_price: string | null
  discount_percentage: number
  primary_image: string | null
  league_name: string | null
  category_name: string | null
  is_featured: boolean
}

interface CartPatch {
  id: number
  name: string
  image: string | null
  extra_price: string
}

interface CartItem {
  id: number
  product: CartProduct
  size: string
  custom_name: string | null
  custom_number: string | null
  patch: CartPatch | null
  quantity: number
  subtotal: string
}

interface Cart {
  items: CartItem[]
  total: string
  count: number
}

interface AddItemPayload {
  product_id: number
  size: string
  quantity: number
  custom_name?: string
  custom_number?: string
  patch_id?: number | null
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    cart: { items: [], total: '0.00', count: 0 } as Cart,
    isOpen: false,
    loading: false,
  }),

  getters: {
    itemCount: (state): number => state.cart.count,
    cartTotal: (state): string => state.cart.total,
  },

  actions: {
    async initOnClient() {
      if (process.client) {
        await this.fetchCart()
      }
    },

    async fetchCart() {
      if (!process.client) return

      this.loading = true
      try {
        // Handle test environment
        let baseURL = 'http://localhost:8000/api/v1'
        if (typeof useRuntimeConfig !== 'undefined') {
          const config = useRuntimeConfig()
          baseURL = config.public.apiBase as string
        }
        
        const authStore = useAuthStore()

        const headers: Record<string, string> = {
          'Content-Type': 'application/json',
        }
        if (authStore.accessToken) {
          headers['Authorization'] = `Bearer ${authStore.accessToken}`
        }

        const res = await fetch(`${baseURL}/cart/`, {
          credentials: 'include',
          headers,
        })
        if (res.ok) {
          const data = await res.json() as Cart
          this.cart = data
        }
      } catch (e) {
        console.error('Failed to fetch cart', e)
      } finally {
        this.loading = false
      }
    },

    async addItem(payload: AddItemPayload) {
      if (!process.client) return

      this.loading = true
      try {
        // Handle test environment
        let baseURL = 'http://localhost:8000/api/v1'
        if (typeof useRuntimeConfig !== 'undefined') {
          const config = useRuntimeConfig()
          baseURL = config.public.apiBase as string
        }
        
        const authStore = useAuthStore()

        const headers: Record<string, string> = {
          'Content-Type': 'application/json',
        }
        if (authStore.accessToken) {
          headers['Authorization'] = `Bearer ${authStore.accessToken}`
        }

        const res = await fetch(`${baseURL}/cart/`, {
          method: 'POST',
          credentials: 'include',
          headers,
          body: JSON.stringify(payload),
        })
        if (!res.ok) {
          const err = await res.json().catch(() => ({}))
          throw err
        }
        await this.fetchCart()
        this.isOpen = true
      } finally {
        this.loading = false
      }
    },

    async updateQuantity(itemId: number, quantity: number) {
      if (!process.client) return

      try {
        // Handle test environment
        let baseURL = 'http://localhost:8000/api/v1'
        if (typeof useRuntimeConfig !== 'undefined') {
          const config = useRuntimeConfig()
          baseURL = config.public.apiBase as string
        }
        
        const authStore = useAuthStore()

        const headers: Record<string, string> = {
          'Content-Type': 'application/json',
        }
        if (authStore.accessToken) {
          headers['Authorization'] = `Bearer ${authStore.accessToken}`
        }

        const res = await fetch(`${baseURL}/cart/${itemId}/`, {
          method: 'PATCH',
          credentials: 'include',
          headers,
          body: JSON.stringify({ quantity }),
        })
        if (res.ok || res.status === 204) {
          await this.fetchCart()
        }
      } catch (e) {
        console.error('Failed to update quantity', e)
      }
    },

    async removeItem(itemId: number) {
      if (!process.client) return

      try {
        // Handle test environment
        let baseURL = 'http://localhost:8000/api/v1'
        if (typeof useRuntimeConfig !== 'undefined') {
          const config = useRuntimeConfig()
          baseURL = config.public.apiBase as string
        }
        
        const authStore = useAuthStore()

        const headers: Record<string, string> = {}
        if (authStore.accessToken) {
          headers['Authorization'] = `Bearer ${authStore.accessToken}`
        }

        await fetch(`${baseURL}/cart/${itemId}/`, {
          method: 'DELETE',
          credentials: 'include',
          headers,
        })
        await this.fetchCart()
      } catch (e) {
        console.error('Failed to remove item', e)
      }
    },

    toggleCart() {
      if (process.client) {
        this.isOpen = !this.isOpen
      }
    },
  },
})