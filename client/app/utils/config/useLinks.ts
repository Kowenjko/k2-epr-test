import type { RouteLocationRaw } from 'vue-router'

export const NEW_ORDERS_LINK = {
  name: 'orders-new',
} as const satisfies RouteLocationRaw

export const PRODUCTS_LINK = {
  name: 'products',
} as const satisfies RouteLocationRaw

export const CLIENTS_LINK = {
  name: 'clients',
} as const satisfies RouteLocationRaw

export const HOME_LINK = {
  name: 'index',
} as const satisfies RouteLocationRaw
