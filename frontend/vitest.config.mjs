import { defineConfig } from 'vitest/config'
import { fileURLToPath } from 'url'
import { dirname, resolve } from 'path'
import vue from '@vitejs/plugin-vue'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: ['./tests/setup.ts'],
    environmentOptions: {
      happyDOM: {
        settings: {
          disableJavaScriptEvaluation: false,
        },
      },
    },
    server: {
      deps: {
        inline: ['@vue', '@vueuse', 'pinia', 'nuxt']
      }
    },
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      include: ['app/**/*.{ts,vue}'],
      exclude: ['app/**/*.d.ts', 'app/types/**'],
    },
  },
  resolve: {
    alias: {
      '~': resolve(__dirname, './app'),
      '@': resolve(__dirname, './app'),
      '#app': resolve(__dirname, './node_modules/nuxt/dist/app/index.mjs'),
    },
  },
})