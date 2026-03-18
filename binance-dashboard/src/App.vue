<template>
  <div class="dashboard">
    <header class="header">
      <h1>📊 币安实时行情 Dashboard</h1>
      <div class="symbol-selector">
        <select v-model="selectedSymbol" @change="onSymbolChange">
          <option value="BTCUSDT">BTC/USDT</option>
          <option value="ETHUSDT">ETH/USDT</option>
          <option value="BNBUSDT">BNB/USDT</option>
          <option value="SOLUSDT">SOL/USDT</option>
          <option value="XRPUSDT">XRP/USDT</option>
          <option value="ADAUSDT">ADA/USDT</option>
          <option value="DOGEUSDT">DOGE/USDT</option>
        </select>
        <button class="refresh-btn" @click="fetchAllData" :disabled="loading">
          {{ loading ? '刷新中...' : '🔄 刷新' }}
        </button>
      </div>
    </header>

    <main class="main-content">
      <!-- 第一排：四个卡片并列 -->
      <section class="top-row">
        <!-- 1. 价格卡片 -->
        <div class="price-card main-price">
          <div class="card-header">
            <span class="coin-icon">{{ getCoinIcon(selectedSymbol) }}</span>
            <span class="coin-name">{{ selectedSymbol.replace('USDT', '') }}/USDT</span>
          </div>
          <div class="price-display">
            <span class="current-price">${{ formatPrice(tickerData.price) }}</span>
            <span :class="['price-change', ticker24h.priceChangePercent >= 0 ? 'positive' : 'negative']">
              {{ ticker24h.priceChangePercent >= 0 ? '+' : '' }}{{ ticker24h.priceChangePercent || 0 }}%
            </span>
          </div>
          <div class="price-stats">
            <div class="price-stat">
              <span class="stat-label">24h高</span>
              <span class="stat-value">${{ formatPrice(ticker24h.highPrice) }}</span>
            </div>
            <div class="price-stat">
              <span class="stat-label">24h低</span>
              <span class="stat-value">${{ formatPrice(ticker24h.lowPrice) }}</span>
            </div>
            <div class="price-stat">
              <span class="stat-label">24h量</span>
              <span class="stat-value">{{ formatNumber(ticker24h.volume) }}</span>
            </div>
          </div>
        </div>

        <!-- 2. 多周期状态 -->
        <div class="cycle-card">
          <div class="card-title">
            <span class="title-icon">📊</span>
            <span>多周期趋势</span>
          </div>
          <div class="cycle-grid">
            <div :class="['cycle-item', mtfData.trend5m ? 'bullish' : 'bearish']">
              <span class="cycle-label">5M</span>
              <span class="cycle-status">{{ mtfData.trend5m ? '多头' : '空头' }}</span>
            </div>
            <div :class="['cycle-item', mtfData.trend15m ? 'bullish' : 'bearish']">
              <span class="cycle-label">15M</span>
              <span class="cycle-status">{{ mtfData.trend15m ? '多头' : '空头' }}</span>
            </div>
            <div :class="['cycle-item', mtfData.trend30m ? 'bullish' : 'bearish']">
              <span class="cycle-label">30M</span>
              <span class="cycle-status">{{ mtfData.trend30m ? '多头' : '空头' }}</span>
            </div>
            <div :class="['cycle-item', mtfData.trend1h ? 'bullish' : 'bearish']">
              <span class="cycle-label">1H</span>
              <span class="cycle-status">{{ mtfData.trend1h ? '多头' : '空头' }}</span>
            </div>
            <div :class="['cycle-item', mtfData.trend4h ? 'bullish' : 'bearish']">
              <span class="cycle-label">4H</span>
              <span class="cycle-status">{{ mtfData.trend4h ? '多头' : '空头' }}</span>
            </div>
            <div :class="['cycle-item', mtfData.trend1d ? 'bullish' : 'bearish']">
              <span class="cycle-label">1D</span>
              <span class="cycle-status">{{ mtfData.trend1d ? '多头' : '空头' }}</span>
            </div>
          </div>
        </div>

        <!-- 3. 决策建议 -->
        <div :class="['decision-card', decision.adviceClass]">
          <div class="card-title">
            <span class="title-icon">{{ decision.adviceIcon }}</span>
            <span>智能决策</span>
          </div>
          <div class="decision-content">
            <div class="decision-status">
              <span class="status-main">{{ decision.adviceTitle }}</span>
              <span class="status-action">{{ decision.action }}</span>
            </div>
            <div class="decision-metrics">
              <div class="decision-metric">
                <span class="dm-label">趋势</span>
                <span :class="['dm-value', decision.state > 0 ? 'bullish' : (decision.state < 0 ? 'bearish' : 'neutral')]">
                  {{ decision.state > 0 ? '上涨' : (decision.state < 0 ? '下跌' : '震荡') }}
                </span>
              </div>
              <div class="decision-metric">
                <span class="dm-label">阶段</span>
                <span :class="['dm-value', decision.stageClass]">{{ decision.stageLabel }}</span>
              </div>
              <div class="decision-metric">
                <span class="dm-label">偏离</span>
                <span :class="['dm-value', decision.isOverextended ? 'warning' : '']">{{ decision.biasRatio }}%</span>
              </div>
              <div class="decision-metric">
                <span class="dm-label">根数/时间</span>
                <span class="dm-value">{{ decision.trendBars }}根 / {{ decision.timeStr }}</span>
              </div>
            </div>
            <div class="warning-flags">
              <span v-if="decision.isDivergence" class="flag danger">⚠️ 背驰</span>
              <span v-if="decision.isVolSpike" class="flag warning">⚠️ 天量</span>
              <span v-if="decision.isClimaxTop" class="flag danger">🚨 出货</span>
            </div>
          </div>
        </div>

        <!-- 4. 持仓信息 -->
        <div class="position-card">
          <div class="card-title">
            <span class="title-icon">📈</span>
            <span>持仓参考</span>
          </div>
          <div class="position-content">
            <div class="position-row">
              <span class="pos-label">多头止损</span>
              <span class="pos-value bullish">{{ decision.rigidStopLong || '---' }}</span>
            </div>
            <div class="position-row">
              <span class="pos-label">空头止损</span>
              <span class="pos-value bearish">{{ decision.rigidStopShort || '---' }}</span>
            </div>
            <div class="position-row">
              <span class="pos-label">目标位(高)</span>
              <span class="pos-value">{{ decision.swingHigh || '---' }}</span>
            </div>
            <div class="position-row">
              <span class="pos-label">目标位(低)</span>
              <span class="pos-value">{{ decision.swingLow || '---' }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- TradingView K线图表 -->
      <section class="chart-section">
        <div class="section-header">
          <h2>K线走势图</h2>
          <div class="chart-controls">
            <div class="interval-selector">
              <button
                v-for="int in intervals"
                :key="int.value"
                :class="['interval-btn', selectedInterval === int.value ? 'active' : '']"
                @click="changeInterval(int.value)"
              >
                {{ int.label }}
              </button>
            </div>
            <div class="indicator-selector">
              <div class="indicator-checkboxes">
                <label class="ind-check">
                  <input type="checkbox" value="ma" v-model="selectedIndicators" @change="updateIndicators" />
                  <span>MA</span>
                </label>
                <label class="ind-check">
                  <input type="checkbox" value="ema" v-model="selectedIndicators" @change="updateIndicators" />
                  <span>EMA</span>
                </label>
                <label class="ind-check">
                  <input type="checkbox" value="bollinger" v-model="selectedIndicators" @change="updateIndicators" />
                  <span>布林带</span>
                </label>
                <label class="ind-check">
                  <input type="checkbox" value="rsi" v-model="selectedIndicators" @change="updateIndicators" />
                  <span>RSI</span>
                </label>
                <label class="ind-check">
                  <input type="checkbox" value="macd" v-model="selectedIndicators" @change="updateIndicators" />
                  <span>MACD</span>
                </label>
                <label class="ind-check">
                  <input type="checkbox" value="volume" v-model="selectedIndicators" @change="updateIndicators" />
                  <span>成交量</span>
                </label>
              </div>
              <!-- MA/EMA 参数选择 -->
              <div v-if="selectedIndicators.includes('ma') || selectedIndicators.includes('ema')" class="indicator-params">
                <span class="params-label">{{ selectedIndicators.includes('ema') ? 'EMA' : 'MA' }}周期:</span>
                <label v-for="param in (selectedIndicators.includes('ema') ? emaParams : maParams)" :key="param" class="param-check">
                  <input type="checkbox" :value="param" v-model="selectedParams" @change="updateIndicators" />
                  <span>{{ param }}</span>
                </label>
              </div>
              <!-- 布林带参数 -->
              <div v-if="selectedIndicators.includes('bollinger')" class="indicator-params">
                <label>
                  <span>周期:</span>
                  <input type="number" v-model.number="bollingerPeriod" @change="updateIndicators" min="5" max="50" style="width:50px" />
                </label>
                <label>
                  <span>倍数:</span>
                  <input type="number" v-model.number="bollingerStdDev" @change="updateIndicators" min="1" max="3" step="0.5" style="width:50px" />
                </label>
              </div>
              <!-- RSI参数 -->
              <div v-if="selectedIndicators.includes('rsi')" class="indicator-params">
                <label>
                  <span>RSI周期:</span>
                  <input type="number" v-model.number="rsiPeriod" @change="updateIndicators" min="5" max="30" style="width:50px" />
                </label>
              </div>
              <!-- ATR止盈止损参数 (始终显示) -->
              <div class="indicator-params atr-params">
                <label>
                  <span>ATR倍数:</span>
                  <input type="number" v-model.number="atrMultiplier" @change="updateIndicators" min="0.5" max="10" step="0.5" style="width:50px" />
                </label>
                <span class="atr-hint">上线: 价格 + {{ atrMultiplier }}×ATR | 下线: 价格 - {{ atrMultiplier }}×ATR</span>
              </div>
            </div>
          </div>
        </div>
        <div class="chart-container main-chart">
          <div id="tradingview-chart"></div>
        </div>
      </section>

      <!-- 成交量图表 -->
      <section class="chart-section volume-section">
        <div class="section-header">
          <h2>成交量</h2>
          <div class="show-hide">
            <label>
              <input type="checkbox" v-model="showVolume" @change="updateVolumeChart" />
              显示
            </label>
          </div>
        </div>
        <div class="chart-container volume-chart">
          <div id="volume-chart"></div>
        </div>
      </section>

      <!-- MACD图表 -->
      <section class="chart-section macd-section">
        <div class="section-header">
          <h2>MACD (12, 26, 9)</h2>
          <div class="show-hide">
            <label>
              <input type="checkbox" v-model="showMACD" @change="updateMACDChart" />
              显示
            </label>
          </div>
        </div>
        <div class="chart-container macd-chart">
          <div id="macd-chart"></div>
        </div>
      </section>

      <!-- 订单簿和最新成交 -->
      <section class="data-section">
        <div class="orderbook-container">
          <h2>📖 订单簿</h2>
          <div class="orderbook">
            <div class="orderbook-header">
              <span>价格 (USDT)</span>
              <span>数量</span>
            </div>
            <div class="asks">
              <div v-for="(ask, i) in orderbook.asks.slice(0, 10).reverse()" :key="'ask-'+i" class="order-row ask">
                <span class="price">{{ parseFloat(ask[0]).toFixed(2) }}</span>
                <span class="qty">{{ parseFloat(ask[1]).toFixed(4) }}</span>
                <div class="depth-bar ask-bar" :style="{ width: (ask[1] / maxAskQty * 100) + '%' }"></div>
              </div>
            </div>
            <div class="spread">
              <span>价差: ${{ spread }}</span>
            </div>
            <div class="bids">
              <div v-for="(bid, i) in orderbook.bids.slice(0, 10)" :key="'bid-'+i" class="order-row bid">
                <span class="price">{{ parseFloat(bid[0]).toFixed(2) }}</span>
                <span class="qty">{{ parseFloat(bid[1]).toFixed(4) }}</span>
                <div class="depth-bar bid-bar" :style="{ width: (bid[1] / maxBidQty * 100) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="trades-container">
          <h2>⚡ 最新成交</h2>
          <div class="trades">
            <div class="trades-header">
              <span>价格</span>
              <span>数量</span>
              <span>时间</span>
            </div>
            <div v-for="trade in trades" :key="trade.id" :class="['trade-row', trade.isBuyerMaker ? 'sell' : 'buy']">
              <span class="price">{{ parseFloat(trade.price).toFixed(2) }}</span>
              <span class="qty">{{ parseFloat(trade.qty).toFixed(4) }}</span>
              <span class="time">{{ formatTime(trade.time) }}</span>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 自动刷新提示 -->
    <div class="auto-refresh">
      <label>
        <input type="checkbox" v-model="autoRefresh" @change="toggleAutoRefresh" />
        自动刷新 (每5秒)
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import axios from 'axios'
import { createChart, CrosshairMode } from 'lightweight-charts'

// 状态变量
const selectedSymbol = ref('BTCUSDT')
const loading = ref(false)
const autoRefresh = ref(true)
const selectedIndicators = ref([])
const selectedInterval = ref('1m')
const selectedParams = ref([12, 26])
const bollingerPeriod = ref(20)
const bollingerStdDev = ref(2)
const rsiPeriod = ref(14)
const atrMultiplier = ref(3.5)
const showVolume = ref(true)
const showMACD = ref(true)

// EMA/MA 参数选项
const emaParams = [7, 12, 25, 26, 50, 99, 144, 169, 200, 230]
const maParams = [7, 10, 20, 30, 60, 99, 120, 200]

// EMA/MA 颜色配置
const paramColors = {
  7: '#e74c3c',
  10: '#3498db',
  12: '#9b59b6',
  20: '#f0b90b',
  25: '#1abc9c',
  26: '#e67e22',
  30: '#95a5a6',
  50: '#2ecc71',
  60: '#34495e',
  99: '#16a085',
  120: '#8e44ad',
  144: '#f39c12',
  169: '#d35400',
  200: '#27ae60',
  230: '#c0392b'
}

// 决策配置
const config = ref({
  emaFast: 12,
  lookback: 50,
  volMult: 3.0,
  biasLimit: 1.5,
  atrPeriod: 14,
  atrMult: 2.2
})

// 多周期数据
const mtfData = ref({
  trend5m: false,
  trend15m: false,
  trend30m: false,
  trend1h: false,
  trend4h: false,
  trend1d: false
})

// 决策结果
const decision = ref({
  state: 0,           // 1: 多头, -1: 空头, 0: 震荡
  trendBars: 0,
  timeStr: '0分',
  stageLabel: '【震荡期】',
  stageClass: 'neutral',
  isDivergence: false,
  isVolSpike: false,
  isClimaxTop: false,
  isOverextended: false,
  biasRatio: '0.00',
  rigidStopLong: null,
  rigidStopShort: null,
  swingHigh: null,
  swingLow: null,
  adviceTitle: '博弈平衡区',
  adviceBody: '建议观望，等待明确信号',
  adviceIcon: '⚖️',
  adviceClass: 'neutral',
  action: '观望',
  actionClass: 'neutral'
})

let refreshTimer = null

// 主图表
let chart = null
let candlestickSeries = null

// 成交量图表
let volumeChart = null
let volumeSeries = null

// MACD图表
let macdChart = null
let macdLineSeries = null
let signalLineSeries = null
let histogramSeries = null

// 指标系列
const maSeriesMap = new Map()
const emaSeriesMap = new Map()
let bollingerUpperSeries = null
let bollingerMiddleSeries = null
let bollingerLowerSeries = null
let rsiSeries = null
let atrUpperSeries = null  // ATR上线 (价格 + n*ATR)
let atrLowerSeries = null  // ATR下线 (价格 - n*ATR)

const tickerData = ref({ price: 0 })
const ticker24h = ref({})
const orderbook = ref({ bids: [], asks: [] })
const klines = ref([])
const trades = ref([])

const intervals = [
  { label: '1分', value: '1m' },
  { label: '5分', value: '5m' },
  { label: '15分', value: '15m' },
  { label: '1时', value: '1h' },
  { label: '4时', value: '4h' },
  { label: '1天', value: '1d' }
]

// 计算属性
const maxAskQty = computed(() => Math.max(...orderbook.value.asks.slice(0, 10).map(a => parseFloat(a[1])), 0.001))
const maxBidQty = computed(() => Math.max(...orderbook.value.bids.slice(0, 10).map(b => parseFloat(b[1])), 0.001))

const spread = computed(() => {
  if (orderbook.value.asks.length && orderbook.value.bids.length) {
    const lowestAsk = parseFloat(orderbook.value.asks[0][0])
    const highestBid = parseFloat(orderbook.value.bids[0][0])
    return (lowestAsk - highestBid).toFixed(2)
  }
  return '0'
})

// 方法
const getCoinIcon = (symbol) => {
  const icons = {
    'BTCUSDT': '₿',
    'ETHUSDT': 'Ξ',
    'BNBUSDT': '◈',
    'SOLUSDT': '◎',
    'XRPUSDT': '✕',
    'ADAUSDT': '₳',
    'DOGEUSDT': 'Ð'
  }
  return icons[symbol] || '●'
}

const formatPrice = (price) => {
  if (!price) return '0.00'
  const p = parseFloat(price)
  return p < 1 ? p.toFixed(6) : p.toFixed(2)
}

const formatNumber = (num) => {
  if (!num) return '0'
  const n = parseFloat(num)
  return n >= 1e9 ? (n / 1e9).toFixed(2) + 'B' :
         n >= 1e6 ? (n / 1e6).toFixed(2) + 'M' :
         n >= 1e3 ? (n / 1e3).toFixed(2) + 'K' :
         n.toFixed(2)
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`
}

const fetchTicker = async () => {
  try {
    const res = await axios.get(`/api/ticker/${selectedSymbol.value}`)
    tickerData.value = res.data
  } catch (e) {
    console.error('获取价格失败', e)
  }
}

const fetch24hTicker = async () => {
  try {
    const res = await axios.get(`/api/ticker/24h/${selectedSymbol.value}`)
    ticker24h.value = res.data
  } catch (e) {
    console.error('获取24h数据失败', e)
  }
}

const fetchOrderbook = async () => {
  try {
    const res = await axios.get(`/api/orderbook/${selectedSymbol.value}`)
    orderbook.value = res.data
  } catch (e) {
    console.error('获取订单簿失败', e)
  }
}

const fetchKlines = async () => {
  try {
    const res = await axios.get(`/api/klines/${selectedSymbol.value}`, {
      params: { interval: selectedInterval.value, limit: 200 }
    })
    klines.value = res.data
    updateChart()
  } catch (e) {
    console.error('获取K线失败', e)
  }
}

const fetchTrades = async () => {
  try {
    const res = await axios.get(`/api/trades/${selectedSymbol.value}`, {
      params: { limit: 20 }
    })
    trades.value = res.data
  } catch (e) {
    console.error('获取成交失败', e)
  }
}

const fetchMtfData = async () => {
  try {
    const res = await axios.get(`/api/klines-mtf/${selectedSymbol.value}`, {
      params: { limit: 50 }
    })
    const data = res.data

    // 计算各周期趋势 (收盘价 > SMA20)
    const calcTrend = (klines) => {
      if (!klines || klines.length < 20) return false
      const closes = klines.map(k => parseFloat(k[4]))
      const sma20 = closes.slice(-20).reduce((a, b) => a + b, 0) / 20
      return closes[closes.length - 1] > sma20
    }

    mtfData.value = {
      trend5m: calcTrend(data['5m']),
      trend15m: calcTrend(data['15m']),
      trend30m: calcTrend(data['30m']),
      trend1h: calcTrend(data['1h']),
      trend4h: calcTrend(data['4h']),
      trend1d: calcTrend(data['1d'])
    }
  } catch (e) {
    console.error('获取多周期数据失败', e)
  }
}

const fetchAllData = async () => {
  loading.value = true
  await Promise.all([
    fetchTicker(),
    fetch24hTicker(),
    fetchOrderbook(),
    fetchKlines(),
    fetchTrades(),
    fetchMtfData()
  ])
  // 计算决策
  calculateDecision()
  loading.value = false
}

const onSymbolChange = () => {
  fetchAllData()
}

const changeInterval = (interval) => {
  selectedInterval.value = interval
  fetchKlines().then(() => calculateDecision())
}

// 核心决策计算 (Sentinel 策略核心逻辑)
const calculateDecision = () => {
  if (!klines.value.length || klines.value.length < 30) return

  const cfg = config.value
  const closes = klines.value.map(k => parseFloat(k[4]))
  const highs = klines.value.map(k => parseFloat(k[2]))
  const lows = klines.value.map(k => parseFloat(k[3]))
  const opens = klines.value.map(k => parseFloat(k[1]))
  const volumes = klines.value.map(k => parseFloat(k[5]))
  const timestamps = klines.value.map(k => k[0]) // K线时间戳

  const currentClose = closes[closes.length - 1]
  const currentOpen = opens[opens.length - 1]

  // 计算 EMA12 和 SMA20 (Purple Line)
  const ema12 = calculateEmaValue(closes, cfg.emaFast)
  const sma20 = calculateSmaValue(closes, 20)

  // 计算 ATR
  const trValues = []
  for (let i = 1; i < klines.value.length; i++) {
    const tr = Math.max(
      highs[i] - lows[i],
      Math.abs(highs[i] - closes[i - 1]),
      Math.abs(lows[i] - closes[i - 1])
    )
    trValues.push(tr)
  }
  const atrValue = calculateEmaValue(trValues, cfg.atrPeriod)

  // 计算 MACD
  const macdData = calculateMACDForChart(12, 26, 9)
  const currentHist = macdData.histogram[macdData.histogram.length - 1]

  // 判断金叉死叉 (使用最近的EMA和SMA比较)
  const recentCloses = closes.slice(-5)
  const prevEma12 = calculateEmaValue(closes.slice(0, -1), cfg.emaFast)
  const prevSma20 = calculateSmaValue(closes.slice(0, -1), 20)
  const crossUp = prevEma12 <= prevSma20 && ema12 > sma20
  const crossDown = prevEma12 >= prevSma20 && ema12 < sma20

  // 确定趋势状态
  let currentState = 0
  let trendBars = 1
  let trendStartIndex = klines.value.length - 1

  // 检查最近的金叉死叉位置
  for (let i = klines.value.length - 2; i >= 0; i--) {
    const prevC = closes.slice(0, i + 1)
    const emaC = calculateEmaValue(prevC, cfg.emaFast)
    const smaC = calculateSmaValue(prevC, 20)
    if (emaC > smaC) {
      currentState = 1
      trendStartIndex = i
      break
    } else if (emaC < smaC) {
      currentState = -1
      trendStartIndex = i
      break
    }
  }

  // 计算趋势持续根数
  trendBars = klines.value.length - trendStartIndex

  // 计算物理时间 (使用趋势开始的第一根K线时间)
  const startTime = timestamps[trendStartIndex]
  const endTime = timestamps[timestamps.length - 1]
  const elapsedMs = endTime - startTime
  const totalMins = Math.floor(elapsedMs / 60000)
  const days = Math.floor(totalMins / 1440)
  const hours = Math.floor((totalMins % 1440) / 60)
  const mins = totalMins % 60
  let timeStr = ''
  if (days > 0) timeStr += days + '天'
  if (hours > 0) timeStr += (timeStr ? ' ' : '') + hours + '时'
  timeStr += (timeStr ? ' ' : '') + mins + '分'

  // 趋势阶段评估
  let stageLabel = '【震荡期】'
  let stageClass = 'neutral'
  if (currentState !== 0) {
    if (trendBars <= 15) {
      stageLabel = '【趋势爆发期】'
      stageClass = 'bullish'
    } else if (trendBars <= 50) {
      stageLabel = '【趋势稳定期】'
      stageClass = 'stable'
    } else {
      stageLabel = '【潜在衰竭期】'
      stageClass = 'warning'
    }
  }

  // 偏离度计算
  const biasRatio = ((currentClose - sma20) / sma20) * 100
  const isOverextended = biasRatio > cfg.biasLimit

  // 计算成交量SMA
  const volSma20 = calculateSmaValue(volumes, 20)
  const isVolSpike = volumes[volumes.length - 1] > volSma20 * cfg.volMult

  // 计算背驰 (价格创新高但MACD未创新高)
  const priceMaxLookback = Math.max(...highs.slice(-cfg.lookback))
  const histMax5 = Math.max(...macdData.histogram.slice(-5))
  const isNewPriceHigh = highs[highs.length - 1] > priceMaxLookback
  const isDivergence = isNewPriceHigh && currentClose > priceMaxLookback * 0.99 && currentHist < histMax5 && currentHist > 0 && isOverextended

  // 天量顶判断
  const isClimaxTop = isDivergence && isVolSpike && currentState === 1

  // 刚性生命线计算
  const isBearSpike = currentClose < currentOpen && trValues[trValues.length - 1] > atrValue * 1.6
  const isBullSpike = currentClose > currentOpen && trValues[trValues.length - 1] > atrValue * 1.6
  let rigidStopLong = sma20 - atrValue * cfg.atrMult
  let rigidStopShort = sma20 + atrValue * cfg.atrMult

  // 目标位
  const swingHigh = Math.max(...highs.slice(-cfg.lookback))
  const swingLow = Math.min(...lows.slice(-cfg.lookback))

  // 生成决策建议
  let adviceTitle = '博弈平衡区'
  let adviceBody = '建议观望，等待明确信号'
  let adviceIcon = '⚖️'
  let adviceClass = 'neutral'
  let action = '观望'
  let actionClass = 'neutral'

  if (isClimaxTop && currentState === 1) {
    adviceTitle = '🚨 主力出货预警'
    adviceBody = '原因：天量背驰确认，主力派发。分析：当前为趋势末端，风险极高。'
    adviceIcon = '🚨'
    adviceClass = 'danger'
    action = '立即撤离!'
    actionClass = 'danger'
  } else if (isDivergence && currentState === 1) {
    adviceTitle = '⚠️ 动力学背驰'
    adviceBody = '原因：动能衰竭，趋势末端特征。分析：建议趋势末端止盈。'
    adviceIcon = '⚠️'
    adviceClass = 'warning'
    action = '分批止盈'
    actionClass = 'warning'
  } else if (mtfData.value.trend1d && mtfData.value.trend1h && mtfData.value.trend5m) {
    adviceTitle = '🌟 三周期共振'
    adviceBody = '原因：5M/1H/1D 周期同步上涨。分析：强劲上涨趋势，持续持仓。'
    adviceIcon = '🌟'
    adviceClass = 'bullish'
    action = '持续持有，回踩加仓'
    actionClass = 'bullish'
  } else if (mtfData.value.trend1d && mtfData.value.trend1h && !mtfData.value.trend5m) {
    adviceTitle = '📊 多头结构回调'
    adviceBody = '原因：杠杆清洗，小级别调整。分析：不破生命线可持续持有。'
    adviceIcon = '📊'
    adviceClass = 'stable'
    action = '持有，回调不破止损可加仓'
    actionClass = 'stable'
  } else if (!mtfData.value.trend1d && !mtfData.value.trend1h && !mtfData.value.trend5m) {
    adviceTitle = '🛡️ 全周期同步下行'
    adviceBody = '原因：所有周期均处于下跌趋势。分析：建议全线避险。'
    adviceIcon = '🛡️'
    adviceClass = 'danger'
    action = '全线避险，观望为主'
    actionClass = 'danger'
  } else {
    adviceTitle = '🔄 趋势修正/反弹'
    adviceBody = '原因：超卖或小级别波动。分析：快进快出为主。'
    adviceIcon = '🔄'
    adviceClass = 'neutral'
    action = '快进快出'
    actionClass = 'neutral'
  }

  // 更新决策结果
  decision.value = {
    state: currentState,
    trendBars,
    timeStr,
    stageLabel,
    stageClass,
    isDivergence,
    isVolSpike,
    isClimaxTop,
    isOverextended,
    biasRatio: biasRatio.toFixed(2),
    rigidStopLong: rigidStopLong.toFixed(4),
    rigidStopShort: rigidStopShort.toFixed(4),
    swingHigh: swingHigh.toFixed(2),
    swingLow: swingLow.toFixed(2),
    adviceTitle,
    adviceBody,
    adviceIcon,
    adviceClass,
    action,
    actionClass
  }
}

// 辅助计算函数
const calculateEmaValue = (data, period) => {
  if (data.length < period) return data[data.length - 1]
  const k = 2 / (period + 1)
  let ema = data.slice(0, period).reduce((a, b) => a + b, 0) / period
  for (let i = period; i < data.length; i++) {
    ema = data[i] * k + ema * (1 - k)
  }
  return ema
}

const calculateSmaValue = (data, period) => {
  if (data.length < period) return data[data.length - 1]
  return data.slice(-period).reduce((a, b) => a + b, 0) / period
}

const calculateMACD = (closes, fastPeriod, slowPeriod, signalPeriod) => {
  const fastEma = []
  const slowEma = []
  const kFast = 2 / (fastPeriod + 1)
  const kSlow = 2 / (slowPeriod + 1)

  let emaFast = closes[0]
  let emaSlow = closes[0]
  for (let i = 0; i < closes.length; i++) {
    emaFast = closes[i] * kFast + emaFast * (1 - kFast)
    emaSlow = closes[i] * kSlow + emaSlow * (1 - kSlow)
    fastEma.push(emaFast)
    slowEma.push(emaSlow)
  }

  const dif = fastEma.map((f, i) => f - slowEma[i])

  const kSignal = 2 / (signalPeriod + 1)
  let emaSignal = dif[0]
  const dea = [emaSignal]
  for (let i = 1; i < dif.length; i++) {
    emaSignal = dif[i] * kSignal + emaSignal * (1 - kSignal)
    dea.push(emaSignal)
  }

  const histogram = dif.map((d, i) => d - dea[i])

  return { dif, dea, histogram }
}

const updateDecision = () => {
  calculateDecision()
}

// 初始化图表
const initChart = () => {
  // ===== 主图表 (K线 + 指标) =====
  const container = document.getElementById('tradingview-chart')
  if (!container) return

  chart = createChart(container, {
    layout: {
      background: { color: '#161b22' },
      textColor: '#d1d5db'
    },
    grid: {
      vertLines: { color: '#21262d' },
      horzLines: { color: '#21262d' }
    },
    crosshair: {
      mode: CrosshairMode.Normal
    },
    rightPriceScale: {
      borderColor: '#30363d'
    },
    timeScale: {
      borderColor: '#30363d',
      timeVisible: true,
      secondsVisible: false
    },
    handleScroll: {
      mouseWheel: true,
      pressedMouseMove: true
    },
    handleScale: {
      axisPressedMouseMove: true,
      mouseWheel: true,
      pinch: true
    }
  })

  candlestickSeries = chart.addCandlestickSeries({
    upColor: '#26de81',
    downColor: '#fc5c7d',
    borderUpColor: '#26de81',
    borderDownColor: '#fc5c7d',
    wickUpColor: '#26de81',
    wickDownColor: '#fc5c7d'
  })

  // 预创建 MA/EMA 系列（最多10条）
  for (let i = 0; i < 10; i++) {
    maSeriesMap.set(i, chart.addLineSeries({
      color: '#f0b90b',
      lineWidth: 1,
      priceLineVisible: false,
      crosshairMarkerVisible: false,
      visible: false
    }))
    emaSeriesMap.set(i, chart.addLineSeries({
      color: '#9b59b6',
      lineWidth: 1,
      priceLineVisible: false,
      crosshairMarkerVisible: false,
      visible: false
    }))
  }

  // 布林带系列
  bollingerUpperSeries = chart.addLineSeries({
    color: 'rgba(231, 76, 60, 0.5)',
    lineWidth: 1,
    priceLineVisible: false,
    crosshairMarkerVisible: false,
    visible: false
  })
  bollingerMiddleSeries = chart.addLineSeries({
    color: 'rgba(52, 152, 219, 0.8)',
    lineWidth: 1,
    priceLineVisible: false,
    crosshairMarkerVisible: false,
    visible: false
  })
  bollingerLowerSeries = chart.addLineSeries({
    color: 'rgba(231, 76, 60, 0.5)',
    lineWidth: 1,
    priceLineVisible: false,
    crosshairMarkerVisible: false,
    visible: false
  })

  // RSI 系列 (使用单独price scale在顶部显示)
  rsiSeries = chart.addLineSeries({
    color: '#e91e63',
    lineWidth: 2,
    priceLineVisible: false,
    crosshairMarkerVisible: false,
    visible: false,
    priceScaleId: 'rsi'
  })

  // ATR 上线 (价格 + n*ATR) - 绿色虚线
  atrUpperSeries = chart.addLineSeries({
    color: '#26de81',
    lineWidth: 2,
    priceLineVisible: false,
    crosshairMarkerVisible: true,
    visible: false,
    lineStyle: 2
  })

  // ATR 下线 (价格 - n*ATR) - 红色虚线
  atrLowerSeries = chart.addLineSeries({
    color: '#fc5c7d',
    lineWidth: 2,
    priceLineVisible: false,
    crosshairMarkerVisible: true,
    visible: false,
    lineStyle: 2
  })

  // 设置RSI的price scale (右上角)
  chart.priceScale('rsi').applyOptions({
    scaleMargins: { top: 0.85, bottom: 0.1 }
  })

  // 调整主图表容器大小
  const resizeObserver = new ResizeObserver(entries => {
    if (entries.length === 0 || !chart) return
    const newRect = entries[0].contentRect
    chart.applyOptions({ width: newRect.width, height: newRect.height })
  })
  resizeObserver.observe(container)

  // ===== 成交量图表 =====
  initVolumeChart()

  // ===== MACD图表 =====
  initMACDChart()
}

// 初始化成交量图表
const initVolumeChart = () => {
  const container = document.getElementById('volume-chart')
  if (!container) return

  volumeChart = createChart(container, {
    layout: {
      background: { color: '#161b22' },
      textColor: '#d1d5db'
    },
    grid: {
      vertLines: { color: '#21262d' },
      horzLines: { color: '#21262d' }
    },
    rightPriceScale: {
      borderColor: '#30363d'
    },
    timeScale: {
      borderColor: '#30363d',
      timeVisible: true,
      secondsVisible: false
    },
    height: 120
  })

  volumeSeries = volumeChart.addHistogramSeries({
    color: '#26a69a',
    priceFormat: { type: 'volume' },
    priceScaleId: 'volume'
  })

  const resizeObserver = new ResizeObserver(entries => {
    if (entries.length === 0 || !volumeChart) return
    const newRect = entries[0].contentRect
    volumeChart.applyOptions({ width: newRect.width })
  })
  resizeObserver.observe(container)
}

// 初始化MACD图表
const initMACDChart = () => {
  const container = document.getElementById('macd-chart')
  if (!container) return

  macdChart = createChart(container, {
    layout: {
      background: { color: '#161b22' },
      textColor: '#d1d5db'
    },
    grid: {
      vertLines: { color: '#21262d' },
      horzLines: { color: '#21262d' }
    },
    rightPriceScale: {
      borderColor: '#30363d'
    },
    timeScale: {
      borderColor: '#30363d',
      timeVisible: true,
      secondsVisible: false
    },
    height: 150
  })

  // MACD柱状图
  histogramSeries = macdChart.addHistogramSeries({
    priceScaleId: 'histogram'
  })

  // MACD线
  macdLineSeries = macdChart.addLineSeries({
    color: '#2196F3',
    lineWidth: 2,
    priceLineVisible: false,
    crosshairMarkerVisible: false,
    priceScaleId: 'macd'
  })

  // Signal线
  signalLineSeries = macdChart.addLineSeries({
    color: '#FF9800',
    lineWidth: 2,
    priceLineVisible: false,
    crosshairMarkerVisible: false,
    priceScaleId: 'macd'
  })

  // 设置价格 scale
  macdChart.priceScale('histogram').applyOptions({
    scaleMargins: { top: 0.1, bottom: 0.1 }
  })
  macdChart.priceScale('macd').applyOptions({
    scaleMargins: { top: 0.1, bottom: 0.1 }
  })

  const resizeObserver = new ResizeObserver(entries => {
    if (entries.length === 0 || !macdChart) return
    const newRect = entries[0].contentRect
    macdChart.applyOptions({ width: newRect.width })
  })
  resizeObserver.observe(container)
}

// 转换K线数据格式
const formatCandleData = () => {
  return klines.value.map(k => ({
    time: k[0] / 1000,
    open: parseFloat(k[1]),
    high: parseFloat(k[2]),
    low: parseFloat(k[3]),
    close: parseFloat(k[4])
  }))
}

const formatVolumeData = () => {
  return klines.value.map(k => ({
    time: k[0] / 1000,
    value: parseFloat(k[5]),
    color: parseFloat(k[4]) >= parseFloat(k[1]) ? 'rgba(38, 222, 129, 0.5)' : 'rgba(252, 92, 125, 0.5)'
  }))
}

// 计算MA
const calculateMA = (period) => {
  const closes = klines.value.map(k => parseFloat(k[4]))
  const result = []
  for (let i = 0; i < closes.length; i++) {
    if (i < period - 1) {
      result.push({ time: klines.value[i][0] / 1000, value: null })
    } else {
      const sum = closes.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0)
      result.push({ time: klines.value[i][0] / 1000, value: sum / period })
    }
  }
  return result
}

// 计算EMA
const calculateEMA = (period) => {
  const closes = klines.value.map(k => parseFloat(k[4]))
  const k = 2 / (period + 1)
  const result = []
  let ema = closes[0]
  for (let i = 0; i < closes.length; i++) {
    if (i === 0) {
      ema = closes[0]
    } else {
      ema = closes[i] * k + ema * (1 - k)
    }
    result.push({ time: klines.value[i][0] / 1000, value: ema })
  }
  return result
}

// 计算布林带
const calculateBollinger = (period = 20, stdDev = 2) => {
  const closes = klines.value.map(k => parseFloat(k[4]))
  const result = { upper: [], middle: [], lower: [] }
  for (let i = 0; i < closes.length; i++) {
    if (i < period - 1) {
      result.middle.push({ time: klines.value[i][0] / 1000, value: null })
      result.upper.push({ time: klines.value[i][0] / 1000, value: null })
      result.lower.push({ time: klines.value[i][0] / 1000, value: null })
    } else {
      const slice = closes.slice(i - period + 1, i + 1)
      const ma = slice.reduce((a, b) => a + b, 0) / period
      const variance = slice.reduce((a, b) => a + Math.pow(b - ma, 2), 0) / period
      const std = Math.sqrt(variance)
      result.middle.push({ time: klines.value[i][0] / 1000, value: ma })
      result.upper.push({ time: klines.value[i][0] / 1000, value: ma + stdDev * std })
      result.lower.push({ time: klines.value[i][0] / 1000, value: ma - stdDev * std })
    }
  }
  return result
}

// 更新图表
const updateChart = () => {
  if (!candlestickSeries || !klines.value.length) return

  const candleData = formatCandleData()
  candlestickSeries.setData(candleData)

  updateIndicators()
  updateVolumeChart()
  updateMACDChart()
}

// 更新成交量图表
const updateVolumeChart = () => {
  if (!volumeSeries || !klines.value.length) return

  const volumeData = formatVolumeData()
  volumeSeries.setData(volumeData)
  volumeSeries.applyOptions({ visible: showVolume.value })

  if (volumeChart) {
    volumeChart.timeScale().fitContent()
  }
}

// 计算MACD (用于MACD图表显示)
const calculateMACDForChart = (fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) => {
  const closes = klines.value.map(k => parseFloat(k[4]))

  // 计算EMA
  const calculateEma = (period) => {
    const k = 2 / (period + 1)
    let ema = closes[0]
    const result = [ema]
    for (let i = 1; i < closes.length; i++) {
      ema = closes[i] * k + ema * (1 - k)
      result.push(ema)
    }
    return result
  }

  const fastEMA = calculateEma(fastPeriod)
  const slowEMA = calculateEma(slowPeriod)

  // DIF (MACD线)
  const dif = fastEMA.map((f, i) => f - slowEMA[i])

  // DEA (Signal线)
  const calculateSignalEma = (data, period) => {
    const k = 2 / (period + 1)
    let ema = data[0]
    const result = [ema]
    for (let i = 1; i < data.length; i++) {
      ema = data[i] * k + ema * (1 - k)
      result.push(ema)
    }
    return result
  }

  const dea = calculateSignalEma(dif, signalPeriod)

  // Histogram
  const histogram = dif.map((d, i) => d - dea[i])

  return {
    dif: dif.map((v, i) => ({ time: klines.value[i][0] / 1000, value: v })),
    dea: dea.map((v, i) => ({ time: klines.value[i][0] / 1000, value: v })),
    histogram: histogram.map((v, i) => ({
      time: klines.value[i][0] / 1000,
      value: v,
      color: v >= 0 ? 'rgba(38, 222, 129, 0.8)' : 'rgba(252, 92, 125, 0.8)'
    }))
  }
}

// 更新MACD图表
const updateMACDChart = () => {
  if (!macdLineSeries || !signalLineSeries || !histogramSeries || !klines.value.length) return

  const macdData = calculateMACDForChart(12, 26, 9)

  macdLineSeries.setData(macdData.dif)
  signalLineSeries.setData(macdData.dea)
  histogramSeries.setData(macdData.histogram)

  macdLineSeries.applyOptions({ visible: showMACD.value })
  signalLineSeries.applyOptions({ visible: showMACD.value })
  histogramSeries.applyOptions({ visible: showMACD.value })

  if (macdChart) {
    macdChart.timeScale().fitContent()
  }
}

const updateIndicators = () => {
  if (!candlestickSeries || !klines.value.length) return

  // 重置所有指标系列
  maSeriesMap.forEach(series => series.applyOptions({ visible: false }))
  emaSeriesMap.forEach(series => series.applyOptions({ visible: false }))
  if (bollingerUpperSeries) bollingerUpperSeries.applyOptions({ visible: false })
  if (bollingerMiddleSeries) bollingerMiddleSeries.applyOptions({ visible: false })
  if (bollingerLowerSeries) bollingerLowerSeries.applyOptions({ visible: false })
  if (rsiSeries) rsiSeries.applyOptions({ visible: false })

  // MA 均线
  if (selectedIndicators.value.includes('ma')) {
    selectedParams.value.forEach((param, index) => {
      if (maSeriesMap.has(index)) {
        const color = paramColors[param] || '#f0b90b'
        maSeriesMap.get(index).applyOptions({ visible: true, color, lineWidth: 1 })
        maSeriesMap.get(index).setData(calculateMA(param))
      }
    })
  }

  // EMA 均线
  if (selectedIndicators.value.includes('ema')) {
    selectedParams.value.forEach((param, index) => {
      if (emaSeriesMap.has(index)) {
        const color = paramColors[param] || '#9b59b6'
        emaSeriesMap.get(index).applyOptions({ visible: true, color, lineWidth: 1 })
        emaSeriesMap.get(index).setData(calculateEMA(param))
      }
    })
  }

  // 布林带
  if (selectedIndicators.value.includes('bollinger')) {
    const period = bollingerPeriod.value
    const stdDev = bollingerStdDev.value
    const bb = calculateBollinger(period, stdDev)
    bollingerUpperSeries.applyOptions({ visible: true, color: 'rgba(231, 76, 60, 0.6)' })
    bollingerMiddleSeries.applyOptions({ visible: true, color: 'rgba(52, 152, 219, 0.9)' })
    bollingerLowerSeries.applyOptions({ visible: true, color: 'rgba(231, 76, 60, 0.6)' })
    bollingerUpperSeries.setData(bb.upper)
    bollingerMiddleSeries.setData(bb.middle)
    bollingerLowerSeries.setData(bb.lower)
  }

  // RSI
  if (selectedIndicators.value.includes('rsi')) {
    const rsiData = calculateRSI(rsiPeriod.value)
    rsiSeries.applyOptions({ visible: true, color: '#e91e63' })
    rsiSeries.setData(rsiData)
  }

  // ATR 止盈止损线 (始终显示，根据倍数计算)
  const atrData = calculateATR(14)
  const closes = klines.value.map(k => parseFloat(k[4]))
  const multiplier = atrMultiplier.value

  const atrUpperData = []
  const atrLowerData = []

  for (let i = 0; i < klines.value.length; i++) {
    const atr = atrData[i]?.value
    const price = closes[i]

    if (atr && price) {
      atrUpperData.push({
        time: klines.value[i][0] / 1000,
        value: price + atr * multiplier
      })
      atrLowerData.push({
        time: klines.value[i][0] / 1000,
        value: price - atr * multiplier
      })
    }
  }

  if (atrUpperSeries && atrLowerSeries) {
    atrUpperSeries.setData(atrUpperData)
    atrLowerSeries.setData(atrLowerData)
    atrUpperSeries.applyOptions({ visible: true })
    atrLowerSeries.applyOptions({ visible: true })
  }

  // 成交量 (在主图表显示)
  if (selectedIndicators.value.includes('volume') && volumeSeries) {
    volumeSeries.applyOptions({ visible: true })
  } else if (volumeSeries) {
    volumeSeries.applyOptions({ visible: false })
  }

  // 自适应缩放
  chart.timeScale().fitContent()
}

// 计算RSI
const calculateRSI = (period = 14) => {
  const closes = klines.value.map(k => parseFloat(k[4]))
  const rsiData = []

  for (let i = 0; i < closes.length; i++) {
    if (i < period) {
      rsiData.push({ time: klines.value[i][0] / 1000, value: 50 })
      continue
    }

    let gain = 0, loss = 0
    for (let j = i - period + 1; j <= i; j++) {
      const change = closes[j] - closes[j - 1]
      if (change > 0) gain += change
      else loss += Math.abs(change)
    }

    const avgGain = gain / period
    const avgLoss = loss / period
    const rs = avgLoss === 0 ? 100 : avgGain / avgLoss
    const rsi = 100 - (100 / (1 + rs))

    rsiData.push({ time: klines.value[i][0] / 1000, value: rsi })
  }

  return rsiData
}

// 计算ATR
const calculateATR = (period = 14) => {
  const highs = klines.value.map(k => parseFloat(k[2]))
  const lows = klines.value.map(k => parseFloat(k[3]))
  const closes = klines.value.map(k => parseFloat(k[4]))
  const atrData = []

  if (highs.length < period + 1) {
    return klines.value.map(k => ({ time: k[0] / 1000, value: null }))
  }

  // 计算所有True Range
  const trValues = []
  for (let i = 0; i < highs.length; i++) {
    if (i === 0) {
      trValues.push(highs[i] - lows[i])
    } else {
      const tr = Math.max(
        highs[i] - lows[i],
        Math.abs(highs[i] - closes[i - 1]),
        Math.abs(lows[i] - closes[i - 1])
      )
      trValues.push(tr)
    }
  }

  // 计算ATR
  for (let i = 0; i < trValues.length; i++) {
    if (i < period) {
      // 初始期间使用简单的平均
      const sum = trValues.slice(0, i + 1).reduce((a, b) => a + b, 0)
      atrData.push({ time: klines.value[i][0] / 1000, value: sum / (i + 1) })
    } else if (i === period) {
      // 第一个正式ATR
      const sum = trValues.slice(1, period + 1).reduce((a, b) => a + b, 0)
      const atr = sum / period
      atrData.push({ time: klines.value[i][0] / 1000, value: atr })
    } else {
      // Wilder平滑
      const prevAtr = atrData[i - 1].value
      const atr = (prevAtr * (period - 1) + trValues[i]) / period
      atrData.push({ time: klines.value[i][0] / 1000, value: atr })
    }
  }

  return atrData
}

const toggleAutoRefresh = () => {
  if (autoRefresh.value) {
    refreshTimer = setInterval(fetchAllData, 5000)
  } else {
    clearInterval(refreshTimer)
  }
}

onMounted(async () => {
  await nextTick()
  initChart()
  fetchAllData()
  refreshTimer = setInterval(fetchAllData, 5000)
})

onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
  if (chart) chart.remove()
  if (volumeChart) volumeChart.remove()
  if (macdChart) macdChart.remove()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #0d1117;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
  border-radius: 12px;
  border: 1px solid #21262d;
}

.header h1 {
  font-size: 24px;
  color: #f0b90b;
}

.symbol-selector {
  display: flex;
  gap: 12px;
}

.symbol-selector select {
  padding: 10px 16px;
  font-size: 16px;
  background: #21262d;
  color: #e6edf3;
  border: 1px solid #30363d;
  border-radius: 8px;
  cursor: pointer;
}

.refresh-btn {
  padding: 10px 20px;
  background: #f0b90b;
  color: #000;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.refresh-btn:hover:not(:disabled) {
  background: #d4a000;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 第一排：四个卡片并列 */
.top-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 1400px) {
  .top-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .top-row {
    grid-template-columns: 1fr;
  }
}

/* 通用卡片样式 */
.price-card, .cycle-card, .decision-card, .position-card {
  background: linear-gradient(135deg, #1a1f2e 0%, #161b22 100%);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #21262d;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 16px;
  font-weight: 600;
  color: #e6edf3;
}

.title-icon {
  font-size: 18px;
}

/* 价格卡片 */
.price-card .current-price {
  font-size: 32px;
  font-weight: 700;
  color: #e6edf3;
}

.price-card .price-change {
  font-size: 18px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
}

.price-card .price-change.positive {
  color: #26de81;
  background: rgba(38, 222, 129, 0.15);
}

.price-card .price-change.negative {
  color: #fc5c7d;
  background: rgba(252, 92, 125, 0.15);
}

.price-stats {
  display: flex;
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #21262d;
}

.price-stat {
  flex: 1;
  text-align: center;
}

.price-stat .stat-label {
  display: block;
  font-size: 11px;
  color: #8b949e;
  margin-bottom: 4px;
}

.price-stat .stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #e6edf3;
}

/* 多周期卡片 */
.cycle-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.cycle-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 8px;
  border-radius: 10px;
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
  font-size: 12px;
  color: #8b949e;
  margin-bottom: 4px;
}

.cycle-status {
  font-size: 14px;
  font-weight: 700;
}

.cycle-item.bullish .cycle-status { color: #26de81; }
.cycle-item.bearish .cycle-status { color: #fc5c7d; }

/* 决策卡片 */
.decision-card {
  display: flex;
  flex-direction: column;
}

.decision-card.neutral { border-color: #8b949e; }
.decision-card.bullish { border-color: #26de81; }
.decision-card.warning { border-color: #f39c12; }
.decision-card.danger { border-color: #e74c3c; }
.decision-card.stable { border-color: #3498db; }

.decision-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.decision-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-main {
  font-size: 15px;
  font-weight: 600;
}

.decision-card.neutral .status-main { color: #8b949e; }
.decision-card.bullish .status-main { color: #26de81; }
.decision-card.warning .status-main { color: #f39c12; }
.decision-card.danger .status-main { color: #e74c3c; }
.decision-card.stable .status-main { color: #3498db; }

.status-action {
  font-size: 13px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(255,255,255,0.1);
}

.decision-card.neutral .status-action { color: #8b949e; }
.decision-card.bullish .status-action { color: #26de81; }
.decision-card.warning .status-action { color: #f39c12; }
.decision-card.danger .status-action { color: #e74c3c; }
.decision-card.stable .status-action { color: #3498db; }

.decision-metrics {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.decision-metric {
  text-align: center;
  padding: 8px;
  background: #0d1117;
  border-radius: 8px;
}

.dm-label {
  display: block;
  font-size: 10px;
  color: #8b949e;
  margin-bottom: 2px;
}

.dm-value {
  font-size: 13px;
  font-weight: 600;
}

.dm-value.bullish { color: #26de81; }
.dm-value.bearish { color: #fc5c7d; }
.dm-value.neutral { color: #8b949e; }
.dm-value.warning { color: #f39c12; }
.dm-value.stable { color: #3498db; }

.warning-flags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.flag {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}

.flag.danger {
  background: rgba(231, 76, 60, 0.2);
  color: #e74c3c;
}

.flag.warning {
  background: rgba(243, 156, 18, 0.2);
  color: #f39c12;
}

/* 持仓卡片 */
.position-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.position-content .position-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 12px;
  background: #0d1117;
  border-radius: 8px;
}

.position-content .pos-label {
  color: #8b949e;
  font-size: 13px;
}

.position-content .pos-value {
  font-family: monospace;
  font-size: 14px;
  font-weight: 600;
}

.position-content .pos-value.bullish { color: #26de81; }
.position-content .pos-value.bearish { color: #fc5c7d; }

.decision-badge.neutral {
  background: rgba(139, 148, 158, 0.15);
  border: 1px solid #8b949e;
}

.decision-badge.bullish {
  background: rgba(38, 222, 129, 0.15);
  border: 1px solid #26de81;
}

.decision-badge.warning {
  background: rgba(243, 156, 18, 0.15);
  border: 1px solid #f39c12;
}

.decision-badge.danger {
  background: rgba(231, 76, 60, 0.15);
  border: 1px solid #e74c3c;
}

.decision-badge.stable {
  background: rgba(52, 152, 219, 0.15);
  border: 1px solid #3498db;
}

.badge-icon {
  font-size: 20px;
}

.badge-title {
  font-size: 14px;
  font-weight: 600;
  flex: 1;
}

.decision-badge.neutral .badge-title { color: #8b949e; }
.decision-badge.bullish .badge-title { color: #26de81; }
.decision-badge.warning .badge-title { color: #f39c12; }
.decision-badge.danger .badge-title { color: #e74c3c; }
.decision-badge.stable .badge-title { color: #3498db; }

.badge-action {
  font-size: 14px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(255,255,255,0.1);
}

.decision-badge.neutral .badge-action { color: #8b949e; }
.decision-badge.bullish .badge-action { color: #26de81; }
.decision-badge.warning .badge-action { color: #f39c12; }
.decision-badge.danger .badge-action { color: #e74c3c; }
.decision-badge.stable .badge-action { color: #3498db; }

.mini-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

.mini-metric {
  text-align: center;
  padding: 8px 4px;
  background: #0d1117;
  border-radius: 8px;
}

.mini-metric.warning {
  border: 1px solid #f39c12;
}

.mini-metric.warning .mini-value {
  color: #f39c12;
}

.mini-label {
  display: block;
  font-size: 10px;
  color: #8b949e;
  margin-bottom: 2px;
}

.mini-value {
  font-size: 13px;
  font-weight: 600;
  color: #e6edf3;
}

.mini-value.bullish { color: #26de81; }
.mini-value.bearish { color: #fc5c7d; }
.mini-value.neutral { color: #8b949e; }
.mini-value.warning { color: #f39c12; }
.mini-value.danger { color: #e74c3c; }
.mini-value.stable { color: #3498db; }

.chart-section {
  display: block;
  color: #8b949e;
  font-size: 14px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
}

.stat-value.positive { color: #26de81; }
.stat-value.negative { color: #fc5c7d; }

.chart-section {
  background: #161b22;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  border: 1px solid #21262d;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.section-header h2 {
  font-size: 18px;
  color: #e6edf3;
}

.chart-controls {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.interval-selector {
  display: flex;
  gap: 8px;
}

.interval-btn {
  padding: 6px 12px;
  background: #21262d;
  color: #8b949e;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.interval-btn.active {
  background: #f0b90b;
  color: #000;
}

.indicator-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.indicator-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ind-check {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  background: #21262d;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  color: #8b949e;
  transition: all 0.2s;
}

.ind-check:hover {
  background: #30363d;
}

.ind-check input {
  accent-color: #f0b90b;
}

.ind-check:has(input:checked) {
  background: rgba(240, 185, 11, 0.2);
  color: #f0b90b;
}

.indicator-params {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  padding: 8px;
  background: #0d1117;
  border-radius: 8px;
}

.params-label {
  font-size: 12px;
  color: #8b949e;
}

.param-check {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 3px 6px;
  background: #21262d;
  border-radius: 4px;
  font-size: 11px;
  color: #8b949e;
  cursor: pointer;
}

.param-check input {
  width: 12px;
  height: 12px;
  accent-color: #f0b90b;
}

.param-check:has(input:checked) {
  background: rgba(240, 185, 11, 0.3);
  color: #f0b90b;
}

.atr-params {
  background: rgba(38, 222, 129, 0.1) !important;
  border: 1px solid rgba(38, 222, 129, 0.3);
}

.atr-hint {
  font-size: 11px;
  color: #8b949e;
  margin-left: 8px;
}

.indicator-params input[type="number"],
.indicator-params input[type="text"] {
  background: #21262d;
  border: 1px solid #30363d;
  color: #e6edf3;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.indicator-params input[type="checkbox"] {
  width: 14px;
  height: 14px;
  accent-color: #f0b90b;
}

.indicator-params input[type="number"] {
  background: #0d1117;
  border: 1px solid #30363d;
  color: #e6edf3;
  padding: 2px 4px;
  border-radius: 4px;
}

.chart-container {
  height: 400px;
  width: 100%;
}

.main-chart {
  height: 500px;
}

.volume-section {
  margin-top: 16px;
}

.volume-chart {
  height: 120px;
}

.macd-section {
  margin-top: 16px;
}

.macd-chart {
  height: 150px;
}

/* 决策面板样式 */
.decision-section {
  background: #161b22;
  border-radius: 16px;
  padding: 24px;
  margin-top: 24px;
  border: 1px solid #21262d;
}

.decision-config {
  display: flex;
  gap: 16px;
}

.decision-config label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #8b949e;
  font-size: 13px;
}

.decision-config input {
  background: #0d1117;
  border: 1px solid #30363d;
  color: #e6edf3;
  padding: 4px 8px;
  border-radius: 4px;
}

/* 多周期看板 */
.multi-timeframe-dash {
  display: flex;
  gap: 12px;
  margin: 16px 0;
  flex-wrap: wrap;
}

.tf-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 16px;
  background: #0d1117;
  border-radius: 8px;
  border: 2px solid #30363d;
  min-width: 60px;
}

.tf-item.active {
  border-color: #26de81;
  background: rgba(38, 222, 129, 0.1);
}

.tf-item.danger {
  border-color: #fc5c7d;
  background: rgba(252, 92, 125, 0.1);
}

.tf-label {
  font-size: 12px;
  color: #8b949e;
}

.tf-status {
  font-size: 16px;
  font-weight: 700;
}

.tf-item.active .tf-status {
  color: #26de81;
}

.tf-item.danger .tf-status {
  color: #fc5c7d;
}

/* 核心指标 */
.core-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin: 16px 0;
}

.metric-card {
  background: #0d1117;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #21262d;
}

.metric-card.warning {
  border-color: #f39c12;
}

.metric-card.danger {
  border-color: #e74c3c;
}

.metric-label {
  display: block;
  font-size: 12px;
  color: #8b949e;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 16px;
  font-weight: 600;
  color: #e6edf3;
}

.metric-value.bullish { color: #26de81; }
.metric-value.bearish { color: #fc5c7d; }
.metric-value.neutral { color: #8b949e; }
.metric-value.warning { color: #f39c12; }
.metric-value.danger { color: #e74c3c; }

/* 决策建议 */
.advice-panel {
  padding: 20px;
  border-radius: 12px;
  margin: 16px 0;
  border: 2px solid;
}

.advice-panel.neutral {
  background: rgba(139, 148, 158, 0.1);
  border-color: #8b949e;
}

.advice-panel.bullish {
  background: rgba(38, 222, 129, 0.1);
  border-color: #26de81;
}

.advice-panel.warning {
  background: rgba(243, 156, 18, 0.1);
  border-color: #f39c12;
}

.advice-panel.danger {
  background: rgba(231, 76, 60, 0.1);
  border-color: #e74c3c;
}

.advice-panel.stable {
  background: rgba(52, 152, 219, 0.1);
  border-color: #3498db;
}

.advice-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.advice-icon {
  font-size: 24px;
}

.advice-title {
  font-size: 18px;
  font-weight: 700;
}

.advice-panel.neutral .advice-title { color: #8b949e; }
.advice-panel.bullish .advice-title { color: #26de81; }
.advice-panel.warning .advice-title { color: #f39c12; }
.advice-panel.danger .advice-title { color: #e74c3c; }
.advice-panel.stable .advice-title { color: #3498db; }

.advice-body p {
  color: #d1d5db;
  line-height: 1.6;
  margin: 0;
}

.advice-action {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid rgba(255,255,255,0.1);
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-label {
  color: #8b949e;
}

.action-value {
  font-size: 18px;
  font-weight: 700;
}

.advice-panel.neutral .action-value { color: #8b949e; }
.advice-panel.bullish .action-value { color: #26de81; }
.advice-panel.warning .action-value { color: #f39c12; }
.advice-panel.danger .action-value { color: #e74c3c; }
.advice-panel.stable .action-value { color: #3498db; }

/* 持仓信息 */
.position-info {
  background: #0d1117;
  border-radius: 8px;
  padding: 16px;
  margin-top: 16px;
}

.position-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #21262d;
}

.position-row:last-child {
  border-bottom: none;
}

.pos-label {
  color: #8b949e;
}

.pos-value {
  font-family: monospace;
  font-weight: 600;
}

.pos-value.bullish { color: #26de81; }
.pos-value.bearish { color: #fc5c7d; }

.show-hide {
  display: flex;
  align-items: center;
}

.show-hide label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #8b949e;
  cursor: pointer;
}

.show-hide input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #f0b90b;
}

#tradingview-chart {
  width: 100%;
  height: 100%;
}

#volume-chart {
  width: 100%;
  height: 100%;
}

#macd-chart {
  width: 100%;
  height: 100%;
}

.data-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

@media (max-width: 768px) {
  .data-section {
    grid-template-columns: 1fr;
  }
}

.orderbook-container, .trades-container {
  background: #161b22;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #21262d;
}

.orderbook-container h2, .trades-container h2 {
  font-size: 18px;
  margin-bottom: 16px;
  color: #e6edf3;
}

.orderbook-header, .trades-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 8px 12px;
  color: #8b949e;
  font-size: 14px;
  border-bottom: 1px solid #21262d;
}

.trades-header {
  grid-template-columns: 1fr 1fr 1fr;
}

.order-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 6px 12px;
  position: relative;
  font-size: 14px;
}

.order-row .price { font-family: monospace; }
.order-row .qty { text-align: right; font-family: monospace; color: #8b949e; }

.depth-bar {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  opacity: 0.2;
}

.ask-bar { background: #fc5c7d; }
.bid-bar { background: #26de81; }

.spread {
  padding: 8px 12px;
  text-align: center;
  color: #f0b90b;
  font-size: 14px;
  background: #21262d;
  margin: 4px 0;
}

.trade-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  padding: 8px 12px;
  font-size: 14px;
  border-bottom: 1px solid #21262d;
}

.trade-row.buy .price { color: #26de81; }
.trade-row.sell .price { color: #fc5c7d; }

.auto-refresh {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #161b22;
  padding: 12px 20px;
  border-radius: 8px;
  border: 1px solid #21262d;
}

.auto-refresh label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #8b949e;
  cursor: pointer;
}

.auto-refresh input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #f0b90b;
}
</style>