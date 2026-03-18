<template>
  <div class="cycle-card">
    <div class="card-title">
      <span class="title-icon">📊</span>
      <span>多周期趋势</span>
    </div>
    <div class="cycle-grid">
      <div :class="['cycle-item', trend5m ? 'bullish' : 'bearish']">
        <span class="cycle-label">5M</span>
        <span class="cycle-status">{{ trend5m ? '多头' : '空头' }}</span>
      </div>
      <div :class="['cycle-item', trend15m ? 'bullish' : 'bearish']">
        <span class="cycle-label">15M</span>
        <span class="cycle-status">{{ trend15m ? '多头' : '空头' }}</span>
      </div>
      <div :class="['cycle-item', trend30m ? 'bullish' : 'bearish']">
        <span class="cycle-label">30M</span>
        <span class="cycle-status">{{ trend30m ? '多头' : '空头' }}</span>
      </div>
      <div :class="['cycle-item', trend1h ? 'bullish' : 'bearish']">
        <span class="cycle-label">1H</span>
        <span class="cycle-status">{{ trend1h ? '多头' : '空头' }}</span>
      </div>
      <div :class="['cycle-item', trend4h ? 'bullish' : 'bearish']">
        <span class="cycle-label">4H</span>
        <span class="cycle-status">{{ trend4h ? '多头' : '空头' }}</span>
      </div>
      <div :class="['cycle-item', trend1d ? 'bullish' : 'bearish']">
        <span class="cycle-label">1D</span>
        <span class="cycle-status">{{ trend1d ? '多头' : '空头' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  trend5m: { type: Boolean, default: false },
  trend15m: { type: Boolean, default: false },
  trend30m: { type: Boolean, default: false },
  trend1h: { type: Boolean, default: false },
  trend4h: { type: Boolean, default: false },
  trend1d: { type: Boolean, default: false }
})
</script>

<style scoped>
.cycle-card {
  background: linear-gradient(135deg, #1a1f2e 0%, #161b22 100%);
  border-radius: 12px;
  padding: 12px;
  border: 1px solid #21262d;
  height: 75%;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #e6edf3;
}

.title-icon {
  font-size: 14px;
}

.cycle-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
}

.cycle-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4px;
  border-radius: 4px;
  background: #0d1117;
}

.cycle-item.bullish {
  background: rgba(38, 222, 129, 0.1);
  border: 1px solid rgba(38, 222, 129, 0.3);
}

.cycle-item.bearish {
  background: rgba(252, 92, 125, 0.1);
  border: 1px solid rgba(252, 92, 125, 0.3);
}

.cycle-label {
  font-size: 9px;
  color: #8b949e;
  margin-bottom: 1px;
}

.cycle-status {
  font-size: 10px;
  font-weight: 700;
}

.cycle-item.bullish .cycle-status { color: #26de81; }
.cycle-item.bearish .cycle-status { color: #fc5c7d; }
</style>