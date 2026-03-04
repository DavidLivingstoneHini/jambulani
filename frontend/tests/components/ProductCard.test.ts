/**
 * ProductCard component unit tests.
 *
 * Tests rendering logic: image vs placeholder, discount badge,
 * price display, strikethrough original price, and link href.
 */
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import type { ProductList } from '../../app/types'

import ProductCard from '../../app/components/product/ProductCard.vue'

// Fixtures 

const baseProduct: ProductList = {
  id: 1,
  name: 'Manchester United 21-22 Home Shirt',
  slug: 'manchester-united-21-22-home-shirt',
  price: '30.00',
  original_price: '89.95',
  discount_percentage: 67,
  primary_image: 'http://localhost:8000/media/products/mu.jpg',
  league_name: 'Premier League',
  category_name: 'Home Shirt',
  is_featured: true,
}

function mountCard(product: Partial<ProductList> = {}) {
  return mount(ProductCard, {
    props: { product: { ...baseProduct, ...product } },
    global: {
      stubs: {
        NuxtLink: {
          template: '<a :href="to"><slot /></a>',
          props: ['to'],
        },
      },
    },
  })
}

// Tests 

describe('ProductCard', () => {

  // Content rendering 

  it('renders the product name', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('Manchester United 21-22 Home Shirt')
  })

  it('renders the current price with euro sign', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('€30.00')
  })

  it('renders the original price when provided', () => {
    const wrapper = mountCard()
    expect(wrapper.text()).toContain('€89.95')
  })

  it('does not render original price when null', () => {
    const wrapper = mountCard({ original_price: null })
    expect(wrapper.text()).not.toContain('€89.95')
  })

  // Discount badge 
  it('shows the discount badge when discount_percentage > 0', () => {
    const wrapper = mountCard({ discount_percentage: 67 })
    expect(wrapper.text()).toContain('Save 67%')
  })

  it('hides the discount badge when discount_percentage is 0', () => {
    const wrapper = mountCard({ discount_percentage: 0, original_price: null })
    expect(wrapper.text()).not.toContain('Save')
  })

  it('discount badge reflects the correct percentage', () => {
    const wrapper = mountCard({ discount_percentage: 33 })
    expect(wrapper.text()).toContain('Save 33%')
  })

  // Image 

  it('renders an img element when primary_image is set', () => {
    const wrapper = mountCard()
    const img = wrapper.find('img')
    expect(img.exists()).toBe(true)
  })

  it('sets the correct src on the product image', () => {
    const wrapper = mountCard()
    const img = wrapper.find('img')
    expect(img.attributes('src')).toBe(
      'http://localhost:8000/media/products/mu.jpg',
    )
  })

  it('sets the correct alt text on the product image', () => {
    const wrapper = mountCard()
    const img = wrapper.find('img')
    expect(img.attributes('alt')).toBe('Manchester United 21-22 Home Shirt')
  })

  it('renders SVG placeholder when primary_image is null', () => {
    const wrapper = mountCard({ primary_image: null })
    expect(wrapper.find('img').exists()).toBe(false)
    expect(wrapper.find('svg').exists()).toBe(true)
  })

  // Original price strikethrough 
  it('applies line-through class to original price', () => {
    const wrapper = mountCard()
    const strikethrough = wrapper.find('.line-through')
    expect(strikethrough.exists()).toBe(true)
    expect(strikethrough.text()).toContain('89.95')
  })

  it('does not render line-through element when no original price', () => {
    const wrapper = mountCard({ original_price: null, discount_percentage: 0 })
    expect(wrapper.find('.line-through').exists()).toBe(false)
  })

  // Link 
  it('links to the correct product detail page', () => {
    const wrapper = mountCard()
    const link = wrapper.find('a')
    expect(link.attributes('href')).toBe(
      '/products/manchester-united-21-22-home-shirt',
    )
  })

  it('link href updates when slug changes', () => {
    const wrapper = mountCard({ slug: 'barcelona-away-shirt' })
    expect(wrapper.find('a').attributes('href')).toBe(
      '/products/barcelona-away-shirt',
    )
  })
})