/**
 * Cart store unit tests.
 *
 * The store uses raw fetch() internally (not useApi).
 * cartTotal getter returns string (not number) — confirmed from store source.
 * itemCount getter returns cart.count (not sum of quantities).
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

// Globals 
Object.defineProperty(globalThis, 'process', {
  value: { client: true },
  writable: true,
  configurable: true,
})

vi.stubGlobal('useRuntimeConfig', () => ({
  public: { apiBase: 'http://localhost:8000/api/v1' },
}))

vi.stubGlobal('useAuthStore', () => ({ accessToken: null }))

// Fixtures 

const makeCartItem = (overrides = {}) => ({
  id: 1,
  product: {
    id: 10,
    name: 'Manchester United 21-22 Home Shirt',
    slug: 'manchester-united-21-22-home-shirt',
    price: '30.00',
    original_price: '89.95',
    discount_percentage: 67,
    primary_image: 'http://localhost:8000/media/products/mu.jpg',
    league_name: 'Premier League',
    category_name: 'Home Shirt',
    is_featured: true,
  },
  size: 'L',
  custom_name: null,
  custom_number: null,
  patch: null,
  quantity: 1,
  subtotal: '30.00',
  ...overrides,
})

const makeCart = (items = [makeCartItem()]) => ({
  items,
  total: items.reduce((sum, i) => sum + parseFloat(i.subtotal), 0).toFixed(2),
  count: items.length,
})

function mockFetchCart(cartData: object) {
  return vi.fn().mockResolvedValue({
    ok: true,
    status: 200,
    json: () => Promise.resolve(cartData),
  })
}

// Tests 

describe('Cart Store', () => {
  let useCartStore: typeof import('../../app/stores/cart').useCartStore

  beforeEach(async () => {
    setActivePinia(createPinia())
    vi.unstubAllGlobals()

    vi.stubGlobal('useRuntimeConfig', () => ({
      public: { apiBase: 'http://localhost:8000/api/v1' },
    }))
    vi.stubGlobal('useAuthStore', () => ({ accessToken: null }))
    Object.defineProperty(globalThis, 'process', {
      value: { client: true }, writable: true, configurable: true,
    })

    const mod = await import('../../app/stores/cart')
    useCartStore = mod.useCartStore
  })

  // Initial state 

  it('starts with empty cart and drawer closed', () => {
    const cart = useCartStore()
    expect(cart.cart.items).toEqual([])
    expect(cart.cart.count).toBe(0)
    expect(cart.cart.total).toBe('0.00')
    expect(cart.isOpen).toBe(false)
    expect(cart.loading).toBe(false)
  })

  // Getters 

  it('itemCount returns cart.count from state', () => {
    const cart = useCartStore()
    cart.cart.count = 3
    expect(cart.itemCount).toBe(3)
  })

  it('cartTotal returns cart.total string from state', () => {
    const cart = useCartStore()
    cart.cart.total = '94.50'
    expect(cart.cartTotal).toBe('94.50')
  })

  it('cartTotal is "0.00" for an empty cart', () => {
    const cart = useCartStore()
    expect(cart.cartTotal).toBe('0.00')
  })

  // toggleCart() 
  it('toggleCart opens a closed drawer', () => {
    const cart = useCartStore()
    expect(cart.isOpen).toBe(false)
    cart.toggleCart()
    expect(cart.isOpen).toBe(true)
  })

  it('toggleCart closes an open drawer', () => {
    const cart = useCartStore()
    cart.isOpen = true
    cart.toggleCart()
    expect(cart.isOpen).toBe(false)
  })

  // fetchCart() 

  it('fetchCart calls GET /cart/ and updates state', async () => {
    const cart = useCartStore()
    const cartData = makeCart([makeCartItem(), makeCartItem({ id: 2 })])
    vi.stubGlobal('fetch', mockFetchCart(cartData))

    await cart.fetchCart()

    expect(cart.cart.items).toHaveLength(2)
    expect(cart.cart.count).toBe(2)
    expect(cart.loading).toBe(false)
  })

  it('fetchCart calls the correct endpoint', async () => {
    const cart = useCartStore()
    const fetchMock = mockFetchCart(makeCart([]))
    vi.stubGlobal('fetch', fetchMock)

    await cart.fetchCart()

    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/',
      expect.objectContaining({ credentials: 'include' }),
    )
  })

  it('fetchCart resets loading to false after completion', async () => {
    const cart = useCartStore()
    vi.stubGlobal('fetch', mockFetchCart(makeCart([])))

    await cart.fetchCart()

    expect(cart.loading).toBe(false)
  })

  it('fetchCart handles network error gracefully without throwing', async () => {
    const cart = useCartStore()
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network error')))

    await expect(cart.fetchCart()).resolves.toBeUndefined()
    expect(cart.loading).toBe(false)
  })

  // addItem() 

  it('addItem posts to correct endpoint and opens drawer', async () => {
    const cart = useCartStore()
    const addedItem = makeCartItem()
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true, status: 201,
        json: () => Promise.resolve(addedItem),
      })
      .mockResolvedValueOnce({
        ok: true, status: 200,
        json: () => Promise.resolve(makeCart([addedItem])),
      })
    vi.stubGlobal('fetch', fetchMock)

    await cart.addItem({
      product_id: 10,
      size: 'L',
      quantity: 1,
    })

    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/',
      expect.objectContaining({ method: 'POST' }),
    )
    expect(cart.isOpen).toBe(true)
    expect(cart.loading).toBe(false)
  })

  it('addItem throws on API error and does not open drawer', async () => {
    const cart = useCartStore()
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false, status: 400,
      json: () => Promise.resolve({ product_id: ['Invalid product.'] }),
    }))

    await expect(
      cart.addItem({ product_id: 999, size: 'M', quantity: 1 })
    ).rejects.toBeTruthy()

    expect(cart.isOpen).toBe(false)
  })

  it('addItem sends correct JSON body', async () => {
    const cart = useCartStore()
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true, status: 201,
        json: () => Promise.resolve(makeCartItem()),
      })
      .mockResolvedValueOnce({
        ok: true, status: 200,
        json: () => Promise.resolve(makeCart([])),
      })
    vi.stubGlobal('fetch', fetchMock)

    await cart.addItem({ product_id: 10, size: 'XL', quantity: 2, patch_id: 3 })

    const [, options] = fetchMock.mock.calls[0]
    const body = JSON.parse(options.body)
    expect(body.product_id).toBe(10)
    expect(body.size).toBe('XL')
    expect(body.quantity).toBe(2)
    expect(body.patch_id).toBe(3)
  })

  // updateQuantity() 
  it('updateQuantity sends PATCH to correct item endpoint', async () => {
    const cart = useCartStore()
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ ok: true, status: 200, json: () => Promise.resolve({}) })
      .mockResolvedValueOnce({ ok: true, status: 200, json: () => Promise.resolve(makeCart([])) })
    vi.stubGlobal('fetch', fetchMock)

    await cart.updateQuantity(42, 3)

    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/42/',
      expect.objectContaining({ method: 'PATCH' }),
    )
  })

  it('updateQuantity sends the new quantity in the body', async () => {
    const cart = useCartStore()
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ ok: true, status: 200, json: () => Promise.resolve({}) })
      .mockResolvedValueOnce({ ok: true, status: 200, json: () => Promise.resolve(makeCart([])) })
    vi.stubGlobal('fetch', fetchMock)

    await cart.updateQuantity(42, 5)

    const [, options] = fetchMock.mock.calls[0]
    const body = JSON.parse(options.body)
    expect(body.quantity).toBe(5)
  })

  // removeItem() 
  it('removeItem sends DELETE to correct item endpoint', async () => {
    const cart = useCartStore()
    const item = makeCartItem({ id: 7 })
    cart.cart.items = [item]

    const fetchMock = vi.fn()
      .mockResolvedValueOnce({ ok: true, status: 204, json: () => Promise.resolve(null) })
      .mockResolvedValueOnce({ ok: true, status: 200, json: () => Promise.resolve(makeCart([])) })
    vi.stubGlobal('fetch', fetchMock)

    await cart.removeItem(7)

    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/7/',
      expect.objectContaining({ method: 'DELETE' }),
    )
  })

  it('removeItem refreshes cart state after deletion', async () => {
    const cart = useCartStore()
    cart.cart.items = [makeCartItem({ id: 7 })]

    vi.stubGlobal('fetch', vi.fn()
      .mockResolvedValueOnce({ ok: true, status: 204, json: () => Promise.resolve(null) })
      .mockResolvedValueOnce({ ok: true, status: 200, json: () => Promise.resolve(makeCart([])) }),
    )

    await cart.removeItem(7)

    expect(cart.cart.items).toHaveLength(0)
  })
})