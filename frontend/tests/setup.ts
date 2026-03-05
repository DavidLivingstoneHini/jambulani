import { config } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, afterEach, vi } from 'vitest'

// Mock process.env for Pinia
vi.stubGlobal('process', {
  ...process,
  env: {
    ...process.env,
    NODE_ENV: 'test'
  }
})

// Create mock fetch
export const mockFetch = vi.fn()
global.fetch = mockFetch

// Mock localStorage
export const localStorageMock = (() => {
  let store: Record<string, string> = {}
  
  return {
    getItem: vi.fn((key: string) => store[key] || null),
    setItem: vi.fn((key: string, value: string) => {
      store[key] = value.toString()
    }),
    removeItem: vi.fn((key: string) => {
      delete store[key]
    }),
    clear: vi.fn(() => {
      store = {}
    }),
    key: vi.fn((index: number) => Object.keys(store)[index] || null),
    get length() {
      return Object.keys(store).length
    },
  }
})()

Object.defineProperty(global, 'localStorage', { 
  value: localStorageMock,
  writable: true 
})

// Mock Nuxt composables - FIXED VERSION
vi.mock('#app', () => ({
  useRuntimeConfig: () => ({
    public: {
      apiBase: 'http://localhost:8000/api/v1',
      mediaBase: 'http://localhost:8000',
    }
  }),
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
    forward: vi.fn(),
  }),
  useRoute: () => ({
    path: '/',
    fullPath: '/',
    query: {},
    params: {},
    hash: '',
  }),
  navigateTo: vi.fn(),
  defineNuxtRouteMiddleware: vi.fn(),
}))

// Mock useApi composable
vi.mock('~/composables/useApi', () => ({
  useApi: () => ({
    apiFetch: vi.fn(),
    baseURL: 'http://localhost:8000/api/v1'
  })
}))

// Mock console methods
vi.spyOn(console, 'error').mockImplementation(() => {})
vi.spyOn(console, 'warn').mockImplementation(() => {})
vi.spyOn(console, 'log').mockImplementation(() => {})
vi.spyOn(console, 'info').mockImplementation(() => {})

// Fresh Pinia before every test
beforeEach(() => {
  const pinia = createPinia()
  setActivePinia(pinia)
  vi.clearAllMocks()
  mockFetch.mockClear()
  localStorageMock.clear()
})

afterEach(() => {
  vi.restoreAllMocks()
})

// Stub NuxtLink component
config.global.stubs = {
  NuxtLink: {
    template: '<a :href="to"><slot /></a>',
    props: ['to'],
  },
}