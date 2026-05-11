// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  ssr: true,
  modules: ['@nuxt/image', '@nuxtjs/tailwindcss', 'shadcn-nuxt', '@vueuse/nuxt'],
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_API_BASE_URL,
      apiBaseUrlServer: process.env.NUXT_API_URL_SERVER,
    },
  },
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  image: {
    format: ['webp'],
  },
  imports: {
    dirs: ['~/composables/**'],
  },
  shadcn: {
    /**
     * Prefix for all the imported component.
     * @default "Ui"
     */
    prefix: '',
    /**
     * Directory that the component lives in.
     * Will respect the Nuxt aliases.
     * @link https://nuxt.com/docs/api/nuxt-config#alias
     * @default "@/components/ui"
     */
    componentDir: '@/components/ui',
  },
})
