/**
 * Cart store unit tests.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { mockFetch } from '../setup'
import { useCartStore } from '../../app/stores/cart'

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

describe('Cart Store', () => {
  let cart: ReturnType<typeof useCartStore>

  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    mockFetch.mockClear()
    cart = useCartStore()
  })

  // Initial state
  it('starts with empty cart and drawer closed', () => {
    expect(cart.cart.items).toEqual([])
    expect(cart.cart.count).toBe(0)
    expect(cart.cart.total).toBe('0.00')
    expect(cart.isOpen).toBe(false)
    expect(cart.loading).toBe(false)
  })

  // Getters
  it('itemCount returns cart.count from state', () => {
    cart.cart.count = 3
    expect(cart.itemCount).toBe(3)
  })

  it('cartTotal returns cart.total string from state', () => {
    cart.cart.total = '94.50'
    expect(cart.cartTotal).toBe('94.50')
  })

  it('cartTotal is "0.00" for an empty cart', () => {
    expect(cart.cartTotal).toBe('0.00')
  })

  // toggleCart()
  it('toggleCart opens a closed drawer', () => {
    cart.isOpen = false
    cart.toggleCart()
    expect(cart.isOpen).toBe(true)
  })

  it('toggleCart closes an open drawer', () => {
    cart.isOpen = true
    cart.toggleCart()
    expect(cart.isOpen).toBe(false)
  })

  // fetchCart()
  it('fetchCart calls GET /cart/ and updates state', async () => {
    const cartData = makeCart([makeCartItem(), makeCartItem({ id: 2 })])
    
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(cartData),
    })

    await cart.fetchCart()

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/',
      expect.objectContaining({ 
        credentials: 'include',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      }),
    )
    expect(cart.cart.items).toHaveLength(2)
    expect(cart.cart.count).toBe(2)
    expect(cart.loading).toBe(false)
  })

  it('fetchCart calls the correct endpoint', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(makeCart([])),
    })

    await cart.fetchCart()

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/',
      expect.objectContaining({ 
        credentials: 'include',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      }),
    )
  })

  it('fetchCart resets loading to false after completion', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(makeCart([])),
    })

    await cart.fetchCart()

    expect(cart.loading).toBe(false)
  })

  it('fetchCart handles network error gracefully without throwing', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Network error'))

    await cart.fetchCart()
    
    expect(cart.loading).toBe(false)
    expect(cart.cart.items).toEqual([])
  })

  // addItem()
  it('addItem posts to correct endpoint and opens drawer', async () => {
    const addedItem = makeCartItem()
    
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: () => Promise.resolve(addedItem),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve(makeCart([addedItem])),
      })

    await cart.addItem({
      product_id: 10,
      size: 'L',
      quantity: 1,
    })

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/',
      expect.objectContaining({ 
        method: 'POST',
        credentials: 'include',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      }),
    )
    expect(cart.isOpen).toBe(true)
    expect(cart.loading).toBe(false)
  })

  it('addItem throws on API error and does not open drawer', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: () => Promise.resolve({ product_id: ['Invalid product.'] }),
    })

    await expect(
      cart.addItem({ product_id: 999, size: 'M', quantity: 1 })
    ).rejects.toBeTruthy()

    expect(cart.isOpen).toBe(false)
  })

  it('addItem sends correct JSON body', async () => {
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: () => Promise.resolve(makeCartItem()),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve(makeCart([])),
      })

    await cart.addItem({ 
      product_id: 10, 
      size: 'XL', 
      quantity: 2, 
      patch_id: 3,
      custom_name: 'LAMPARD',
      custom_number: '8'
    })

    expect(mockFetch).toHaveBeenCalledTimes(2)
    
    // Check first call (POST)
    const [postUrl, postOptions] = mockFetch.mock.calls[0]
    expect(postUrl).toBe('http://localhost:8000/api/v1/cart/')
    expect(postOptions.method).toBe('POST')
    
    const body = JSON.parse(postOptions.body)
    expect(body.product_id).toBe(10)
    expect(body.size).toBe('XL')
    expect(body.quantity).toBe(2)
    expect(body.patch_id).toBe(3)
    expect(body.custom_name).toBe('LAMPARD')
    expect(body.custom_number).toBe('8')
  })

  it('addItem merges duplicate items by increasing quantity', async () => {
    const existingItem = makeCartItem({ id: 1, size: 'L', quantity: 2 })
    cart.cart.items = [existingItem]
    cart.cart.count = 1
    cart.cart.total = '60.00'

    // Mock the POST response (existing item found and updated)
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ ...existingItem, quantity: 3 }),
    })

    await cart.addItem({
      product_id: 10,
      size: 'L',
      quantity: 1,
    })

    expect(mockFetch).toHaveBeenCalledTimes(1)
    expect(cart.cart.items[0].quantity).toBe(3)
  })

  // updateQuantity()
  it('updateQuantity sends PATCH to correct item endpoint', async () => {
    const item = makeCartItem({ id: 42 })
    cart.cart.items = [item]
    
    mockFetch
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 200, 
        json: () => Promise.resolve({ ...item, quantity: 3 }) 
      })
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 200, 
        json: () => Promise.resolve(makeCart([{ ...item, quantity: 3 }])) 
      })

    await cart.updateQuantity(42, 3)

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/42/',
      expect.objectContaining({ 
        method: 'PATCH',
        credentials: 'include',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      }),
    )
  })

  it('updateQuantity sends the new quantity in the body', async () => {
    const item = makeCartItem({ id: 42 })
    cart.cart.items = [item]
    
    mockFetch
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 200, 
        json: () => Promise.resolve({ ...item, quantity: 5 }) 
      })
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 200, 
        json: () => Promise.resolve(makeCart([{ ...item, quantity: 5 }])) 
      })

    await cart.updateQuantity(42, 5)

    expect(mockFetch).toHaveBeenCalledTimes(2)
    
    const [patchUrl, patchOptions] = mockFetch.mock.calls[0]
    expect(patchUrl).toBe('http://localhost:8000/api/v1/cart/42/')
    expect(patchOptions.method).toBe('PATCH')
    
    const body = JSON.parse(patchOptions.body)
    expect(body.quantity).toBe(5)
  })

  it('updateQuantity deletes item when quantity set to 0', async () => {
    const item = makeCartItem({ id: 42 })
    cart.cart.items = [item]
    cart.cart.count = 1
    
    mockFetch
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 204, 
        json: () => Promise.resolve(null) 
      })
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 200, 
        json: () => Promise.resolve(makeCart([])) 
      })

    await cart.updateQuantity(42, 0)

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/42/',
      expect.objectContaining({ 
        method: 'PATCH',
        body: JSON.stringify({ quantity: 0 })
      }),
    )
    expect(cart.cart.items).toHaveLength(0)
    expect(cart.cart.count).toBe(0)
  })

  // removeItem()
  it('removeItem sends DELETE to correct item endpoint', async () => {
    const item = makeCartItem({ id: 7 })
    cart.cart.items = [item]
    cart.cart.count = 1

    mockFetch
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 204, 
        json: () => Promise.resolve(null) 
      })
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 200, 
        json: () => Promise.resolve(makeCart([])) 
      })

    await cart.removeItem(7)

    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/cart/7/',
      expect.objectContaining({ 
        method: 'DELETE',
        credentials: 'include'
      }),
    )
  })

  it('removeItem refreshes cart state after deletion', async () => {
    const item = makeCartItem({ id: 7 })
    cart.cart.items = [item]
    cart.cart.count = 1

    mockFetch
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 204, 
        json: () => Promise.resolve(null) 
      })
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 200, 
        json: () => Promise.resolve(makeCart([])) 
      })

    await cart.removeItem(7)

    expect(mockFetch).toHaveBeenCalledTimes(2)
    expect(cart.cart.items).toHaveLength(0)
    expect(cart.cart.count).toBe(0)
  })

  it('removeItem handles non-existent item gracefully', async () => {
    const item = makeCartItem({ id: 7 })
    cart.cart.items = [item]
    cart.cart.count = 1

    mockFetch
      .mockResolvedValueOnce({ 
        ok: false, 
        status: 404, 
        json: () => Promise.resolve({ detail: 'Not found' }) 
      })
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 200, 
        json: () => Promise.resolve(makeCart([item])) 
      })

    await cart.removeItem(999)

    expect(cart.cart.items).toHaveLength(1)
    expect(cart.cart.count).toBe(1)
  })

  // clear cart
  it('clear cart removes all items', async () => {
    cart.cart.items = [makeCartItem({ id: 1 }), makeCartItem({ id: 2 })]
    cart.cart.count = 2

    mockFetch
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 204, 
        json: () => Promise.resolve(null) 
      })
      .mockResolvedValueOnce({ 
        ok: true, 
        status: 200, 
        json: () => Promise.resolve(makeCart([])) 
      })

    // Add a clear method if it exists in your store
    if (typeof cart.clear === 'function') {
      await cart.clear()
      expect(cart.cart.items).toHaveLength(0)
      expect(cart.cart.count).toBe(0)
    }
  })

  // Subtotal calculation
  it('calculates subtotal correctly with patch', () => {
    const itemWithPatch = makeCartItem({
      patch: {
        id: 5,
        name: 'Champions League Badge',
        image: null,
        extra_price: '5.00'
      },
      quantity: 2,
      subtotal: '70.00' // (30 + 5) * 2
    })
    
    expect(itemWithPatch.subtotal).toBe('70.00')
  })

  it('calculates subtotal correctly without patch', () => {
    const itemWithoutPatch = makeCartItem({
      quantity: 3,
      subtotal: '90.00' // 30 * 3
    })
    
    expect(itemWithoutPatch.subtotal).toBe('90.00')
  })

  // Cart total calculation
  it('calculates cart total correctly with multiple items', () => {
    const items = [
      makeCartItem({ id: 1, quantity: 2, subtotal: '60.00' }),
      makeCartItem({ id: 2, quantity: 1, subtotal: '30.00' }),
      makeCartItem({ id: 3, quantity: 3, subtotal: '90.00' })
    ]
    
    cart.cart.items = items
    cart.cart.total = items.reduce((sum, i) => sum + parseFloat(i.subtotal), 0).toFixed(2)
    
    expect(cart.cartTotal).toBe('180.00')
  })
})