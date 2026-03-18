<template>
  <div class="dashboard">
    <!-- 头部 -->
    <header class="header">
      <h1>📊 币安实时行情 Dashboard</h1>
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
                @click="selectSymbol(symbol)"
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
                @click="selectSymbol(symbol.symbol)"
              >
                {{ formatSymbol(symbol.symbol) }}
              </div>
            </div>
            <div class="dropdown-empty" v-if="searchQuery !== '' && filteredSymbols.length === 0">
              未找到匹配的交易对
            </div>
          </div>
        </div>
        <button class="refresh-btn" @click="fetchAllData" :disabled="loading">
          {{ loading ? '刷新中...' : '🔄 刷新' }}
        </button>
      </div>
    </header>

    <main class="main-content">
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
          <!-- K线走势图 -->
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
                <button class="indicator-btn" @click="showIndicatorModal = true">
                  <span class="indicator-icon">⚙️</span>
                  指标配置
                </button>
              </div>
            </div>
            <div class="resize-corner" @mousedown.stop="startResize($event, 'candle')"></div>
            <div class="chart-container main-chart" :style="{ height: chartHeights.candle + 'px' }">
              <div id="tradingview-chart"></div>
            </div>
          </div>

          <!-- 成交量图表 -->
          <div class="chart-section volume-section">
            <div class="section-header">
              <h2>成交量</h2>
              <div class="show-hide">
                <label>
                  <input type="checkbox" v-model="showVolume" @change="updateVolumeChart" />
                  显示
                </label>
              </div>
            </div>
            <div class="resize-corner" @mousedown.stop="startResize($event, 'volume')"></div>
            <div class="chart-container volume-chart" v-show="showVolume" :style="{ height: chartHeights.volume + 'px' }">
              <div id="volume-chart"></div>
            </div>
          </div>

          <!-- RSI图表 -->
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
            <div class="resize-corner" @mousedown.stop="startResize($event, 'rsi')"></div>
            <div class="chart-container rsi-chart" v-show="showRSI" :style="{ height: chartHeights.rsi + 'px' }">
              <div id="rsi-chart"></div>
              <div class="rsi-zones">
                <div class="rsi-zone overbought">超买区 (>70)</div>
                <div class="rsi-zone neutral">正常区 (30-70)</div>
                <div class="rsi-zone oversold">超卖区 (<30)</div>
              </div>
            </div>
          </div>

          <!-- MACD图表 -->
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
            <div class="resize-corner" @mousedown.stop="startResize($event, 'macd')"></div>
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
            <div class="resize-corner" @mousedown.stop="startResize($event, 'orderbook')"></div>
          </div>
        </div>
      </section>

      <!-- 智能分析时间线 -->
      <section class="analysis-section">
        <div class="analysis-header">
          <h2>🧠 智能趋势分析</h2>
          <span class="analysis-subtitle">基于 1H/4H/1D 多周期趋势追踪</span>
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
                <div class="node-tf-status" v-if="node.tfStatus">{{ node.tfStatus }}</div>
                <div class="node-metrics">
                  <div class="metric">
                    <span class="metric-label">持续时间</span>
                    <span class="metric-value large">{{ node.duration }}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">涨跌幅度</span>
                    <span :class="['metric-value', 'large', parseFloat(node.changePercent) >= 0 ? 'positive' : 'negative']">
                      {{ node.changePercent >= 0 ? '+' : '' }}{{ node.changePercent }}%
                    </span>
                  </div>
                </div>
                <div class="node-metrics">
                  <div class="metric">
                    <span class="metric-label">入场价格</span>
                    <span class="metric-value">{{ node.entryPrice }}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">当前价格</span>
                    <span class="metric-value">{{ node.currentPrice }}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">趋势阶段</span>
                    <span :class="['metric-value', node.stageClass]">{{ node.stageLabel }}</span>
                  </div>
                </div>
                <div class="node-badge" v-if="node.isCurrent">进行中</div>
              </div>
            </div>
          </div>
          <div v-if="trendNodes.length === 0" class="no-data">
            <span>暂无趋势分析数据，请等待数据加载...</span>
          </div>
        </div>
      </section>
    </main>

    <!-- 指标配置弹窗 -->
    <IndicatorModal
      :visible="showIndicatorModal"
      :indicators="selectedIndicators"
      :params="selectedParams"
      :bollinger-period="bollingerPeriod"
      :bollinger-std-dev="bollingerStdDev"
      :rsi-period="rsiPeriod"
      :atr-multiplier="atrMultiplier"
      @close="showIndicatorModal = false"
      @update="handleIndicatorsUpdate"
      @paramsChange="handleParamsChange"
      @bollingerChange="handleBollingerChange"
      @rsiChange="handleRsiChange"
      @atrChange="handleAtrChange"
    />

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
import { ref, reactive, onMounted, onUnmounted, watch, computed } from 'vue'
import axios from 'axios'
import { createChart, CrosshairMode } from 'lightweight-charts'

// 导入组件
import PriceCard from '@/components/cards/PriceCard.vue'
import CycleCard from '@/components/cards/CycleCard.vue'
import DecisionCard from '@/components/cards/DecisionCard.vue'
import PositionCard from '@/components/cards/PositionCard.vue'
import IndicatorModal from '@/components/common/IndicatorModal.vue'

// 导入 composables
import { useTrading } from '@/composables/useTrading'
import { useChart } from '@/composables/useChart'
import { useMarketData } from '@/composables/useMarketData'
import { useIndicators } from '@/composables/useIndicators'
import { useDecision } from '@/composables/useDecision'
import { createChart, CrosshairMode } from 'lightweight-charts'

// 使用 composables
const {
  selectedSymbol,
  searchQuery,
  showDropdown,
  searchWrapper,
  allSymbols,
  defaultSymbols,
  filteredSymbols,
  selectSymbol,
  formatSymbol,
  onSearchInput,
  getCoinIcon,
  setAllSymbols,
  closeDropdown
} = useTrading()

const {
  chartHeights,
  showVolume,
  showMACD,
  showRSI,
  updateChartHeight
} = useChartConfig()

const {
  tickerData,
  ticker24h,
  orderbook,
  klines,
  spread,
  maxAskQty,
  maxBidQty,
  formatPrice,
  formatNumber,
  fetchTicker,
  fetchOrderbook,
  fetchKlines,
  fetchAllSymbols,
  updateOrderbookMetrics
} = useMarketData()

const {
  selectedIndicators,
  selectedInterval,
  selectedParams,
  bollingerPeriod,
  bollingerStdDev,
  rsiPeriod,
  atrMultiplier,
  intervals,
  calculateMA,
  calculateEMA,
  calculateRSI,
  calculateMACD,
  calculateBollingerBands,
  calculateATR
} = useIndicators()

const {
  config,
  mtfData,
  decision,
  trendNodes,
  calculateDecision,
  generateTrendNodes
} = useDecision()

// 本地状态
const loading = ref(false)
const autoRefresh = ref(true)
const showIndicatorModal = ref(false)
let refreshInterval = null
let orderbookInterval = null

// 图表引用
let volumeChart = null
let rsiChart = null
let macdChart = null
let volumeSeries = null
let rsiLineSeries = null
let rsiUpperBand = null
let rsiLowerBand = null
let histogramSeries = null
let macdLineSeries = null
let signalLineSeries = null

// 拖拽调整高度
const isResizing = ref(false)
const resizeChartType = ref('')
let startY = 0
let startHeight = 0

const startResize = (event, chartType) => {
  event.preventDefault()
  event.stopPropagation()
  isResizing.value = true
  resizeChartType.value = chartType
  startY = event.clientY
  startHeight = chartHeights[chartType]

  window.addEventListener('mousemove', doResize)
  window.addEventListener('mouseup', stopResize)
  document.body.style.cursor = 'ns-resize'
  document.body.style.userSelect = 'none'
}

const doResize = (event) => {
  if (!isResizing.value) return
  const deltaY = event.clientY - startY
  const maxHeight = resizeChartType.value === 'orderbook' ? 1500 : 800
  const newHeight = Math.max(80, Math.min(maxHeight, startHeight + deltaY))
  chartHeights[resizeChartType.value] = newHeight
  updateChartHeight(resizeChartType.value)
}

const stopResize = () => {
  isResizing.value = false
  window.removeEventListener('mousemove', doResize)
  window.removeEventListener('mouseup', stopResize)
  document.body.style.cursor = ''
  document.body.style.userSelect = ''
}

// 切换K线周期
const changeInterval = (interval) => {
  selectedInterval.value = interval
  fetchKlines(selectedSymbol.value, interval, 200)
  initTradingView()
}

// 初始化TradingView
const initTradingView = () => {
  // 动态加载TradingView脚本
  const script = document.createElement('script')
  script.src = 'https://s3.tradingview.com/tv.js'
  script.onload = () => {
    if (window.TradingView) {
      new window.TradingView.widget({
        autosize: true,
        symbol: `BINANCE:${selectedSymbol.value}`,
        interval: selectedInterval.value,
        timezone: 'Asia/Shanghai',
        theme: 'dark',
        style: '1',
        locale: 'zh_CN',
        toolbar_bg: '#161b22',
        enable_publishing: false,
        allow_symbol_change: false,
        hide_side_toolbar: false,
        container_id: 'tradingview-chart'
      })
      console.log('TradingView 图表初始化完成')
    }
  }
  document.head.appendChild(script)
}

// 初始化成交量图表
const initVolumeChart = () => {
  const container = document.getElementById('volume-chart')
  if (!container) return

  volumeChart = createChart(container, {
    layout: { background: { color: '#161b22' }, textColor: '#d1d5db' },
    grid: { vertLines: { color: '#21262d' }, horzLines: { color: '#21262d' } },
    rightPriceScale: { borderColor: '#30363d' },
    timeScale: { borderColor: '#30363d', timeVisible: true, secondsVisible: false },
    height: chartHeights.volume
  })

  volumeSeries = volumeChart.addHistogramSeries({
    color: '#26a69a',
    priceFormat: { type: 'volume' },
    priceScaleId: 'volume'
  })

  const resizeObserver = new ResizeObserver(entries => {
    if (entries.length === 0 || !volumeChart) return
    const newRect = entries[0].contentRect
    volumeChart.applyOptions({ width: newRect.width, height: newRect.height })
  })
  resizeObserver.observe(container)
}

// 初始化RSI图表
const initRSIChart = () => {
  const container = document.getElementById('rsi-chart')
  if (!container) return

  rsiChart = createChart(container, {
    width: container.clientWidth,
    height: chartHeights.rsi,
    layout: { background: { type: 'solid', color: '#161b22' }, textColor: '#8b949e' },
    grid: { vertLines: { color: '#21262d' }, horzLines: { color: '#21262d' } },
    rightPriceScale: { borderColor: '#30363d', scaleMargins: { top: 0.1, bottom: 0.1 } },
    timeScale: { borderColor: '#30363d', visible: false },
    crosshair: { mode: CrosshairMode.Normal }
  })

  rsiUpperBand = rsiChart.addLineSeries({
    color: '#fc5c7d', lineWidth: 1, lineStyle: 2, priceLineVisible: false, crosshairMarkerVisible: false
  })
  rsiLowerBand = rsiChart.addLineSeries({
    color: '#26de81', lineWidth: 1, lineStyle: 2, priceLineVisible: false, crosshairMarkerVisible: false
  })
  rsiLineSeries = rsiChart.addLineSeries({ color: '#9b59b6', lineWidth: 2, priceLineVisible: false })

  const rsiResizeObserver = new ResizeObserver(entries => {
    if (entries.length === 0 || !rsiChart) return
    const newRect = entries[0].contentRect
    rsiChart.applyOptions({ width: newRect.width, height: newRect.height })
  })
  rsiResizeObserver.observe(container)
}

// 初始化MACD图表
const initMACDChart = () => {
  const container = document.getElementById('macd-chart')
  if (!container) return

  macdChart = createChart(container, {
    layout: { background: { color: '#161b22' }, textColor: '#d1d5db' },
    grid: { vertLines: { color: '#21262d' }, horzLines: { color: '#21262d' } },
    rightPriceScale: { borderColor: '#30363d' },
    timeScale: { borderColor: '#30363d', timeVisible: true, secondsVisible: false },
    height: chartHeights.macd
  })

  histogramSeries = macdChart.addHistogramSeries({ priceScaleId: 'histogram' })
  macdLineSeries = macdChart.addLineSeries({ color: '#2196F3', lineWidth: 2, priceLineVisible: false, crosshairMarkerVisible: false, priceScaleId: 'macd' })
  signalLineSeries = macdChart.addLineSeries({ color: '#FF9800', lineWidth: 2, priceLineVisible: false, crosshairMarkerVisible: false, priceScaleId: 'macd' })

  macdChart.priceScale('histogram').applyOptions({ scaleMargins: { top: 0.1, bottom: 0.1 } })
  macdChart.priceScale('macd').applyOptions({ scaleMargins: { top: 0.1, bottom: 0.1 } })

  const resizeObserver = new ResizeObserver(entries => {
    if (entries.length === 0 || !macdChart) return
    const newRect = entries[0].contentRect
    macdChart.applyOptions({ width: newRect.width, height: newRect.height })
  })
  resizeObserver.observe(container)
}

// 数据格式化
const formatVolumeData = () => {
  return klines.value.map(k => ({
    time: k[0] / 1000,
    value: parseFloat(k[5]),
    color: parseFloat(k[4]) >= parseFloat(k[1]) ? 'rgba(38, 222, 129, 0.5)' : 'rgba(252, 92, 125, 0.5)'
  }))
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

// 计算MACD
const calculateMACDForChart = (fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) => {
  const closes = klines.value.map(k => parseFloat(k[4]))

  const calculateEma = (period) => {
    const k = 2 / (period + 1)
    let ema = closes.slice(0, period).reduce((a, b) => a + b, 0) / period
    const result = [ema]
    for (let i = 1; i < closes.length; i++) {
      ema = closes[i] * k + ema * (1 - k)
      result.push(ema)
    }
    return result
  }

  const fastEMA = calculateEma(fastPeriod)
  const slowEMA = calculateEma(slowPeriod)

  const macdLine = closes.map((_, i) => fastEMA[i] - slowEMA[i])

  const k = 2 / (signalPeriod + 1)
  let signal = macdLine.slice(slowPeriod, slowPeriod + signalPeriod).reduce((a, b) => a + b, 0) / signalPeriod
  const signalLine = []

  for (let i = 0; i < macdLine.length; i++) {
    if (i < slowPeriod + signalPeriod - 1) {
      signalLine.push(null)
    } else if (i === slowPeriod + signalPeriod - 1) {
      signalLine.push(signal)
    } else {
      signal = macdLine[i] * k + signal * (1 - k)
      signalLine.push(signal)
    }
  }

  const histogram = macdLine.map((macd, i) => {
    if (macd === null || signalLine[i] === null) return null
    return macd - signalLine[i]
  })

  return { macdLine, signalLine, histogram }
}

// 更新MACD图表
const updateMACDChart = () => {
  if (!macdLineSeries || !klines.value.length) return

  const { macdLine, signalLine, histogram } = calculateMACDForChart()

  const macdData = macdLine.map((v, i) => ({
    time: klines.value[i][0] / 1000,
    value: v
  })).filter(d => d.value !== null)

  const signalData = signalLine.map((v, i) => ({
    time: klines.value[i][0] / 1000,
    value: v
  })).filter(d => d.value !== null)

  const histData = histogram.map((v, i) => ({
    time: klines.value[i][0] / 1000,
    value: v,
    color: v >= 0 ? 'rgba(38, 222, 129, 0.8)' : 'rgba(252, 92, 125, 0.8)'
  })).filter(d => d.value !== null)

  macdLineSeries.setData(macdData)
  signalLineSeries.setData(signalData)
  histogramSeries.setData(histData)
  histogramSeries.applyOptions({ visible: showMACD.value })
  macdLineSeries.applyOptions({ visible: showMACD.value })
  signalLineSeries.applyOptions({ visible: showMACD.value })

  if (macdChart) {
    macdChart.timeScale().fitContent()
  }
}

// 更新RSI图表
const updateRSIChart = () => {
  if (!rsiLineSeries || !klines.value.length) return

  const rsiData = calculateRSI(klines.value, rsiPeriod.value)
  rsiLineSeries.setData(rsiData)
  rsiLineSeries.applyOptions({ visible: showRSI.value })

  if (rsiUpperBand && rsiLowerBand && rsiData.length > 0) {
    const upperData = rsiData.map(d => ({ time: d.time, value: 70 }))
    const lowerData = rsiData.map(d => ({ time: d.time, value: 30 }))
    rsiUpperBand.setData(upperData)
    rsiLowerBand.setData(lowerData)
  }

  if (rsiChart) {
    rsiChart.timeScale().fitContent()
  }
}

// 更新指标
const updateIndicators = () => {
  console.log('更新指标:', selectedIndicators.value)
  // 指标更新逻辑
}

// 处理指标配置弹窗事件
const handleIndicatorsUpdate = (indicators) => {
  selectedIndicators.value = indicators
  updateIndicators()
}

const handleParamsChange = (params) => {
  selectedParams.value = params
  updateIndicators()
}

const handleBollingerChange = ({ period, stdDev }) => {
  bollingerPeriod.value = period
  bollingerStdDev.value = stdDev
  updateIndicators()
}

const handleRsiChange = (period) => {
  rsiPeriod.value = period
  updateRSIChart()
}

const handleAtrChange = (multiplier) => {
  atrMultiplier.value = multiplier
}

// 切换自动刷新
const toggleAutoRefresh = () => {
  if (autoRefresh.value) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}

const startAutoRefresh = () => {
  if (refreshInterval) clearInterval(refreshInterval)
  refreshInterval = setInterval(() => {
    fetchAllData()
  }, 5000)
}

const stopAutoRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

// 获取所有数据
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

    // 更新图表
    if (volumeSeries) updateVolumeChart()
    if (rsiLineSeries) updateRSIChart()
    if (macdLineSeries) updateMACDChart()

    // 计算决策
    calculateDecision(klines.value, tickerData.value, ticker24h.value, atrMultiplier.value)
    generateTrendNodes(klines.value)

  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 初始化
onMounted(async () => {
  // 加载交易对列表
  await fetchAllSymbols()

  // 初始化图表
  initVolumeChart()
  initRSIChart()
  initMACDChart()
  initTradingView()

  // 加载数据
  await fetchAllData()

  // 启动自动刷新
  startAutoRefresh()

  // 点击外部关闭下拉框
  document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
  stopAutoRefresh()
  document.removeEventListener('click', closeDropdown)
})

// 监听交易对变化
watch(selectedSymbol, () => {
  fetchAllData()
})
</script>

<style scoped>
/* 组件特定样式 - 使用全局样式 */

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 8px;
}

.section-header h2 {
  font-size: 14px;
  color: #e6edf3;
  margin: 0;
}

.chart-controls {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.interval-selector {
  display: flex;
  gap: 4px;
}

.interval-btn {
  padding: 4px 8px;
  background: #21262d;
  color: #8b949e;
  border: none;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
}

.interval-btn:hover {
  background: #30363d;
}

.interval-btn.active {
  background: #f0b90b;
  color: #000;
}

.indicator-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 4px;
  color: #8b949e;
  font-size: 11px;
  cursor: pointer;
}

.indicator-btn:hover {
  background: #30363d;
  color: #e6edf3;
}

.show-hide label {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #8b949e;
  font-size: 12px;
  cursor: pointer;
}

.show-hide input {
  accent-color: #f0b90b;
}

.main-chart-section,
.volume-section,
.rsi-section,
.macd-section {
  position: relative;
}

.volume-section,
.rsi-section,
.macd-section {
  margin-top: 12px;
}

.main-chart {
  width: 100%;
  position: relative;
}

.volume-chart,
.rsi-chart,
.macd-chart {
  width: 100%;
  position: relative;
}

.rsi-zones {
  position: absolute;
  top: 8px;
  right: 30px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 10px;
  z-index: 5;
}

.rsi-zone {
  padding: 2px 6px;
  border-radius: 3px;
  opacity: 0.8;
}

.rsi-zone.overbought {
  background: rgba(252, 92, 125, 0.3);
  color: #fc5c7d;
}

.rsi-zone.oversold {
  background: rgba(38, 222, 129, 0.3);
  color: #26de81;
}

.rsi-zone.neutral {
  background: rgba(139, 148, 158, 0.2);
  color: #8b949e;
}

/* 订单簿 */
.orderbook h2 {
  font-size: 14px;
  margin-bottom: 8px;
  color: #e6edf3;
}

.orderbook {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.orderbook-header {
  display: flex;
  justify-content: space-between;
  padding: 6px 8px;
  font-size: 11px;
  color: #8b949e;
  border-bottom: 1px solid #21262d;
  flex-shrink: 0;
}

.asks,
.bids {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

.order-row {
  display: flex;
  justify-content: space-between;
  padding: 3px 8px;
  font-size: 11px;
  position: relative;
}

.order-row.ask .price {
  color: #fc5c7d;
}

.order-row.bid .price {
  color: #26de81;
}

.order-row .qty {
  color: #8b949e;
}

.depth-bar {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  opacity: 0.15;
}

.ask-bar {
  background: #fc5c7d;
}

.bid-bar {
  background: #26de81;
}

.spread {
  text-align: center;
  padding: 6px;
  font-size: 11px;
  color: #8b949e;
  border-top: 1px solid #21262d;
  border-bottom: 1px solid #21262d;
  flex-shrink: 0;
}
</style>