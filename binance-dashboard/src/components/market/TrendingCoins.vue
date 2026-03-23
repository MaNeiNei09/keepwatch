<template>
  <div class="trending-coins">
    <div class="trending-header">
      <h3>🔥 热门币种</h3>
    </div>

    <div class="trending-list">
      <div
        v-for="item in items"
        :key="item.symbol"
        class="trending-item"
        @click="$emit('select-symbol', item.symbol)"
      >
        <div class="item-rank">{{ item.rank }}</div>
        <div class="item-icon">{{ getIcon(item.symbol) }}</div>
        <div class="item-info">
          <div class="item-name">{{ item.name }}</div>
          <div class="item-symbol">{{ item.symbol }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

defineEmits(['select-symbol'])

const getIcon = (symbol) => {
  const icons = {
    'BTCUSDT': '₿',
    'ETHUSDT': 'Ξ',
    'BNBUSDT': 'B',
    'SOLUSDT': 'S',
    'XRPUSDT': 'X',
    'ADAUSDT': 'A',
    'DOGEUSDT': '🐕',
    'PEPEUSDT': '🐸',
    'WIFUSDT': '🐕',
    'AVAXUSDT': 'A'
  }
  return icons[symbol] || '●'
}
</script>

<style scoped>
.trending-coins {
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 12px;
  overflow: hidden;
}

.trending-header {
  padding: 12px 16px;
  border-bottom: 1px solid #21262d;
}

.trending-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: #e6edf3;
  margin: 0;
}

.trending-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px;
}

.trending-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #21262d;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
}

.trending-item:hover {
  background: #30363d;
}

.item-rank {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(240, 185, 11, 0.2);
  color: #f0b90b;
  font-size: 11px;
  font-weight: 700;
  border-radius: 4px;
}

.item-icon {
  font-size: 18px;
}

.item-info {
  display: flex;
  flex-direction: column;
}

.item-name {
  font-size: 12px;
  font-weight: 600;
  color: #e6edf3;
}

.item-symbol {
  font-size: 10px;
  color: #8b949e;
}
</style>