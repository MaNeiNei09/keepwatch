<template>
  <div class="top-list">
    <div class="list-header">
      <h3>🔥 涨幅榜</h3>
      <span class="list-subtitle">24h</span>
    </div>

    <div class="list-content">
      <div
        v-for="(item, index) in items"
        :key="item.symbol"
        class="list-item"
        @click="$emit('select-symbol', item.symbol)"
      >
        <div class="item-rank">{{ index + 1 }}</div>
        <div class="item-info">
          <div class="item-symbol">{{ item.baseAsset || item.symbol.replace('USDT', '') }}</div>
          <div class="item-name">{{ item.symbol }}</div>
        </div>
        <div class="item-price">{{ formatPrice(item.price) }}</div>
        <div class="item-change positive">
          +{{ parseFloat(item.change24h).toFixed(2) }}%
        </div>
      </div>

      <div v-if="items.length === 0" class="empty-state">
        暂无数据
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

const formatPrice = (price) => {
  if (!price) return '0.00'
  const num = parseFloat(price)
  if (num >= 1000) return num.toFixed(2)
  if (num >= 1) return num.toFixed(4)
  return num.toFixed(6)
}
</script>

<style scoped>
.top-list {
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 12px;
  overflow: hidden;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #21262d;
}

.list-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: #e6edf3;
  margin: 0;
}

.list-subtitle {
  font-size: 11px;
  color: #8b949e;
  background: #21262d;
  padding: 2px 8px;
  border-radius: 4px;
}

.list-content {
  max-height: 400px;
  overflow-y: auto;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  cursor: pointer;
  transition: background 0.15s;
}

.list-item:hover {
  background: #21262d;
}

.item-rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(38, 222, 129, 0.1);
  color: #26de81;
  font-size: 12px;
  font-weight: 700;
  border-radius: 4px;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-symbol {
  font-size: 13px;
  font-weight: 600;
  color: #e6edf3;
}

.item-name {
  font-size: 11px;
  color: #8b949e;
}

.item-price {
  font-size: 12px;
  color: #e6edf3;
  font-family: monospace;
}

.item-change {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.item-change.positive {
  color: #26de81;
  background: rgba(38, 222, 129, 0.1);
}

.empty-state {
  padding: 40px 20px;
  text-align: center;
  color: #8b949e;
  font-size: 13px;
}
</style>