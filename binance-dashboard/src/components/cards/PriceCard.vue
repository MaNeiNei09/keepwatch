<template>
  <div class="price-card">
    <div class="card-header">
      <span class="coin-icon">{{ getCoinIcon(symbol) }}</span>
      <span class="coin-name">{{ formatSymbol(symbol) }}</span>
    </div>
    <div class="price-display">
      <span class="current-price">${{ formatPrice(price) }}</span>
      <span :class="['price-change', priceChangePercent >= 0 ? 'positive' : 'negative']">
        {{ priceChangePercent >= 0 ? '+' : '' }}{{ priceChangePercent || 0 }}%
      </span>
    </div>
    <div class="price-stats">
      <div class="price-stat">
        <span class="stat-label">24h高</span>
        <span class="stat-value">${{ formatPrice(highPrice) }}</span>
      </div>
      <div class="price-stat">
        <span class="stat-label">24h低</span>
        <span class="stat-value">${{ formatPrice(lowPrice) }}</span>
      </div>
      <div class="price-stat">
        <span class="stat-label">24h量</span>
        <span class="stat-value">{{ formatNumber(volume) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  symbol: { type: String, default: '' },
  price: { type: [String, Number], default: 0 },
  priceChangePercent: { type: [String, Number], default: 0 },
  highPrice: { type: [String, Number], default: 0 },
  lowPrice: { type: [String, Number], default: 0 },
  volume: { type: [String, Number], default: 0 }
})

const formatSymbol = (symbol) => {
  if (!symbol) return ''
  return symbol.replace('USDT', '/USDT')
}

const getCoinIcon = (symbol) => {
  const icons = {
    'BTC': '₿', 'ETH': 'Ξ', 'BNB': 'B', 'SOL': 'S',
    'XRP': 'X', 'ADA': 'A', 'DOGE': 'D', 'AVAX': 'A'
  }
  const base = symbol?.replace('USDT', '') || ''
  return icons[base] || '●'
}

const formatPrice = (price) => {
  if (!price) return '0.00'
  const num = parseFloat(price)
  if (num >= 1000) return num.toFixed(2)
  if (num >= 1) return num.toFixed(4)
  return num.toFixed(6)
}

const formatNumber = (num) => {
  if (!num) return '0'
  const n = parseFloat(num)
  if (n >= 1e9) return (n / 1e9).toFixed(2) + 'B'
  if (n >= 1e6) return (n / 1e6).toFixed(2) + 'M'
  if (n >= 1e3) return (n / 1e3).toFixed(2) + 'K'
  return n.toFixed(2)
}
</script>

<style scoped>
.price-card {
  background: linear-gradient(135deg, #1a1f2e 0%, #161b22 100%);
  border-radius: 12px;
  padding: 12px;
  border: 1px solid #21262d;
  height: 75%;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.coin-icon {
  font-size: 16px;
}

.coin-name {
  font-size: 14px;
  color: #e6edf3;
  font-weight: 600;
}

.price-display {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 8px;
}

.current-price {
  font-size: 20px;
  font-weight: 700;
  color: #e6edf3;
}

.price-change {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.price-change.positive {
  color: #26de81;
  background: rgba(38, 222, 129, 0.15);
}

.price-change.negative {
  color: #fc5c7d;
  background: rgba(252, 92, 125, 0.15);
}

.price-stats {
  display: flex;
  gap: 6px;
  margin-top: auto;
  padding-top: 6px;
  border-top: 1px solid #21262d;
}

.price-stat {
  flex: 1;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 9px;
  color: #8b949e;
  margin-bottom: 1px;
}

.stat-value {
  font-size: 11px;
  font-weight: 600;
  color: #e6edf3;
}
</style>