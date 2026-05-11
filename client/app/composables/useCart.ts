/**
 * useCart — reactive shopping cart for building orders.
 * Uses Nuxt's useState for SSR-safe global state.
 */
import type { Product, CartItem } from "~/types";

export function useCart() {
  const items = useState<CartItem[]>("cart", () => []);

  function add(product: Product, qty = 1): void {
    const existing = items.value.find((i) => i.product.id === product.id);
    if (existing) {
      existing.quantity += qty;
    } else {
      items.value.push({ product, quantity: qty });
    }
  }

  function remove(productId: number): void {
    items.value = items.value.filter((i) => i.product.id !== productId);
  }

  function setQty(productId: number, quantity: number): void {
    if (quantity <= 0) { remove(productId); return; }
    const item = items.value.find((i) => i.product.id === productId);
    if (item) item.quantity = quantity;
  }

  function clear(): void {
    items.value = [];
  }

  const total = computed(() =>
    items.value.reduce(
      (sum, i) => sum + parseFloat(i.product.price) * i.quantity, 0
    )
  );

  const count = computed(() =>
    items.value.reduce((sum, i) => sum + i.quantity, 0)
  );

  const isEmpty = computed(() => items.value.length === 0);

  const toOrderItems = computed(() =>
    items.value.map((i) => ({ product_id: i.product.id, quantity: i.quantity }))
  );

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
  };
}
