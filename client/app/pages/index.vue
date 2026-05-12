<script setup lang="ts">
import { Search, RefreshCw, ClipboardList } from 'lucide-vue-next'

const orders = ref<Order[]>([])
const selectedClientId = ref<number | null>(null)
const loading = ref(false)

const statusLabels: Record<OrderStatus, string> = {
  pending: 'Очікує',
  confirmed: 'Підтверджено',
  shipped: 'Відправлено',
  delivered: 'Доставлено',
  cancelled: 'Скасовано',
}

const statusVariants: Record<OrderStatus, string> = {
  pending: 'pending',
  confirmed: 'confirmed',
  shipped: 'shipped',
  delivered: 'delivered',
  cancelled: 'cancelled',
}

const errorsStore = useErrorsStore()
const { data: clients } = useAPI<IClient[]>(CLIENTS)

const selectedClient = computed(
  () => clients.value?.find((client: IClient) => +client.id === selectedClientId.value) ?? null,
)

const loadOrders = async () => {
  if (!selectedClientId.value) return

  try {
    loading.value = true
    orders.value = await orderAPI.byClient(selectedClientId.value)
  } catch (error) {
  } finally {
    loading.value = false
  }
}

watch(selectedClientId, async () => await loadOrders())
</script>

<template>
  <div class="animate-fade-in space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Замовлення</h1>
      <p class="mt-1 text-sm text-muted-foreground">Перегляд замовлень по клієнту</p>
    </div>

    <!-- Client selector -->
    <Card class="p-4">
      <div class="flex flex-col gap-3 sm:flex-row">
        <div class="flex-1">
          <Label for="client-select" class="mb-1.5 block">Оберіть клієнта</Label>

          <Select id="client-select" v-model="selectedClientId">
            <SelectTrigger class="client-select min-w-48">
              <SelectValue placeholder="Клієнт" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectItem v-for="client in clients" :key="client.id" :value="client.id"
                  >{{ client?.name }} - ({{ client?.email }})</SelectItem
                >
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
        <div class="flex items-end">
          <Button
            variant="outline"
            size="sm"
            :disabled="!selectedClientId || loading"
            :loading="loading"
            @click="loadOrders"
          >
            <RefreshCw class="size-4" />
            Оновити
          </Button>
        </div>
      </div>
    </Card>

    <Alert v-if="errorsStore.errors" variant="destructive" class="text-nowrap">{{ errorsStore.errors }}</Alert>

    <!-- Orders list -->
    <template v-if="selectedClientId">
      <div v-if="loading" class="space-y-3">
        <Skeleton v-for="i in 3" :key="i" class="h-24 w-full" />
      </div>

      <div v-else-if="orders && orders.length === 0" class="py-16 text-center text-muted-foreground">
        <ClipboardList class="mx-auto mb-3 size-10 opacity-30" />
        <p class="font-medium">Замовлень поки немає</p>
        <NuxtLink
          :to="NEW_ORDERS_LINK"
          class="mt-1 inline-block text-sm text-primary underline-offset-4 hover:underline"
        >
          Створити перше замовлення →
        </NuxtLink>
      </div>

      <div v-else class="space-y-3">
        <p class="text-sm text-muted-foreground">
          Знайдено {{ orders?.length }} замовл.
          <template v-if="selectedClient">
            для <strong>{{ selectedClient.name }}</strong></template
          >
        </p>

        <Card v-for="order in orders" :key="order.id" class="p-4 transition-shadow hover:shadow-md">
          <div class="flex flex-wrap items-start justify-between gap-3">
            <div class="space-y-1">
              <div class="flex items-center gap-2">
                <span class="font-mono text-sm font-semibold">ID: {{ order.id }}</span>
                <Badge :variant="statusVariants[order.status]">
                  {{ statusLabels[order.status] }}
                </Badge>
              </div>
              <p class="text-xs text-muted-foreground">{{ formatDate(order.created_at) }}</p>
              <p v-if="order.notes" class="text-sm text-muted-foreground italic">{{ order.notes }}</p>
            </div>

            <div class="text-right">
              <p class="text-lg font-bold">{{ formatPrice(order.total_amount) }}</p>
              <p class="text-xs text-muted-foreground">{{ order.items.length }} поз.</p>
            </div>
          </div>

          <!-- Items table -->
          <div v-if="order.items.length" class="mt-3 border-t pt-3">
            <div class="overflow-x-auto">
              <table class="w-full text-xs">
                <thead>
                  <tr class="text-muted-foreground">
                    <th class="pb-1 text-left font-medium">Товар</th>
                    <th class="pb-1 text-right font-medium">К-сть</th>
                    <th class="pb-1 text-right font-medium">Ціна</th>
                    <th class="pb-1 text-right font-medium">Сума</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in order.items" :key="item.id" class="border-t border-border/50">
                    <td class="py-1 pr-2">{{ item.product?.name ?? `ID${item.product_id}` }}</td>
                    <td class="py-1 text-right">{{ item.quantity }}</td>
                    <td class="py-1 text-right font-mono">{{ formatPrice(item.unit_price) }}</td>
                    <td class="py-1 text-right font-mono font-medium">{{ formatPrice(item.subtotal) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </Card>
      </div>
    </template>

    <template v-else>
      <div class="py-20 text-center text-muted-foreground">
        <Search class="mx-auto mb-3 size-10 opacity-30" />
        <p>Оберіть клієнта, щоб побачити замовлення</p>
      </div>
    </template>
  </div>
</template>
