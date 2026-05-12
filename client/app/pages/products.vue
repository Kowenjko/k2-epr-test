<script setup lang="ts">
import { PackagePlus, Package2 } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const submitting = ref(false)
const success = ref('')

const form = reactive({ name: '', description: '', price: '', sku: '' })
const errors = reactive({ name: '', price: '' })

const errorsStore = useErrorsStore()
const { data: products, pending: loading, refresh } = useAPI<Product[]>(PRODUCTS)

function validate(): boolean {
  errors.name = form.name.trim() ? '' : "Назва обов'язкова"
  errors.price = form.price && Number(form.price) > 0 ? '' : 'Ціна має бути > 0'
  return !errors.name && !errors.price
}

const submit = async () => {
  if (!validate()) return
  submitting.value = true

  success.value = ''
  try {
    const created = await productAPI.create({
      name: form.name.trim(),
      description: form.description.trim() || undefined,
      price: parseFloat(form.price).toFixed(2),
      sku: form.sku.trim() || undefined,
    })

    success.value = `Товар "${created.name}" додано`
    toast.success(success.value)
    Object.assign(form, { name: '', description: '', price: '', sku: '' })
    await refresh()
  } catch (e) {
  } finally {
    submitting.value = false
  }
}

watch(success, () => success.value && setTimeout(() => (success.value = ''), 3000))
</script>

<template>
  <div class="animate-fade-in space-y-6">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Товари</h1>
      <p class="mt-1 text-sm text-muted-foreground">Каталог товарів та їх ціни</p>
    </div>

    <div class="grid gap-6 lg:grid-cols-[380px_1fr]">
      <!-- Form -->
      <Card class="h-fit p-5">
        <div class="mb-4 flex items-center gap-2">
          <PackagePlus class="size-4 text-muted-foreground" />
          <h2 class="text-sm font-semibold">Новий товар</h2>
        </div>

        <form @submit.prevent="submit" class="space-y-4">
          <div class="space-y-1.5">
            <Label for="p-name">Назва *</Label>
            <Input id="p-name" v-model="form.name" placeholder="Ноутбук Dell XPS 15" />
            <p v-if="errors.name" class="text-xs text-destructive">{{ errors.name }}</p>
          </div>

          <div class="space-y-1.5">
            <Label for="p-price">Ціна (грн) *</Label>
            <Input id="p-price" v-model="form.price" type="number" step="0.01" min="0.01" placeholder="1999.99" />
            <p v-if="errors.price" class="text-xs text-destructive">{{ errors.price }}</p>
          </div>

          <div class="space-y-1.5">
            <Label for="p-sku">Артикул (SKU)</Label>
            <Input id="p-sku" v-model="form.sku" placeholder="DELL-XPS-001" />
          </div>

          <div class="space-y-1.5">
            <Label for="p-desc">Опис</Label>
            <Textarea id="p-desc" v-model="form.description" placeholder="Короткий опис товару…" />
          </div>

          <Alert v-if="errorsStore.errors" variant="destructive" class="text-xs text-nowrap">{{
            errorsStore.errors
          }}</Alert>
          <Alert v-if="success" variant="success" class="text-xs text-nowrap">{{ success }}</Alert>

          <Button type="submit" class="w-full" :loading="submitting">Додати товар</Button>
        </form>
      </Card>

      <!-- Products table -->
      <Card class="overflow-hidden">
        <div class="flex items-center justify-between border-b p-4">
          <div class="flex items-center gap-2">
            <Package2 class="size-4 text-muted-foreground" />
            <h2 class="text-sm font-semibold">Каталог</h2>
          </div>
          <span class="rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground">
            {{ products?.length }}
          </span>
        </div>

        <div v-if="loading" class="space-y-3 p-4">
          <Skeleton v-for="i in 5" :key="i" class="h-12" />
        </div>

        <div v-else-if="products && products.length === 0" class="p-8 text-center text-sm text-muted-foreground">
          Каталог порожній. Додайте перший товар →
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-muted/50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium tracking-wide text-muted-foreground uppercase">
                  ID
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium tracking-wide text-muted-foreground uppercase">
                  Назва
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium tracking-wide text-muted-foreground uppercase">
                  SKU
                </th>
                <th class="px-4 py-3 text-right text-xs font-medium tracking-wide text-muted-foreground uppercase">
                  Ціна
                </th>
                <th
                  class="hidden px-4 py-3 text-left text-xs font-medium tracking-wide text-muted-foreground uppercase lg:table-cell"
                >
                  Додано
                </th>
              </tr>
            </thead>
            <tbody v-if="products">
              <tr v-for="product in products" :key="product.id" class="border-t transition-colors hover:bg-muted/30">
                <td class="px-4 py-3 font-mono text-xs text-muted-foreground">{{ product.id }}</td>
                <td class="px-4 py-3">
                  <div class="font-medium">{{ product.name }}</div>
                  <div v-if="product.description" class="max-w-[200px] truncate text-xs text-muted-foreground">
                    {{ product.description }}
                  </div>
                </td>
                <td class="px-4 py-3 font-mono text-xs text-muted-foreground">{{ product.sku ?? '—' }}</td>
                <td class="px-4 py-3 text-right font-mono font-semibold">{{ formatPrice(product.price) }}</td>
                <td class="hidden px-4 py-3 text-xs text-muted-foreground lg:table-cell">
                  {{ formatDate(product.created_at) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  </div>
</template>
