// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  telemetry: false,
  app: {
    head: {
      title: 'KyroKart | Premium Direct E-Commerce Store',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'KyroKart - Curated products delivered directly from audited manufacturers with zero retail markups.' }
      ],
      link: [
        {
          rel: 'stylesheet',
          href: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
          crossorigin: 'anonymous'
        }
      ]
    }
  },
  runtimeConfig: {
    apiUpstream: process.env.API_UPSTREAM || '',
    public: {
      apiBase: '/api'
    }
  },
  css: [
    '~/assets/css/main.css'
  ],
  routeRules: {
    '/admin/suppliers': { redirect: { to: '/admin/products', statusCode: 302 } },
    '/admin/suppliers/**': { redirect: { to: '/admin/products', statusCode: 302 } }
  },
  devServer: {
    port: 3000,
    host: 'localhost'
  }
})
