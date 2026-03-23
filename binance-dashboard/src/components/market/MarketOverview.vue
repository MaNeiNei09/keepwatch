<template>
  <div class="market-overview">
    <div class="overview-grid">
      <div class="metric-card">
        <div class="metric-icon">💰</div>
        <div class="metric-content">
          <div class="metric-label">总市值</div>
          <div class="metric-value">${{ formatLargeNumber(metrics.totalMarketCap) }}</div>
          <div :class="['metric-change', changeClass]">
            {{ formatChange(metrics.marketCapChangePercentage24h) }}
          </div>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon">📈</div>
        <div class="metric-content">
          <div class="metric-label">24h 交易量</div>
          <div class="metric-value">${{ formatLargeNumber(metrics.totalVolume24h) }}</div>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon">₿</div>
        <div class="metric-content">
          <div class="metric-label">BTC 主导率</div>
          <div class="metric-value">{{ metrics.btcDominance?.toFixed(1) || '0' }}%</div>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon">Ξ</div>
        <div class="metric-content">
          <div class="metric-label">ETH 主导率</div>
          <div class="metric-value">{{ metrics.ethDominance?.toFixed(1) || '0' }}%</div>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon">🪙</div>
        <div class="metric-content">
          <div class="metric-label">活跃币种</div>
          <div class="metric-value">{{ formatLargeNumber(metrics.activeCryptocurrencies) }}</div>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon">⏰</div>
        <div class="metric-content">
          <div class="metric-label">最后更新</div>
          <div class="metric-value small">{{ lastUpdatedTime }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  metrics: {
    type: Object,
    default: () => ({})
  }
})

const formatLargeNumber = (num) => {
  if (!num) return '0'
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return num.toFixed(2)
}

const formatChange = (change) => {
  if (!change) return '0.00%'
  const num = parseFloat(change)
  const sign = num >= 0 ? '+' : ''
  return `${sign}${num.toFixed(2)}%`
}

const changeClass = computed(() => {
  const change = parseFloat(props.metrics.marketCapChangePercentage24h)
  if (change > 0) return 'positive'
  if (change < 0) return 'negative'
  return 'neutral'
})

const lastUpdatedTime = computed(() => {
  if (!props.metrics.lastUpdated) return '--'
  return new Date(props.metrics.lastUpdated).toLocaleTimeString('zh-CN')
})
</script>

<style scoped>
.market-overview {
  margin-bottom: 20px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
}

@media (max-width: 1200px) {
  .overview-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .overview-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.metric-card {
  background: linear-gradient(135deg, #1a1f2e 0%, #161b22 100%);
  border: 1px solid #21262d;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.metric-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(240, 185, 11, 0.1);
  border-radius: 8px;
}

.metric-content {
  flex: 1;
}

.metric-label {
  font-size: 11px;
  color: #8b949e;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 16px;
  font-weight: 700;
  color: #e6edf3;
}

.metric-value.small {
  font-size: 13px;
  font-weight: 500;
}

.metric-change {
  font-size: 11px;
  font-weight: 600;
  margin-top: 2px;
}

.metric-change.positive { color: #26de81; }
.metric-change.negative { color: #fc5c7d; }
.metric-change.neutral { color: #8b949e; }
</style>