<template>
  <div class="trading-detail">
    <!-- 交易对选择器 -->
    <div class="symbol-selector">
      <div class="search-wrapper" ref="searchWrapper">
        <input
          type="text"
          class="search-input"
          v-model="searchQuery"
          @focus="showDropdown = true"
          @input="onSearchInput"
          :placeholder="selectedSymbol ? formatSymbol(selectedSymbol) : '选择交易对...'"
        />
        <div v-if="showDropdown" class="dropdown">
          <div class="dropdown-section" v-if="searchQuery === ''">
            <div class="dropdown-label">常用交易对</div>
            <div
              v-for="symbol in defaultSymbols"
              :key="symbol"
              class="dropdown-item"
              :class="{ active: selectedSymbol === symbol }"
              @click="handleSelectSymbol(symbol)"
            >
              {{ formatSymbol(symbol) }}
            </div>
          </div>
          <div class="dropdown-section" v-if="filteredSymbols.length > 0">
            <div class="dropdown-label" v-if="searchQuery !== ''">搜索结果 ({{ filteredSymbols.length }})</div>
            <div
              v-for="symbol in filteredSymbols"
              :key="symbol.symbol"
              class="dropdown-item"
              :class="{ active: selectedSymbol === symbol.symbol }"
              @click="handleSelectSymbol(symbol.symbol)"
            >
              {{ formatSymbol(symbol.symbol) }}
            </div>
          </div>
        </div>
      </div>
      <button class="refresh-btn" @click="fetchAllData" :disabled="loading">
        {{ loading ? '刷新中...' : '🔄 刷新' }}
      </button>
    </div>

    <div class="detail-content">
      <!-- 第一排：四个卡片 -->
      <section class="top-row">
        <PriceCard
          :symbol="selectedSymbol"
          :price="tickerData.price"
          :price-change-percent="ticker24h.priceChangePercent"
          :high-price="ticker24h.highPrice"
          :low-price="ticker24h.lowPrice"
          :volume="ticker24h.volume"
        />
        <CycleCard
          :trend5m="mtfData.trend5m"
          :trend15m="mtfData.trend15m"
          :trend30m="mtfData.trend30m"
          :trend1h="mtfData.trend1h"
          :trend4h="mtfData.trend4h"
          :trend1d="mtfData.trend1d"
        />
        <DecisionCard
          :state="decision.state"
          :trend-bars="decision.trendBars"
          :time-str="decision.timeStr"
          :stage-label="decision.stageLabel"
          :stage-class="decision.stageClass"
          :is-divergence="decision.isDivergence"
          :is-vol-spike="decision.isVolSpike"
          :is-climax-top="decision.isClimaxTop"
          :is-overextended="decision.isOverextended"
          :bias-ratio="decision.biasRatio"
          :advice-title="decision.adviceTitle"
          :advice-icon="decision.adviceIcon"
          :advice-class="decision.adviceClass"
          :action="decision.action"
          :action-class="decision.actionClass"
        />
        <PositionCard
          :rigid-stop-long="decision.rigidStopLong"
          :rigid-stop-short="decision.rigidStopShort"
          :swing-high="decision.swingHigh"
          :swing-low="decision.swingLow"
        />
      </section>

      <!-- 图表和订单簿 -->
      <section class="chart-orderbook-wrapper">
        <div class="charts-area">
          <div class="chart-section main-chart-section">
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
              </div>
            </div>
            <div class="chart-container main-chart">
              <div id="tradingview-chart" :style="{ height: chartHeights.candle + 'px' }"></div>
            </div>
          </div>

          <div class="chart-section rsi-section">
            <div class="section-header">
              <h2>RSI (14)</h2>
              <div class="show-hide">
                <label>
                  <input type="checkbox" v-model="showRSI" @change="updateRSIChart" />
                  显示
                </label>
              </div>
            </div>
            <div class="chart-container rsi-chart" v-show="showRSI" :style="{ height: chartHeights.rsi + 'px' }">
              <div id="rsi-chart"></div>
            </div>
          </div>

          <div class="chart-section macd-section">
            <div class="section-header">
              <h2>MACD (12, 26, 9)</h2>
              <div class="show-hide">
                <label>
                  <input type="checkbox" v-model="showMACD" @change="updateMACDChart" />
                  显示
                </label>
              </div>
            </div>
            <div class="chart-container macd-chart" v-show="showMACD" :style="{ height: chartHeights.macd + 'px' }">
              <div id="macd-chart"></div>
            </div>
          </div>
        </div>

        <!-- 订单簿 -->
        <div class="orderbook-sidebar">
          <h2>📖 订单簿</h2>
          <div class="orderbook" id="orderbook-container" :style="{ height: chartHeights.orderbook + 'px' }">
            <div class="orderbook-header">
              <span>价格</span>
              <span>数量</span>
            </div>
            <div class="asks">
              <div v-for="(ask, i) in orderbook.asks.slice(0, 10).reverse()" :key="'ask-'+i" class="order-row ask">
                <span class="price">{{ parseFloat(ask[0]).toFixed(2) }}</span>
                <span class="qty">{{ parseFloat(ask[1]).toFixed(4) }}</span>
              </div>
            </div>
            <div class="spread">
              <span>价差: ${{ spread }}</span>
            </div>
            <div class="bids">
              <div v-for="(bid, i) in orderbook.bids.slice(0, 10)" :key="'bid-'+i" class="order-row bid">
                <span class="price">{{ parseFloat(bid[0]).toFixed(2) }}</span>
                <span class="qty">{{ parseFloat(bid[1]).toFixed(4) }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 智能分析 -->
      <section class="analysis-section">
        <div class="analysis-header">
          <h2>🧠 智能趋势分析</h2>
        </div>
        <div class="timeline-container">
          <div class="timeline-track">
            <div
              v-for="(node, index) in trendNodes"
              :key="index"
              :class="['timeline-node', node.direction, { current: node.isCurrent }]"
            >
              <div class="node-dot">
                <span class="node-icon">{{ node.direction === 'bullish' ? '↗' : '↘' }}</span>
              </div>
              <div class="node-card">
                <div class="node-header">
                  <span class="node-type">{{ node.direction === 'bullish' ? '多头趋势' : '空头趋势' }}</span>
                  <span class="node-time">{{ node.timeStr }}</span>
                </div>
                <div class="node-metrics">
                  <div class="metric">
                    <span class="metric-label">持续时间</span>
                    <span class="metric-value">{{ node.duration }}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">涨跌幅度</span>
                    <span class="metric-value">{{ node.changePercent }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 自动刷新 -->
    <div class="auto-refresh">
      <label>
        <input type="checkbox" v-model="autoRefresh" @change="toggleAutoRefresh" />
        自动刷新 (每5秒)
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createChart, CrosshairMode } from 'lightweight-charts'

import PriceCard from '@/components/cards/PriceCard.vue'
import CycleCard from '@/components/cards/CycleCard.vue'
import DecisionCard from '@/components/cards/DecisionCard.vue'
import PositionCard from '@/components/cards/PositionCard.vue'

import { useTrading } from '@/composables/useTrading'
import { useChartConfig } from '@/composables/useChart'
import { useMarketData } from '@/composables/useMarketData'
import { useIndicators } from '@/composables/useIndicators'
import { useDecision } from '@/composables/useDecision'

const route = useRoute()
const router = useRouter()

const {
  selectedSymbol,
  searchQuery,
  showDropdown,
  searchWrapper,
  defaultSymbols,
  filteredSymbols,
  selectSymbol,
  formatSymbol,
  onSearchInput,
  closeDropdown
} = useTrading()

const { chartHeights, showMACD, showRSI } = useChartConfig()
const {
  tickerData, ticker24h, orderbook, klines, spread,
  fetchTicker, fetchOrderbook, fetchKlines, fetchAllSymbols, updateOrderbookMetrics
} = useMarketData()
const { selectedInterval, intervals, calculateRSI } = useIndicators()
const { mtfData, decision, trendNodes, calculateDecision, generateTrendNodes } = useDecision()

const loading = ref(false)
const autoRefresh = ref(true)
let refreshInterval = null

let rsiChart = null, macdChart = null
let rsiLineSeries = null, rsiUpperBand = null, rsiLowerBand = null
let histogramSeries = null, macdLineSeries = null, signalLineSeries = null

const handleSelectSymbol = (symbol) => {
  selectSymbol(symbol)
  router.push({ name: 'TradingPairDetail', params: { symbol } })
}

const changeInterval = (interval) => {
  selectedInterval.value = interval
  fetchKlines(selectedSymbol.value, interval, 200)
  const container = document.getElementById('tradingview-chart')
  if (container) {
    container.innerHTML = ''
    initTradingView()
  }
}

const initTradingView = () => {
  const tvIntervalMap = { '1m': '1', '5m': '5', '15m': '15', '1h': '60', '4h': '240', '1d': 'D' }
  const tvInterval = tvIntervalMap[selectedInterval.value] || '1'

  const createWidget = () => {
    if (window.TradingView) {
      new window.TradingView.widget({
        autosize: true,
        symbol: `BINANCE:${selectedSymbol.value}`,
        interval: tvInterval,
        timezone: 'Asia/Shanghai',
        theme: 'dark',
        style: '1',
        locale: 'zh_CN',
        toolbar_bg: '#161b22',
        enable_publishing: false,
        allow_symbol_change: true,
        hide_side_toolbar: false,
        container_id: 'tradingview-chart'
      })
    }
  }

  if (window.TradingView) {
    createWidget()
  } else {
    const script = document.createElement('script')
    script.src = 'https://s3.tradingview.com/tv.js'
    script.onload = createWidget
    document.head.appendChild(script)
  }
}

const initRSIChart = () => {
  const container = document.getElementById('rsi-chart')
  if (!container) return
  rsiChart = createChart(container, {
    layout: { background: { type: 'solid', color: '#161b22' }, textColor: '#8b949e' },
    grid: { vertLines: { color: '#21262d' }, horzLines: { color: '#21262d' } },
    height: chartHeights.rsi,
    crosshair: { mode: CrosshairMode.Normal }
  })
  rsiUpperBand = rsiChart.addLineSeries({ color: '#fc5c7d', lineWidth: 1 })
  rsiLowerBand = rsiChart.addLineSeries({ color: '#26de81', lineWidth: 1 })
  rsiLineSeries = rsiChart.addLineSeries({ color: '#9b59b6', lineWidth: 2 })
}

const initMACDChart = () => {
  const container = document.getElementById('macd-chart')
  if (!container) return
  macdChart = createChart(container, {
    layout: { background: { color: '#161b22' }, textColor: '#d1d5db' },
    grid: { vertLines: { color: '#21262d' }, horzLines: { color: '#21262d' } },
    height: chartHeights.macd
  })
  histogramSeries = macdChart.addHistogramSeries({ priceScaleId: 'histogram' })
  macdLineSeries = macdChart.addLineSeries({ color: '#2196F3', lineWidth: 2, priceScaleId: 'macd' })
  signalLineSeries = macdChart.addLineSeries({ color: '#FF9800', lineWidth: 2, priceScaleId: 'macd' })
}

const updateRSIChart = () => {
  if (!rsiLineSeries || !klines.value.length) return
  const rsiData = calculateRSI(klines.value, 14).filter(d => d.value !== null && !isNaN(d.value))
  rsiLineSeries.setData(rsiData)
  if (rsiUpperBand && rsiData.length > 0) {
    rsiUpperBand.setData(rsiData.map(d => ({ time: d.time, value: 70 })))
    rsiLowerBand.setData(rsiData.map(d => ({ time: d.time, value: 30 })))
  }
  if (rsiChart) rsiChart.timeScale().fitContent()
}

const updateMACDChart = () => {
  if (!macdLineSeries || !klines.value.length) return
  const closes = klines.value.map(k => parseFloat(k[4]))
  const calcEma = (period) => {
    const k = 2 / (period + 1)
    let ema = closes.slice(0, period).reduce((a, b) => a + b, 0) / period
    return closes.map(c => { ema = c * k + ema * (1 - k); return ema })
  }
  const fast = calcEma(12), slow = calcEma(26)
  const macdLine = closes.map((_, i) => fast[i] - slow[i])

  macdLineSeries.setData(macdLine.map((v, i) => ({ time: klines.value[i][0] / 1000, value: v })).filter(d => !isNaN(d.value)))
  if (macdChart) macdChart.timeScale().fitContent()
}

const fetchAllData = async () => {
  if (loading.value) return
  loading.value = true
  try {
    await Promise.all([
      fetchTicker(selectedSymbol.value),
      fetchOrderbook(selectedSymbol.value, 20),
      fetchKlines(selectedSymbol.value, selectedInterval.value, 200)
    ])
    updateOrderbookMetrics()
    if (rsiLineSeries) updateRSIChart()
    if (macdLineSeries) updateMACDChart()
    calculateDecision(klines.value, tickerData.value, ticker24h.value, 3.5)
    generateTrendNodes(klines.value)
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

const toggleAutoRefresh = () => {
  if (autoRefresh.value) {
    refreshInterval = setInterval(fetchAllData, 5000)
  } else if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

onMounted(async () => {
  if (route.params.symbol) {
    selectSymbol(route.params.symbol)
  }
  await fetchAllSymbols()
  initRSIChart()
  initMACDChart()
  initTradingView()
  await fetchAllData()
  toggleAutoRefresh()
  document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
  document.removeEventListener('click', closeDropdown)
})

watch(selectedSymbol, () => {
  fetchAllData()
  router.push({ name: 'TradingPairDetail', params: { symbol: selectedSymbol.value } })
})
</script>

<style scoped>
.trading-detail {
  padding: 16px;
}

.symbol-selector {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-wrapper {
  position: relative;
}

.search-input {
  padding: 8px 12px;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 6px;
  color: #e6edf3;
  font-size: 13px;
  width: 200px;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 6px;
  margin-top: 4px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 100;
  min-width: 200px;
}

.dropdown-section { padding: 8px; }
.dropdown-label { font-size: 10px; color: #8b949e; margin-bottom: 4px; }
.dropdown-item { padding: 6px 8px; border-radius: 4px; cursor: pointer; font-size: 13px; }
.dropdown-item:hover { background: #21262d; }
.dropdown-item.active { background: rgba(240, 185, 11, 0.2); color: #f0b90b; }

.refresh-btn {
  padding: 8px 16px;
  background: #f0b90b;
  border: none;
  border-radius: 6px;
  color: #000;
  font-weight: 600;
  cursor: pointer;
}

.refresh-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.top-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

@media (max-width: 1200px) { .top-row { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .top-row { grid-template-columns: 1fr; } }

.chart-orderbook-wrapper {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.charts-area { flex: 1; min-width: 0; }
.orderbook-sidebar { width: 260px; flex-shrink: 0; }

.chart-section { margin-bottom: 12px; }
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.section-header h2 { font-size: 14px; color: #e6edf3; margin: 0; }

.chart-controls { display: flex; gap: 8px; }
.interval-selector { display: flex; gap: 4px; }
.interval-btn {
  padding: 4px 8px;
  background: #21262d;
  color: #8b949e;
  border: none;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
}
.interval-btn:hover { background: #30363d; }
.interval-btn.active { background: #f0b90b; color: #000; }

.chart-container { width: 100%; }

.show-hide label { display: flex; align-items: center; gap: 4px; color: #8b949e; font-size: 12px; cursor: pointer; }
.show-hide input { accent-color: #f0b90b; }

.orderbook { display: flex; flex-direction: column; background: #161b22; border: 1px solid #21262d; border-radius: 8px; }
.orderbook h2 { font-size: 14px; padding: 8px 12px; margin: 0; color: #e6edf3; }
.orderbook-header { display: flex; justify-content: space-between; padding: 6px 12px; font-size: 11px; color: #8b949e; border-bottom: 1px solid #21262d; }
.asks, .bids { flex: 1; overflow-y: auto; }
.order-row { display: flex; justify-content: space-between; padding: 3px 12px; font-size: 11px; }
.order-row.ask .price { color: #fc5c7d; }
.order-row.bid .price { color: #26de81; }
.order-row .qty { color: #8b949e; }
.spread { text-align: center; padding: 6px; font-size: 11px; color: #8b949e; border-top: 1px solid #21262d; border-bottom: 1px solid #21262d; }

.analysis-section {
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 12px;
  padding: 16px;
}
.analysis-header h2 { font-size: 16px; color: #e6edf3; margin: 0 0 12px 0; }
.timeline-track { display: flex; gap: 16px; overflow-x: auto; }
.timeline-node { display: flex; gap: 8px; min-width: 250px; }
.node-dot {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
}
.timeline-node.bullish .node-dot { background: rgba(38, 222, 129, 0.2); border: 2px solid #26de81; color: #26de81; }
.timeline-node.bearish .node-dot { background: rgba(252, 92, 125, 0.2); border: 2px solid #fc5c7d; color: #fc5c7d; }
.node-card { flex: 1; padding: 10px; background: #0d1117; border-radius: 8px; }
.node-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.node-type { font-size: 12px; font-weight: 600; }
.node-time { font-size: 10px; color: #8b949e; }
.node-metrics { display: flex; gap: 8px; margin-top: 6px; }
.metric { flex: 1; }
.metric-label { display: block; font-size: 9px; color: #8b949e; }
.metric-value { font-size: 11px; font-weight: 600; color: #e6edf3; }

.auto-refresh {
  position: fixed;
  bottom: 16px;
  left: 16px;
  padding: 8px 12px;
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 8px;
}
.auto-refresh label { display: flex; align-items: center; gap: 6px; color: #8b949e; font-size: 12px; cursor: pointer; }
.auto-refresh input { accent-color: #f0b90b; }
</style>