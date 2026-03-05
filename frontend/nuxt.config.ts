// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',

  // Nuxt 4 app directory structure
  future: {
    compatibilityVersion: 4,
  },

  devtools: { enabled: true },

  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],

  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@nuxt/image',
    '@vueuse/nuxt',
    '@nuxtjs/google-fonts',
  ],

  pinia: {
    storesDirs: ['./app/stores/**'],
  },

  googleFonts: {
    families: {
      'Barlow Condensed': [400, 600, 700, 800],
      'Montserrat': [300, 400, 500, 600, 700, 800],
      'Bebas Neue': true,
    },
    display: 'swap',
    preload: true,
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1',
      mediaBase: process.env.NUXT_PUBLIC_MEDIA_BASE || 'http://localhost:8000',
    },
  },

  app: {
    head: {
      title: 'Jambulani — Customized Club Jerseys',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content: 'Your favorite customized club jerseys. Free shipping on all orders.',
        },
      ],
      link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },
  },

  css: ['~/assets/css/main.css'],

  image: {
    domains: ['localhost'],
    format: ['webp', 'jpeg', 'png'],
  },

  typescript: {
    strict: true,
    typeCheck: false,
  },

  ssr: true,
})
