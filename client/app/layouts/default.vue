<script lang="ts" setup>
import { Package2, Users, ShoppingCart, ClipboardList } from 'lucide-vue-next'

const route = useRoute()

const nav = [
  { to: '/', label: 'Замовлення', icon: ClipboardList },
  { to: '/clients', label: 'Клієнти', icon: Users },
  { to: '/products', label: 'Товари', icon: Package2 },
  { to: '/orders/new', label: 'Нове замовлення', icon: ShoppingCart },
]
</script>

<template>
  <div class="flex min-h-screen flex-col bg-background">
    <!-- Top nav -->
    <header class="top-0 z-40 border-b">
      <div class="container flex h-14 items-center gap-4 px-4">
        <NuxtLink to="/" class="flex items-center gap-2 text-sm font-semibold">
          <Package2 class="size-5" />
          <span class="hidden sm:inline">K2 ERP</span>
        </NuxtLink>

        <nav class="ml-4 flex items-center gap-1">
          <NuxtLink
            v-for="item in nav"
            :key="item.to"
            :to="item.to"
            class="flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm transition-colors"
            :class="
              route.path === item.to
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

    <!-- Page content -->
    <main class="container flex-1 py-8">
      <slot />
    </main>

    <footer class="border-t py-4 text-center text-xs text-muted-foreground">
      K2 ERP — FastAPI + Nuxt 4 + shadcn-vue
    </footer>
  </div>
</template>
