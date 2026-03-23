<template>
  <div class="check-item" :class="status">
    <div class="item-header">
      <span class="item-status">
        <span v-if="status === 'pass'" class="status-icon pass">✓</span>
        <span v-else-if="status === 'fail'" class="status-icon fail">✗</span>
        <span v-else class="status-icon neutral">○</span>
      </span>
      <span class="item-title">{{ title }}</span>
      <span class="item-value">{{ value }}</span>
    </div>
    <div class="item-detail">{{ detail }}</div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  status: {
    type: String,
    default: 'neutral' // pass, fail, neutral
  },
  value: {
    type: String,
    default: '--'
  },
  detail: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.check-item {
  padding: 8px 10px;
  background: #0d1117;
  border-radius: 6px;
  border-left: 3px solid #7d8590;
  transition: all 0.15s;
}

.check-item.pass {
  border-left-color: #3fb950;
  background: rgba(63, 185, 80, 0.05);
}

.check-item.fail {
  border-left-color: #f85149;
  background: rgba(248, 81, 73, 0.05);
}

.check-item.neutral {
  border-left-color: #7d8590;
}

.item-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.item-status {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-icon {
  font-size: 12px;
  font-weight: bold;
}

.status-icon.pass {
  color: #3fb950;
}

.status-icon.fail {
  color: #f85149;
}

.status-icon.neutral {
  color: #7d8590;
}

.item-title {
  flex: 1;
  font-size: 12px;
  font-weight: 500;
  color: #e6edf3;
}

.item-value {
  font-size: 11px;
  font-weight: 600;
  color: #f0b90b;
  font-family: monospace;
}

.item-detail {
  font-size: 10px;
  color: #7d8590;
  padding-left: 26px;
}
</style>