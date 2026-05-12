<script setup lang="ts">
import { UserPlus, Users } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const submitting = ref(false)
const success = ref('')

const form = reactive({ name: '', email: '', phone: '' })
const errors = reactive({ name: '', email: '', phone: '' })

const errorsStore = useErrorsStore()
const { data: clients, pending: loading, refresh } = useAPI<IClient[]>(CLIENTS, { key: 'clients' })

function validate(): boolean {
  errors.name = form.name.trim() ? '' : "Ім'я обов'язкове"
  errors.email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) ? '' : 'Невірний email'
  return !errors.name && !errors.email
}

const submit = async () => {
  if (!validate()) return
  submitting.value = true
  success.value = ''
  try {
    await clientAPI.create(form)
    success.value = `Клієнта "${form.name}" успішно створено`
    toast.success(success.value)
    Object.assign(form, { name: '', email: '', phone: '' })
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
      <h1 class="text-2xl font-bold tracking-tight">Клієнти</h1>
      <p class="mt-1 text-sm text-muted-foreground">Управління клієнтською базою</p>
    </div>

    <div class="grid gap-6 lg:grid-cols-[380px_1fr]">
      <!-- Create form -->
      <Card class="h-fit p-5">
        <div class="mb-4 flex items-center gap-2">
          <UserPlus class="size-4 text-muted-foreground" />
          <h2 class="text-sm font-semibold">Новий клієнт</h2>
        </div>

        <form @submit.prevent="submit" class="space-y-4">
          <div class="space-y-1.5">
            <Label for="name">Повне ім'я *</Label>
            <Input id="name" v-model="form.name" placeholder="Іван Петренко" />
            <p v-if="errors.name" class="text-xs text-destructive">{{ errors.name }}</p>
          </div>

          <div class="space-y-1.5">
            <Label for="email">Email *</Label>
            <Input id="email" v-model="form.email" type="email" placeholder="ivan@example.com" />
            <p v-if="errors.email" class="text-xs text-destructive">{{ errors.email }}</p>
          </div>

          <div class="space-y-1.5">
            <Label for="phone">Телефон</Label>
            <Input id="phone" v-model="form.phone" placeholder="+380501234567" />
          </div>

          <Alert v-if="errorsStore.errors" variant="destructive" class="text-xs text-nowrap">{{
            errorsStore.errors
          }}</Alert>
          <Alert v-if="success" variant="success" class="text-xs text-nowrap">{{ success }}</Alert>

          <Button type="submit" class="w-full" :loading="submitting"> Створити клієнта </Button>
        </form>
      </Card>

      <!-- Clients table -->
      <Card class="overflow-hidden">
        <div class="flex items-center justify-between border-b p-4">
          <div class="flex items-center gap-2">
            <Users class="size-4 text-muted-foreground" />
            <h2 class="text-sm font-semibold">Всі клієнти</h2>
          </div>
          <span class="rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground">
            {{ clients?.length }}
          </span>
        </div>

        <div v-if="loading" class="space-y-3 p-4">
          <Skeleton v-for="i in 5" :key="i" class="h-12" />
        </div>

        <div v-else-if="clients && clients.length === 0" class="p-8 text-center text-sm text-muted-foreground">
          Жодного клієнта. Створіть першого →
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-muted/50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium tracking-wide text-muted-foreground uppercase">
                  ID
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium tracking-wide text-muted-foreground uppercase">
                  Ім'я
                </th>
                <th class="px-4 py-3 text-left text-xs font-medium tracking-wide text-muted-foreground uppercase">
                  Email
                </th>
                <th
                  class="hidden px-4 py-3 text-left text-xs font-medium tracking-wide text-muted-foreground uppercase md:table-cell"
                >
                  Телефон
                </th>
                <th
                  class="hidden px-4 py-3 text-left text-xs font-medium tracking-wide text-muted-foreground uppercase lg:table-cell"
                >
                  Дата реєстрації
                </th>
              </tr>
            </thead>
            <tbody v-if="clients">
              <tr v-for="client in clients" :key="client.id" class="border-t transition-colors hover:bg-muted/30">
                <td class="px-4 py-3 font-mono text-xs text-muted-foreground">{{ client?.id }}</td>
                <td class="px-4 py-3 font-medium">{{ client?.name }}</td>
                <td class="px-4 py-3 text-muted-foreground">{{ client?.email }}</td>
                <td class="hidden px-4 py-3 text-muted-foreground md:table-cell">{{ client?.phone ?? '—' }}</td>
                <td class="hidden px-4 py-3 text-xs text-muted-foreground lg:table-cell">
                  {{ formatDate(client?.created_at) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  </div>
</template>
