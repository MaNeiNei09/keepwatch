<template>
  <div class="market-heatmap">
    <div class="heatmap-header">
      <h3>🗺️ 市场热力图</h3>
      <span class="heatmap-legend">
        <span class="legend-item positive">涨</span>
        <span class="legend-item negative">跌</span>
      </span>
    </div>

    <div class="heatmap-grid">
      <div
        v-for="item in items"
        :key="item.symbol"
        class="heatmap-cell"
        :style="cellStyle(item)"
        @click="$emit('select-symbol', item.symbol)"
      >
        <div class="cell-symbol">{{ item.baseAsset || item.symbol.replace('USDT', '') }}</div>
        <div class="cell-change">{{ formatChange(item.change24h) }}</div>
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

const formatChange = (change) => {
  if (!change) return '0%'
  const num = parseFloat(change)
  const sign = num >= 0 ? '+' : ''
  return `${sign}${num.toFixed(1)}%`
}

const cellStyle = (item) => {
  const change = parseFloat(item.change24h) || 0
  let bgColor

  if (change > 0) {
    const intensity = Math.min(Math.abs(change) / 20, 1)
    bgColor = `rgba(38, 222, 129, ${0.2 + intensity * 0.6})`
  } else {
    const intensity = Math.min(Math.abs(change) / 20, 1)
    bgColor = `rgba(252, 92, 125, ${0.2 + intensity * 0.6})`
  }

  return {
    backgroundColor: bgColor
  }
}
</script>

<style scoped>
.market-heatmap {
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 12px;
  padding: 16px;
}

.heatmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.heatmap-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: #e6edf3;
  margin: 0;
}

.heatmap-legend {
  display: flex;
  gap: 8px;
}

.legend-item {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 3px;
}

.legend-item.positive {
  background: rgba(38, 222, 129, 0.3);
  color: #26de81;
}

.legend-item.negative {
  background: rgba(252, 92, 125, 0.3);
  color: #fc5c7d;
}

.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

@media (max-width: 768px) {
  .heatmap-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.heatmap-cell {
  padding: 12px 8px;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}

.heatmap-cell:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.cell-symbol {
  font-size: 12px;
  font-weight: 700;
  color: #e6edf3;
  margin-bottom: 4px;
}

.cell-change {
  font-size: 11px;
  font-weight: 600;
  color: #e6edf3;
}
</style>