<script lang="ts" setup>
const years = new Date().getFullYear()
</script>

<template>
  <footer class="border-t py-4 text-center text-xs text-muted-foreground">
    K2 ERP — FastAPI + Nuxt 4 + shadcn-vue -{{ years }}
  </footer>
</template>
