<template>
  <div class="app-layout">
    <AppHeader />
    <main class="app-main">
      <slot></slot>
    </main>
  </div>
</template>

<script setup>
import AppHeader from './AppHeader.vue'
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-main {
  flex: 1;
  overflow-y: auto;
}
</style>