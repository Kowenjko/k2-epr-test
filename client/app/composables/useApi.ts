/**
 * useApi — typed $fetch wrapper around the FastAPI backend.
 * Demonstrates TypeScript-first composable design with full type safety.
 */
import type { Client, ClientCreate, Product, ProductCreate, Order, OrderCreate, ApiError } from '~/types'

export function useApi() {
  const config = useRuntimeConfig()
  const base = config.public.apiBaseUrl as string

  async function request<T>(path: string, options: Parameters<typeof $fetch>[1] = {}): Promise<T> {
    return $fetch<T>(`${base}${path}`, {
      ...options,
      onResponseError({ response }) {
        const body = response._data as ApiError | undefined
        if (!body) return
        if (typeof body.detail === 'string') throw new Error(body.detail)
        if (Array.isArray(body.detail)) throw new Error(body.detail.map((e) => e.msg).join('; '))
      },
    })
  }

  const clients = {
    list: () => request<Client[]>('clients/'),
    get: (id: number) => request<Client>(`clients/${id}`),
    create: (data: ClientCreate) => request<Client>('clients/', { method: 'POST', body: data }),
  }

  const products = {
    list: () => request<Product[]>('products/'),
    get: (id: number) => request<Product>(`products/${id}`),
    create: (data: ProductCreate) => request<Product>('products/', { method: 'POST', body: data }),
  }

  const orders = {
    byClient: (clientId: number) => request<Order[]>(`orders/client/${clientId}`),
    get: (id: number) => request<Order>(`orders/${id}`),
    create: (data: OrderCreate) => request<Order>('orders/', { method: 'POST', body: data }),
  }

  return { clients, products, orders }
}
