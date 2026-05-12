<script setup lang="ts">
import { ShoppingCart, Plus, Minus, Trash2, CheckCircle } from 'lucide-vue-next'

const router = useRouter()

const loading = ref(false)
const submitting = ref(false)

const done = ref(false)
const createdOrderId = ref<number | null>(null)
const selectedClientId = ref<number | null>(null)

const notes = ref('')
const clientError = ref('')

const cartStore = useCartStore()
const errorsStore = useErrorsStore()

const { data: clients } = await useAPI<IClient[]>(CLIENTS)
const { data: products } = useAPI<Product[]>(PRODUCTS)

const toggleProduct = (product: Product) => {
  const inCart = cartStore.productInCart(product)
  if (inCart) {
    cartStore.remove(product.id)
  } else {
    cartStore.add(product, 1)
  }
}

const submit = async () => {
  clientError.value = ''
  if (!selectedClientId.value) {
    clientError.value = 'Оберіть клієнта'
    return
  }
  if (cartStore.isEmpty) {
    errorsStore.setErrors('Додайте хоча б один товар')
    return
  }
  submitting.value = true
  errorsStore.setErrors(null)
  try {
    const order = await orderAPI.create({
      client_id: selectedClientId.value,
      notes: notes.value.trim() || undefined,
      items: cartStore.toOrderItems,
    })
    createdOrderId.value = order.id
    done.value = true
    cartStore.clear()
  } catch (e) {
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="animate-fade-in space-y-6">
    <!-- Success state -->
    <div v-if="done" class="flex flex-col items-center space-y-4 py-20 text-center">
      <CheckCircle class="size-16 text-green-500" />
      <h2 class="text-2xl font-bold">Замовлення ID{{ createdOrderId }} створено!</h2>
      <p class="text-muted-foreground">Сума розрахована автоматично на основі обраних товарів.</p>
      <div class="mt-2 flex gap-3">
        <Button variant="outline" @click="router.push('/')">Переглянути замовлення</Button>
        <Button @click="done = false">Нове замовлення</Button>
      </div>
    </div>

    <template v-else>
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Нове замовлення</h1>
        <p class="mt-1 text-sm text-muted-foreground">Оберіть клієнта, додайте товари — сума порахується автоматично</p>
      </div>

      <div v-if="loading" class="space-y-3">
        <Skeleton v-for="i in 4" :key="i" class="h-16" />
      </div>

      <div v-else class="grid gap-6 lg:grid-cols-[1fr_340px]">
        <!-- Left: client + products -->
        <div class="space-y-5">
          <!-- Client -->
          <Card class="p-5">
            <h2 class="mb-3 flex items-center gap-2 text-sm font-semibold">
              <span
                class="flex size-5 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground"
                >1</span
              >
              Клієнт
            </h2>

            <Select v-model="selectedClientId">
              <SelectTrigger class="client-select min-w-48">
                <SelectValue placeholder="Оберіть клієнта " />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup v-if="clients">
                  <SelectItem v-for="client in clients" :key="client.id" :value="client.id"
                    >{{ client?.name }} - ({{ client?.email }})</SelectItem
                  >
                </SelectGroup>
              </SelectContent>
            </Select>

            <p v-if="clientError" class="mt-1 text-xs text-destructive">{{ clientError }}</p>
          </Card>

          <!-- Products grid -->
          <Card class="p-5">
            <h2 class="mb-3 flex items-center gap-2 text-sm font-semibold">
              <span
                class="flex size-5 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground"
                >2</span
              >
              Товари
              <span class="ml-1 text-xs font-normal text-muted-foreground"> ({{ cartStore.count }} обрано) </span>
            </h2>

            <div v-if="products && products.length === 0" class="py-8 text-center text-sm text-muted-foreground">
              Каталог порожній.
              <NuxtLink :to="PRODUCTS_LINK" class="text-primary underline-offset-4 hover:underline"
                >Додати товари →</NuxtLink
              >
            </div>

            <div class="grid gap-2 sm:grid-cols-2" v-if="products">
              <div
                v-for="product in products"
                :key="product.id"
                class="relative cursor-pointer rounded-md border p-3 transition-all hover:shadow-sm"
                :class="
                  cartStore.productInCart(product)
                    ? 'border-primary bg-primary/5 ring-1 ring-primary'
                    : 'border-border hover:border-muted-foreground'
                "
                @click="toggleProduct(product)"
              >
                <div class="flex items-start justify-between gap-2">
                  <div class="min-w-0 flex-1">
                    <p class="truncate text-sm font-medium">{{ product.name }}</p>
                    <p v-if="product.sku" class="font-mono text-xs text-muted-foreground">{{ product.sku }}</p>
                  </div>
                  <p class="text-sm font-semibold whitespace-nowrap">{{ formatPrice(product.price) }}</p>
                </div>

                <!-- Quantity control (shown when in cart) -->
                <div v-if="cartStore.productInCart(product)" class="mt-2 flex items-center gap-1" @click.stop>
                  <Button
                    variant="outline"
                    size="icon"
                    class="size-6"
                    @click="cartStore.setQty(product.id, (cartStore.productInCart(product)?.quantity ?? 1) - 1)"
                  >
                    <Minus class="size-3" />
                  </Button>
                  <span class="w-6 text-center text-sm font-semibold">
                    {{ cartStore.productInCart(product)?.quantity }}
                  </span>
                  <Button
                    variant="outline"
                    size="icon"
                    class="size-6"
                    @click="cartStore.setQty(product.id, (cartStore.productInCart(product)?.quantity ?? 1) + 1)"
                  >
                    <Plus class="size-3" />
                  </Button>
                </div>
              </div>
            </div>
          </Card>

          <!-- Notes -->
          <Card class="p-5">
            <h2 class="mb-3 flex items-center gap-2 text-sm font-semibold">
              <span
                class="flex size-5 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground"
                >3</span
              >
              Примітки
            </h2>
            <Textarea v-model="notes" placeholder="Коментар до замовлення (необов'язково)…" />
          </Card>
        </div>

        <!-- Right: cart summary -->
        <div class="space-y-4">
          <Card class="sticky top-20 p-5">
            <div class="mb-4 flex items-center gap-2">
              <ShoppingCart class="size-4 text-muted-foreground" />
              <h2 class="text-sm font-semibold">Кошик</h2>
            </div>

            <div v-if="cartStore.isEmpty" class="py-6 text-center text-sm text-muted-foreground">
              Натисніть на товар, щоб додати
            </div>

            <div v-else class="space-y-2">
              <div
                v-for="item in cartStore.items"
                :key="item.product.id"
                class="flex items-center justify-between gap-2 border-b py-2 last:border-0"
              >
                <div class="min-w-0 flex-1">
                  <p class="truncate text-sm font-medium">{{ item.product.name }}</p>
                  <p class="text-xs text-muted-foreground">
                    {{ formatPrice(item.product.price) }} × {{ item.quantity }}
                  </p>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-sm font-semibold">
                    {{ formatPrice(parseFloat(item.product.price) * item.quantity) }}
                  </span>
                  <Button
                    variant="ghost"
                    size="icon"
                    class="size-6 text-muted-foreground hover:text-destructive"
                    @click="cartStore.remove(item.product.id)"
                  >
                    <Trash2 class="size-3" />
                  </Button>
                </div>
              </div>

              <div class="flex items-center justify-between pt-3">
                <span class="font-semibold">Разом</span>
                <span class="text-lg font-bold">{{ formatPrice(cartStore.total) }}</span>
              </div>
              <p class="text-xs text-muted-foreground">Сума розраховується автоматично</p>
            </div>

            <Alert v-if="errorsStore.errors" variant="destructive" class="mt-3 text-xs text-nowrap">{{
              errorsStore.errors
            }}</Alert>

            <Button
              class="mt-4 w-full"
              :disabled="cartStore.isEmpty || !selectedClientId"
              :loading="submitting"
              @click="submit"
            >
              Оформити замовлення
            </Button>
          </Card>
        </div>
      </div>
    </template>
  </div>
</template>
