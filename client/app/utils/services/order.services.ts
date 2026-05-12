export const orderAPI = {
  async byClient(clientId: number) {
    const { $api } = useNuxtApp()
    return await $api<Order[]>(ORDERS + CLIENT + `${clientId}`)
  },

  async get(id: number) {
    const { $api } = useNuxtApp()
    return await $api<Order>(ORDERS + `${id}`)
  },

  async create(body: OrderCreate) {
    const { $api } = useNuxtApp()
    return await $api<Order>(ORDERS, { method: 'POST', body })
  },
}
