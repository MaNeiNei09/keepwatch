<template>
  <div class="trading-checklist">
    <div class="checklist-header">
      <h2>🎯 三维共振交易检测</h2>
      <div class="symbol-selector">
        <select v-model="selectedSymbol" @change="onSymbolChange">
          <option v-for="s in symbols" :key="s" :value="s">{{ s.replace('USDT', '') }}</option>
        </select>
        <span class="current-price" v-if="currentPrice">
          当前价格: <span :class="priceChangeClass">${{ currentPrice.toFixed(2) }}</span>
          <span class="price-change" :class="priceChangeClass">{{ priceChange >= 0 ? '+' : '' }}{{ priceChange.toFixed(2) }}%</span>
        </span>
      </div>
      <button class="analyze-btn" @click="runAnalysis" :disabled="isAnalyzing">
        {{ isAnalyzing ? '分析中...' : '🔍 开始检测' }}
      </button>
    </div>

    <div class="checklist-content">
      <div v-if="isAnalyzing" class="loading-overlay">
        <div class="pulse-loader"></div>
        <span>正在分析市场结构...</span>
      </div>

      <template v-else>
        <!-- 核心逻辑架构说明 -->
        <div class="logic-architecture">
          <div class="logic-item">
            <span class="logic-icon">🏛️</span>
            <div class="logic-content">
              <span class="logic-title">箱体 (The Box)</span>
              <span class="logic-desc">解决"在哪里战" - 识别供需区间，确定支撑与阻力</span>
            </div>
          </div>
          <div class="logic-item">
            <span class="logic-icon">📐</span>
            <div class="logic-content">
              <span class="logic-title">斐波那契 (Fibonacci)</span>
              <span class="logic-desc">解决"在哪进场" - 寻找高概率的回撤/反弹位</span>
            </div>
          </div>
          <div class="logic-item">
            <span class="logic-icon">🔬</span>
            <div class="logic-content">
              <span class="logic-title">缠论 (Chan Theory)</span>
              <span class="logic-desc">解决"何时开枪" - 精准捕捉转折点</span>
            </div>
          </div>
        </div>

        <!-- 左右分栏：做多/决策/做空 -->
        <div class="checklist-grid">
          <!-- 做多检查清单 -->
          <div class="checklist-panel long">
            <div class="panel-header">
              <h3>🟢 做多检测清单</h3>
              <div class="score-badge" :class="longScoreClass">
                {{ longScore }}/{{ longTotal }}
              </div>
            </div>
            <LongChecklist
              :analysis-data="analysisData"
              :current-price="currentPrice"
              :klines="klines"
            />
          </div>

          <!-- 决策建议 -->
          <div class="checklist-panel decision">
            <DecisionPanel
              :long-score="longScore"
              :short-score="shortScore"
              :analysis-data="analysisData"
              :current-price="currentPrice"
            />
          </div>

          <!-- 做空检查清单 -->
          <div class="checklist-panel short">
            <div class="panel-header">
              <h3>🔴 做空检测清单</h3>
              <div class="score-badge" :class="shortScoreClass">
                {{ shortScore }}/{{ shortTotal }}
              </div>
            </div>
            <ShortChecklist
              :analysis-data="analysisData"
              :current-price="currentPrice"
              :klines="klines"
            />
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import LongChecklist from '@/components/trading/LongChecklist.vue'
import ShortChecklist from '@/components/trading/ShortChecklist.vue'
import DecisionPanel from '@/components/trading/DecisionPanel.vue'

const API_BASE = 'http://localhost:5001/api'

const symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT']
const selectedSymbol = ref('BTCUSDT')
const isAnalyzing = ref(false)
const currentPrice = ref(0)
const priceChange = ref(0)
const klines = ref([])
const analysisData = ref({})

const longScore = computed(() => analysisData.value.longScore || 0)
const shortScore = computed(() => analysisData.value.shortScore || 0)
const longTotal = 12
const shortTotal = 12

const longScoreClass = computed(() => {
  const ratio = longScore.value / longTotal
  if (ratio >= 0.7) return 'high'
  if (ratio >= 0.4) return 'medium'
  return 'low'
})

const shortScoreClass = computed(() => {
  const ratio = shortScore.value / shortTotal
  if (ratio >= 0.7) return 'high'
  if (ratio >= 0.4) return 'medium'
  return 'low'
})

const priceChangeClass = computed(() => {
  return priceChange.value >= 0 ? 'positive' : 'negative'
})

const onSymbolChange = () => {
  runAnalysis()
}

const fetchData = async () => {
  try {
    const [tickerRes, klinesRes] = await Promise.all([
      axios.get(`${API_BASE}/ticker/24h/${selectedSymbol.value}`),
      axios.get(`${API_BASE}/klines/${selectedSymbol.value}?interval=1h&limit=200`)
    ])

    currentPrice.value = parseFloat(tickerRes.data.lastPrice)
    priceChange.value = parseFloat(tickerRes.data.priceChangePercent)
    klines.value = klinesRes.data
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

const runAnalysis = async () => {
  isAnalyzing.value = true
  await fetchData()

  // 执行三维共振分析
  analysisData.value = analyzeMarket()

  isAnalyzing.value = false
}

const analyzeMarket = () => {
  const closes = klines.value.map(k => parseFloat(k[4]))
  const highs = klines.value.map(k => parseFloat(k[2]))
  const lows = klines.value.map(k => parseFloat(k[3]))

  // 计算箱体
  const period = 50
  const recentHighs = highs.slice(-period)
  const recentLows = lows.slice(-period)
  const boxUpper = Math.max(...recentHighs)
  const boxLower = Math.min(...recentLows)
  const boxMid = (boxUpper + boxLower) / 2
  const boxRange = boxUpper - boxLower

  // 当前价格在箱体中的位置
  const pricePosition = ((currentPrice.value - boxLower) / boxRange * 100)

  // 斐波那契水平
  const fibLevels = {
    level_0: boxLower,
    level_236: boxLower + boxRange * 0.236,
    level_382: boxLower + boxRange * 0.382,
    level_5: boxLower + boxRange * 0.5,
    level_618: boxLower + boxRange * 0.618,
    level_786: boxLower + boxRange * 0.786,
    level_1: boxUpper
  }

  // 计算MACD
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

  // RSI
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

  // 底分型检测
  const detectBottomFractal = () => {
    if (lows.length < 3) return false
    const len = lows.length
    return lows[len - 2] < lows[len - 3] && lows[len - 2] < lows[len - 1]
  }

  // 顶分型检测
  const detectTopFractal = () => {
    if (highs.length < 3) return false
    const len = highs.length
    return highs[len - 2] > highs[len - 3] && highs[len - 2] > highs[len - 1]
  }

  // 背驰检测
  const detectBullishDivergence = () => {
    const len = histogram.length
    if (len < 20) return false
    const recentHist = histogram.slice(-20)
    const current = recentHist[recentHist.length - 1]
    const prev = recentHist[0]
    return current > prev && current < 0 // 底背驰
  }

  const detectBearishDivergence = () => {
    const len = histogram.length
    if (len < 20) return false
    const recentHist = histogram.slice(-20)
    const current = recentHist[recentHist.length - 1]
    const prev = recentHist[0]
    return current < prev && current > 0 // 顶背驰
  }

  const bottomFractal = detectBottomFractal()
  const topFractal = detectTopFractal()
  const bullishDivergence = detectBullishDivergence()
  const bearishDivergence = detectBearishDivergence()

  // 计算做多得分
  let longScoreCount = 0
  // 箱体定位
  if (pricePosition < 30) longScoreCount++
  // 大级别中枢
  if (macdLine[macdLine.length - 1] < 0) longScoreCount++
  // 斐波那契位置
  if (pricePosition < 40 || pricePosition > 60) longScoreCount++
  // 黄金坑位
  if (pricePosition > 50 && pricePosition < 80) longScoreCount++
  // 共振验证
  if (Math.abs(currentPrice.value - fibLevels.level_618) / fibLevels.level_618 < 0.02) longScoreCount++
  // 底分型
  if (bottomFractal) longScoreCount++
  // 背驰
  if (bullishDivergence) longScoreCount++
  // RSI
  if (rsi < 40) longScoreCount++
  // MACD趋势
  if (histogram[histogram.length - 1] > histogram[histogram.length - 2]) longScoreCount++

  // 计算做空得分
  let shortScoreCount = 0
  if (pricePosition > 70) shortScoreCount++
  if (macdLine[macdLine.length - 1] > 0) shortScoreCount++
  if (pricePosition > 60 || pricePosition < 40) shortScoreCount++
  if (pricePosition > 20 && pricePosition < 50) shortScoreCount++
  if (Math.abs(currentPrice.value - fibLevels.level_618) / fibLevels.level_618 < 0.02) shortScoreCount++
  if (topFractal) shortScoreCount++
  if (bearishDivergence) shortScoreCount++
  if (rsi > 60) shortScoreCount++
  if (histogram[histogram.length - 1] < histogram[histogram.length - 2]) shortScoreCount++

  return {
    box: { upper: boxUpper, lower: boxLower, mid: boxMid, range: boxRange, pricePosition },
    fib: fibLevels,
    macd: { line: macdLine[macdLine.length - 1], histogram: histogram[histogram.length - 1] },
    rsi,
    fractal: { bottom: bottomFractal, top: topFractal },
    divergence: { bullish: bullishDivergence, bearish: bearishDivergence },
    longScore: longScoreCount + 3,
    shortScore: shortScoreCount + 3
  }
}

onMounted(() => {
  runAnalysis()
})
</script>

<style scoped>
.trading-checklist {
  padding: 20px;
  max-width: 1600px;
  margin: 0 auto;
}

.checklist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 12px;
}

.checklist-header h2 {
  font-size: 18px;
  color: #e6edf3;
  margin: 0;
}

.symbol-selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.symbol-selector select {
  padding: 8px 16px;
  background: #21262d;
  border: 1px solid #30363d;
  color: #e6edf3;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
}

.current-price {
  font-size: 14px;
  color: #7d8590;
}

.current-price .positive { color: #3fb950; }
.current-price .negative { color: #f85149; }

.price-change {
  margin-left: 8px;
  font-size: 12px;
}

.analyze-btn {
  padding: 10px 20px;
  background: #f0b90b;
  border: none;
  border-radius: 6px;
  color: #000;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.analyze-btn:hover:not(:disabled) {
  background: #d4a50a;
}

.analyze-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.checklist-content {
  position: relative;
}

.loading-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px;
  color: #7d8590;
  font-size: 14px;
  gap: 16px;
}

.pulse-loader {
  width: 40px;
  height: 40px;
  border: 3px solid #21262d;
  border-top-color: #f0b90b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 核心逻辑架构 */
.logic-architecture {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.logic-item {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 8px;
}

.logic-icon {
  font-size: 24px;
}

.logic-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.logic-title {
  font-size: 13px;
  font-weight: 600;
  color: #e6edf3;
}

.logic-desc {
  font-size: 11px;
  color: #7d8590;
}

/* 检查清单网格 */
.checklist-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
}

.checklist-panel {
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.checklist-panel.long {
  border-top: 3px solid #3fb950;
}

.checklist-panel.decision {
  border-top: 3px solid #f0b90b;
}

.checklist-panel.short {
  border-top: 3px solid #f85149;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #0d1117;
  border-bottom: 1px solid #21262d;
}

.panel-header h3 {
  font-size: 14px;
  color: #e6edf3;
  margin: 0;
}

.score-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.score-badge.high {
  background: rgba(63, 185, 80, 0.2);
  color: #3fb950;
}

.score-badge.medium {
  background: rgba(240, 185, 11, 0.2);
  color: #f0b90b;
}

.score-badge.low {
  background: rgba(248, 81, 73, 0.2);
  color: #f85149;
}

@media (max-width: 1400px) {
  .checklist-grid {
    grid-template-columns: 1fr 1fr;
  }

  .checklist-panel.decision {
    grid-column: span 2;
  }
}

@media (max-width: 1000px) {
  .checklist-grid {
    grid-template-columns: 1fr;
  }

  .checklist-panel.decision {
    grid-column: span 1;
  }

  .logic-architecture {
    flex-direction: column;
  }
}
</style>