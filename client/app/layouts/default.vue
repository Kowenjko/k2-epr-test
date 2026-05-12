<script lang="ts" setup></script>

<template>
  <div class="flex min-h-screen flex-col bg-background">
    <AppHeader />

    <main class="container flex-1 py-8">
      <slot />
    </main>

    <AppFooter />
  </div>
</template>
