export interface IClient {
  id: number
  name: string
  email: string
  phone: string | null
  created_at: string
}

export interface ClientCreate {
  name: string
  email: string
  phone?: string
}

export interface Product {
  id: number
  name: string
  description: string | null
  price: string
  sku: string | null
  created_at: string
}

export interface ProductCreate {
  name: string
  description?: string
  price: string
  sku?: string
}

export interface OrderItemCreate {
  product_id: number
  quantity: number
}

export interface OrderCreate {
  client_id: number
  notes?: string
  items: OrderItemCreate[]
}

export interface OrderItem {
  id: number
  product_id: number
  quantity: number
  unit_price: string
  subtotal: string
  product: Product | null
}

export type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled'

export interface Order {
  id: number
  client_id: number
  status: OrderStatus
  total_amount: string
  notes: string | null
  created_at: string
  updated_at: string
  client: IClient | null
  items: OrderItem[]
}

export interface ApiError {
  detail: string | { msg: string; type: string }[]
}

export interface CartItem {
  product: Product
  quantity: number
}
