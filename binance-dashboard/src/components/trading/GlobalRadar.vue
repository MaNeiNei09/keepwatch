<template>
  <div class="global-radar">
    <div class="radar-header">
      <span class="radar-icon">📡</span>
      <span class="radar-title">全局雷达</span>
      <span class="radar-subtitle">TOP 20 交易对检测</span>
    </div>

    <div class="radar-content">
      <div v-if="isLoading" class="loading-state">
        <div class="pulse-loader"></div>
        <span>扫描中...</span>
      </div>

      <div v-else class="radar-grid">
        <div
          v-for="item in radarData"
          :key="item.symbol"
          class="radar-item"
          :class="getItemClass(item)"
          @click="selectSymbol(item.symbol)"
        >
          <div class="item-symbol">{{ item.symbol.replace('USDT', '') }}</div>
          <div class="item-scores">
            <span class="score long" :class="{ active: item.longScore >= 8 }">
              L: {{ item.longScore }}
            </span>
            <span class="score short" :class="{ active: item.shortScore >= 8 }">
              S: {{ item.shortScore }}
            </span>
          </div>
          <div class="item-signal">{{ item.signal }}</div>
        </div>
      </div>

      <div class="radar-summary">
        <div class="summary-item long">
          <span class="summary-label">强烈做多</span>
          <span class="summary-value">{{ strongLongCount }}</span>
        </div>
        <div class="summary-item short">
          <span class="summary-label">强烈做空</span>
          <span class="summary-value">{{ strongShortCount }}</span>
        </div>
        <div class="summary-item neutral">
          <span class="summary-label">观望</span>
          <span class="summary-value">{{ neutralCount }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:5001/api'

const emit = defineEmits(['select-symbol'])

const isLoading = ref(false)
const radarData = ref([])
const refreshInterval = ref(null)

const topSymbols = [
  'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
  'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT', 'DOTUSDT', 'MATICUSDT',
  'LINKUSDT', 'UNIUSDT', 'ATOMUSDT', 'LTCUSDT', 'ETCUSDT',
  'FILUSDT', 'APTUSDT', 'ARBUSDT', 'OPUSDT', 'NEARUSDT'
]

const strongLongCount = computed(() =>
  radarData.value.filter(item => item.longScore >= 8).length
)

const strongShortCount = computed(() =>
  radarData.value.filter(item => item.shortScore >= 8).length
)

const neutralCount = computed(() =>
  radarData.value.filter(item => item.longScore < 8 && item.shortScore < 8).length
)

const getItemClass = (item) => {
  if (item.longScore >= 8) return 'strong-long'
  if (item.shortScore >= 8) return 'strong-short'
  if (item.longScore >= 6 && item.longScore > item.shortScore) return 'weak-long'
  if (item.shortScore >= 6 && item.shortScore > item.longScore) return 'weak-short'
  return 'neutral'
}

const selectSymbol = (symbol) => {
  emit('select-symbol', symbol)
}

const analyzeSymbol = async (symbol) => {
  try {
    const [tickerRes, klinesRes] = await Promise.all([
      axios.get(`${API_BASE}/ticker/24h/${symbol}`),
      axios.get(`${API_BASE}/klines/${symbol}?interval=1h&limit=200`)
    ])

    const currentPrice = parseFloat(tickerRes.data.lastPrice)
    const klines = klinesRes.data

    const analysis = analyzeKlines(klines, currentPrice)

    return {
      symbol,
      longScore: analysis.longScore,
      shortScore: analysis.shortScore,
      signal: getSignal(analysis.longScore, analysis.shortScore)
    }
  } catch (error) {
    console.error(`Failed to analyze ${symbol}:`, error)
    return {
      symbol,
      longScore: 0,
      shortScore: 0,
      signal: '--'
    }
  }
}

const analyzeKlines = (klines, currentPrice) => {
  const closes = klines.map(k => parseFloat(k[4]))
  const highs = klines.map(k => parseFloat(k[2]))
  const lows = klines.map(k => parseFloat(k[3]))

  // 箱体计算
  const period = 50
  const recentHighs = highs.slice(-period)
  const recentLows = lows.slice(-period)
  const boxUpper = Math.max(...recentHighs)
  const boxLower = Math.min(...recentLows)
  const boxRange = boxUpper - boxLower
  const pricePosition = ((currentPrice - boxLower) / boxRange * 100)

  // MACD计算
  const calcEma = (data, period) => {
    const k = 2 / (period + 1)
    let ema = data.slice(0, period).reduce((a, b) => a + b, 0) / period
    return data.map(c => { ema = c * k + ema * (1 - k); return ema })
  }
  const fastEma = calcEma(closes, 12)
  const slowEma = calcEma(closes, 26)
  const macdLine = fastEma.map((f, i) => f - slowEma[i])
  const signalLine = calcEma(macdLine.slice(26), 9)
  const histogram = macdLine.slice(26).map((m, i) => m - signalLine[i])

  // RSI计算
  const calcRSI = (data, period = 14) => {
    let gains = 0, losses = 0
    for (let i = 1; i <= period; i++) {
      const diff = data[i] - data[i - 1]
      if (diff > 0) gains += diff
      else losses -= diff
    }
    const avgGain = gains / period
    const avgLoss = losses / period
    return 100 - (100 / (1 + avgGain / avgLoss))
  }
  const rsi = calcRSI(closes.slice(-15))

  // 分型检测
  const detectBottomFractal = () => {
    if (lows.length < 3) return false
    const len = lows.length
    return lows[len - 2] < lows[len - 3] && lows[len - 2] < lows[len - 1]
  }
  const detectTopFractal = () => {
    if (highs.length < 3) return false
    const len = highs.length
    return highs[len - 2] > highs[len - 3] && highs[len - 2] > highs[len - 1]
  }

  const bottomFractal = detectBottomFractal()
  const topFractal = detectTopFractal()

  // 背驰检测
  const detectBullishDivergence = () => {
    const len = histogram.length
    if (len < 20) return false
    const recentHist = histogram.slice(-20)
    const current = recentHist[recentHist.length - 1]
    const prev = recentHist[0]
    return current > prev && current < 0
  }
  const detectBearishDivergence = () => {
    const len = histogram.length
    if (len < 20) return false
    const recentHist = histogram.slice(-20)
    const current = recentHist[recentHist.length - 1]
    const prev = recentHist[0]
    return current < prev && current > 0
  }

  const bullishDivergence = detectBullishDivergence()
  const bearishDivergence = detectBearishDivergence()

  // 计算做多得分
  let longScoreCount = 0
  if (pricePosition < 30) longScoreCount++
  if (macdLine[macdLine.length - 1] < 0) longScoreCount++
  if (pricePosition < 40 || pricePosition > 60) longScoreCount++
  if (pricePosition > 50 && pricePosition < 80) longScoreCount++
  if (bottomFractal) longScoreCount++
  if (bullishDivergence) longScoreCount++
  if (rsi < 40) longScoreCount++
  if (histogram[histogram.length - 1] > histogram[histogram.length - 2]) longScoreCount++

  // 计算做空得分
  let shortScoreCount = 0
  if (pricePosition > 70) shortScoreCount++
  if (macdLine[macdLine.length - 1] > 0) shortScoreCount++
  if (pricePosition > 60 || pricePosition < 40) shortScoreCount++
  if (pricePosition > 20 && pricePosition < 50) shortScoreCount++
  if (topFractal) shortScoreCount++
  if (bearishDivergence) shortScoreCount++
  if (rsi > 60) shortScoreCount++
  if (histogram[histogram.length - 1] < histogram[histogram.length - 2]) shortScoreCount++

  return {
    longScore: longScoreCount + 3,
    shortScore: shortScoreCount + 3
  }
}

const getSignal = (longScore, shortScore) => {
  if (longScore >= 8) return '🚀 做多'
  if (shortScore >= 8) return '📉 做空'
  if (longScore >= 6) return '📈 轻多'
  if (shortScore >= 6) return '🔻 轻空'
  return '⏸️ 观望'
}

const scanMarket = async () => {
  isLoading.value = true
  const results = await Promise.all(topSymbols.map(analyzeSymbol))
  radarData.value = results
  isLoading.value = false
}

onMounted(() => {
  scanMarket()
  refreshInterval.value = setInterval(scanMarket, 60000) // 每分钟刷新
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<style scoped>
.global-radar {
  padding: 12px;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: auto;
}

.radar-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #21262d;
}

.radar-icon {
  font-size: 16px;
}

.radar-title {
  font-size: 14px;
  font-weight: 600;
  color: #e6edf3;
}

.radar-subtitle {
  font-size: 11px;
  color: #7d8590;
  margin-left: auto;
}

.radar-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #7d8590;
  gap: 12px;
}

.pulse-loader {
  width: 32px;
  height: 32px;
  border: 3px solid #21262d;
  border-top-color: #f0b90b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.radar-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}

.radar-item {
  padding: 8px;
  background: #0d1117;
  border-radius: 6px;
  border: 1px solid #21262d;
  cursor: pointer;
  transition: all 0.15s;
}

.radar-item:hover {
  border-color: #30363d;
  transform: translateY(-1px);
}

.radar-item.strong-long {
  border-color: #3fb950;
  background: rgba(63, 185, 80, 0.1);
}

.radar-item.strong-short {
  border-color: #f85149;
  background: rgba(248, 81, 73, 0.1);
}

.radar-item.weak-long {
  border-color: #26de81;
  background: rgba(38, 222, 129, 0.05);
}

.radar-item.weak-short {
  border-color: #fc5c7d;
  background: rgba(252, 92, 125, 0.05);
}

.item-symbol {
  font-size: 11px;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 4px;
}

.item-scores {
  display: flex;
  gap: 6px;
  margin-bottom: 4px;
}

.score {
  font-size: 10px;
  color: #7d8590;
  font-family: monospace;
}

.score.long.active {
  color: #3fb950;
}

.score.short.active {
  color: #f85149;
}

.item-signal {
  font-size: 10px;
  color: #7d8590;
}

.radar-summary {
  display: flex;
  gap: 8px;
  padding-top: 8px;
  border-top: 1px solid #21262d;
}

.summary-item {
  flex: 1;
  text-align: center;
  padding: 6px;
  background: #0d1117;
  border-radius: 4px;
}

.summary-item.long {
  border-left: 2px solid #3fb950;
}

.summary-item.short {
  border-left: 2px solid #f85149;
}

.summary-item.neutral {
  border-left: 2px solid #7d8590;
}

.summary-label {
  display: block;
  font-size: 10px;
  color: #7d8590;
  margin-bottom: 2px;
}

.summary-value {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #e6edf3;
}
</style>