<script lang="ts" setup>
import { Package2, Users, ShoppingCart, ClipboardList } from 'lucide-vue-next'

const route = useRoute()

const nav = [
  { to: HOME_LINK, label: 'Замовлення', icon: ClipboardList },
  { to: CLIENTS_LINK, label: 'Клієнти', icon: Users },
  { to: PRODUCTS_LINK, label: 'Товари', icon: Package2 },
  { to: NEW_ORDERS_LINK, label: 'Нове замовлення', icon: ShoppingCart },
]
</script>

<template>
  <header class="top-0 z-40 border-b">
    <div class="container flex h-14 items-center gap-4 px-4">
      <NuxtLink to="/" class="flex items-center gap-2 text-sm font-semibold">
        <Package2 class="size-5" />
        <span class="hidden sm:inline">K2 ERP</span>
      </NuxtLink>

      <nav class="ml-4 flex items-center gap-1">
        <NuxtLink
          v-for="item in nav"
          :key="item.to.name"
          :to="item.to"
          class="flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm transition-colors"
          :class="
            route.name === item.to.name
              ? 'bg-accent font-medium text-accent-foreground'
              : 'text-muted-foreground hover:bg-accent hover:text-foreground'
          "
        >
          <component :is="item.icon" class="size-4" />
          <span class="hidden md:inline">{{ item.label }}</span>
        </NuxtLink>
      </nav>
    </div>
  </header>
</template>
