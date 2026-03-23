<template>
  <div class="position-card">
    <div class="card-title">
      <span class="title-icon">📈</span>
      <span>持仓参考</span>
    </div>
    <div class="position-content">
      <div class="position-row">
        <span class="pos-label">多头止损</span>
        <span class="pos-value bullish">{{ rigidStopLong || '---' }}</span>
      </div>
      <div class="position-row">
        <span class="pos-label">空头止损</span>
        <span class="pos-value bearish">{{ rigidStopShort || '---' }}</span>
      </div>
      <div class="position-row">
        <span class="pos-label">目标位(高)</span>
        <span class="pos-value">{{ swingHigh || '---' }}</span>
      </div>
      <div class="position-row">
        <span class="pos-label">目标位(低)</span>
        <span class="pos-value">{{ swingLow || '---' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  rigidStopLong: { type: String, default: null },
  rigidStopShort: { type: String, default: null },
  swingHigh: { type: String, default: null },
  swingLow: { type: String, default: null }
})
</script>

<style scoped>
.position-card {
  background: linear-gradient(135deg, #1a1f2e 0%, #161b22 100%);
  border-radius: 12px;
  padding: 12px;
  border: 1px solid #21262d;
  display: flex;
  flex-direction: column;
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

.position-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.position-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 6px;
  background: #0d1117;
  border-radius: 4px;
}

.pos-label {
  color: #8b949e;
  font-size: 10px;
}

.pos-value {
  font-family: monospace;
  font-size: 10px;
  font-weight: 600;
}

.pos-value.bullish { color: #26de81; }
.pos-value.bearish { color: #fc5c7d; }
</style>