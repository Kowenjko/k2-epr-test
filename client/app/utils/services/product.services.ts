export const productAPI = {
  async all() {
    const { $api } = useNuxtApp()
    return await $api<Product[]>(PRODUCTS)
  },

  async get(id: number) {
    const { $api } = useNuxtApp()
    return await $api<Product>(PRODUCTS + `/${id}`)
  },

  async create(body: ProductCreate) {
    const { $api } = useNuxtApp()
    return await $api<Product>(PRODUCTS, { method: 'POST', body })
  },

  async delete(id: number) {
    const { $api } = useNuxtApp()
    return await $api<Product>(PRODUCTS + `/${id}`, { method: 'DELETE' })
  },
}
