export const clientAPI = {
  async all() {
    const { $api } = useNuxtApp()
    return await $api<Client[]>(CLIENTS)
  },

  async get(id: number) {
    const { $api } = useNuxtApp()
    return await $api<Client>(CLIENTS + `/${id}`)
  },

  async create(body: ClientCreate) {
    const { $api } = useNuxtApp()
    return await $api<Client>(CLIENTS, { method: 'POST', body })
  },

  async delete(id: number) {
    const { $api } = useNuxtApp()
    return await $api<Client>(CLIENTS + `/${id}`, { method: 'DELETE' })
  },
}
