// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  css: [
    '/public/assets/css/reset.css', // Inclure le fichier CSS global
  ],

  modules: [
    '@nuxt/icon',
    '@nuxt/ui',
    '@nuxt/eslint',
    '@nuxt/fonts'
  ],

  runtimeConfig: {
    public: {
      apiBaseUrl: '/api', // Use /api as the base URL
    },
  },
  nitro: {
    devProxy: {
      '/api': {
        target: 'http://localhost:8000', // Backend URL
        changeOrigin: true,
        prependPath: true,
      },
    },
  },
})