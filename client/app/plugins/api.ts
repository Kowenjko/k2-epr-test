import { defineNuxtPlugin } from '#app'
import { useErrorsStore } from '@/stores/errors'
import { toast } from 'vue-sonner'

export default defineNuxtPlugin((nuxtApp) => {
  const { baseURL } = useBaseUrlApi()

  const api = $fetch.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
    },

    async onRequest() {
      const errorsStore = useErrorsStore()
      errorsStore.setErrors(null)
    },

    async onResponseError({ response }) {
      if (process.client) {
        const body = response._data as ApiError | undefined
        if (!body) return

        let message = 'An error occurred. Please try again.'
        const errorsStore = useErrorsStore()

        if (typeof body.detail === 'string') message = body.detail
        if (Array.isArray(body.detail)) message = body.detail.map((e) => e.msg).join('; ')

        errorsStore.setErrors(message)
        toast.error(message)
      }
    },
  })

  return {
    provide: { api },
  }
})
