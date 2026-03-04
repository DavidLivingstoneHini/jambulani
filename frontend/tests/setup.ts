import { config } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, vi } from 'vitest'

// Fresh Pinia before every test — prevents state leaking between tests
beforeEach(() => {
  setActivePinia(createPinia())
})

// Stub NuxtLink so components don't need the full Nuxt router
config.global.stubs = {
  NuxtLink: {
    template: '<a :href="to"><slot /></a>',
    props: ['to'],
  },
}

// Silence expected console noise from store error paths
vi.spyOn(console, 'error').mockImplementation(() => {})
vi.spyOn(console, 'warn').mockImplementation(() => {})