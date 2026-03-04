/**
 * AppFooter component unit tests.
 */
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { setActivePinia, createPinia } from 'pinia'
import AppFooter from '../../app/components/layout/AppFooter.vue'

// Create a mock for apiFetch
const mockApiFetch = vi.fn()

// Mock useApi before importing the component
vi.mock('../../app/composables/useApi', () => ({
  useApi: () => ({
    apiFetch: mockApiFetch
  })
}))

// Helper
function mountFooter() {
  return mount(AppFooter, {
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

describe('AppFooter — Newsletter', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    mockApiFetch.mockClear()
  })

  it('renders the email input field', () => {
    const wrapper = mountFooter()
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
  })

  it('renders the subscribe button', () => {
    const wrapper = mountFooter()
    expect(wrapper.find('button').exists()).toBe(true)
  })

  it('shows success message after successful subscription', async () => {
    mockApiFetch.mockResolvedValueOnce({})
    const wrapper = mountFooter()

    await wrapper.find('input[type="email"]').setValue('fan@jambulani.com')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('Successfully subscribed!')
  })

  it('clears the email input after successful subscription', async () => {
    mockApiFetch.mockResolvedValueOnce({})
    const wrapper = mountFooter()
    const input = wrapper.find('input[type="email"]')

    await input.setValue('fan@jambulani.com')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect((input.element as HTMLInputElement).value).toBe('')
  })

  it('calls apiFetch with the correct endpoint and email', async () => {
    mockApiFetch.mockResolvedValueOnce({})
    const wrapper = mountFooter()

    await wrapper.find('input[type="email"]').setValue('fan@jambulani.com')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(mockApiFetch).toHaveBeenCalledWith('/newsletter/subscribe/', {
      method: 'POST',
      body: JSON.stringify({ email: 'fan@jambulani.com' }),
    })
  })

  it('shows the API error message on failure', async () => {
    mockApiFetch.mockRejectedValueOnce({
      data: { email: ['This email is already subscribed.'] },
    })
    const wrapper = mountFooter()

    await wrapper.find('input[type="email"]').setValue('existing@jambulani.com')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('This email is already subscribed.')
  })

  it('shows fallback error message when API returns no detail', async () => {
    mockApiFetch.mockRejectedValueOnce({})
    const wrapper = mountFooter()

    await wrapper.find('input[type="email"]').setValue('x@x.com')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('Something went wrong.')
  })

  it('does not call API when email input is empty', async () => {
    const wrapper = mountFooter()

    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(mockApiFetch).not.toHaveBeenCalled()
  })

  it('does not call API when email is only whitespace', async () => {
    const wrapper = mountFooter()

    await wrapper.find('input[type="email"]').setValue('   ')
    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(mockApiFetch).not.toHaveBeenCalled()
  })

  it('renders all four footer column headings', () => {
    const wrapper = mountFooter()
    const text = wrapper.text()
    expect(text).toContain('Main Menu')
    expect(text).toContain('Secondary Menu')
    expect(text).toContain('Subscribe')
    expect(text).toContain('Follow Us')
  })

  it('renders copyright notice', () => {
    const wrapper = mountFooter()
    expect(wrapper.text()).toContain('Jambulani')
  })
})