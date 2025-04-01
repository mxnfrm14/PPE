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
      apiBaseUrl: process.env.API_BASE_URL || 'https://ppe.tail923435.ts.net/',
    },
  },
  
  // En développement, vous pourriez toujours vouloir utiliser le proxy
  ...(process.env.NODE_ENV === 'development' ? {
    nitro: {
      devProxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          prependPath: false,
        },
      },
    },
  } : {})
})