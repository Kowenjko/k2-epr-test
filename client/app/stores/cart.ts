import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])

  const productInCart = (product: Product) => items.value.find((item: any) => item.product.id === product.id)

  const add = (product: Product, qty = 1) => {
    const existing = productInCart(product)
    if (existing) {
      existing.quantity += qty
    } else {
      items.value.push({ product, quantity: qty })
    }
  }

  const remove = (productId: number) => {
    items.value = items.value.filter((i) => i.product.id !== productId)
  }

  const setQty = (productId: number, quantity: number) => {
    if (quantity <= 0) {
      remove(productId)
      return
    }
    const item = items.value.find((i) => i.product.id === productId)
    if (item) item.quantity = quantity
  }

  const clear = () => {
    items.value = []
  }

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + parseFloat(item.product.price) * item.quantity, 0),
  )

  const count = computed(() => items.value.reduce((sum, item) => sum + item.quantity, 0))

  const isEmpty = computed(() => items.value.length === 0)

  const toOrderItems = computed(() =>
    items.value.map((item) => ({ product_id: item.product.id, quantity: item.quantity })),
  )

  return {
    items: readonly(items),
    total,
    count,
    isEmpty,
    toOrderItems,
    add,
    remove,
    setQty,
    clear,
    productInCart,
  }
})
