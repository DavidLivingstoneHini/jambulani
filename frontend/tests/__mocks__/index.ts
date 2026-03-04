// Global mocks for all tests
import { vi } from 'vitest'

// Mock fetch
export const mockFetch = vi.fn()
global.fetch = mockFetch

// Mock useApi
export const mockApiFetch = vi.fn()
vi.mock('../../app/composables/useApi', () => ({
  useApi: () => ({ apiFetch: mockApiFetch }),
}))

// Mock auth store
vi.mock('../../app/stores/auth', () => ({
  useAuthStore: vi.fn(() => ({ 
    accessToken: null,
    user: null,
    isAuthenticated: false,
    loading: false,
    initialized: false
  })),
}))

// Mock Nuxt composables
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
}))