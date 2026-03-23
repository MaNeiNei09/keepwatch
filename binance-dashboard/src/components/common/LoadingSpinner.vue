<template>
  <div class="loading-spinner" :class="size">
    <div class="spinner"></div>
    <span v-if="text" class="loading-text">{{ text }}</span>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (v) => ['small', 'medium', 'large'].includes(v)
  },
  text: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.spinner {
  border: 3px solid #21262d;
  border-top-color: #f0b90b;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-spinner.small .spinner {
  width: 20px;
  height: 20px;
}

.loading-spinner.medium .spinner {
  width: 32px;
  height: 32px;
}

.loading-spinner.large .spinner {
  width: 48px;
  height: 48px;
}

.loading-text {
  color: #8b949e;
  font-size: 13px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>