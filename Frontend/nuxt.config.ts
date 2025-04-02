// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },

  css: [
    "/public/assets/css/reset.css", // Inclure le fichier CSS global
  ],

  modules: ["@nuxt/icon", "@nuxt/ui", "@nuxt/eslint", "@nuxt/fonts"],

  runtimeConfig: {
    public: {
      apiBaseUrl: "https://ppe.tail923435.ts.net",
    },
  },

  nitro: {
    devProxy: {
      "/api": {
        target: "https://ppe.tail923435.ts.net",
        changeOrigin: true,
        prependPath: false,
      },
    },
  },
});
