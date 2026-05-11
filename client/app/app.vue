<script lang="ts" setup>
import { Toaster } from '@/components/ui/sonner'

useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - K2 EPR` : 'K2 EPR'
  },
})
</script>
<template>
  <NuxtLayout>
    <NuxtPage />
    <ClientOnly>
      <Toaster position="top-right" />
    </ClientOnly>
  </NuxtLayout>
</template>
