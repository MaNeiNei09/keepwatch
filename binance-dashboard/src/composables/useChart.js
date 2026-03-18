// 图表相关配置
import { ref, reactive } from 'vue'

// 高度配置
const chartHeights = reactive({
  candle: 500,
  volume: 140,
  rsi: 140,
  macd: 150,
  rsi2: 140,
  orderbook: 400
})

// 显示控制
const showVolume = ref(true)
const showMACD = ref(true)
const showRSI = ref(true)

// 更新图表高度
const updateChartHeight = (chartType) => {
  const height = chartHeights[chartType]
  console.log('Updating height:', chartType, height)

  let containerId = ''
  if (chartType === 'volume') containerId = 'volume-chart'
  else if (chartType === 'rsi') containerId = 'rsi-chart'
  else if (chartType === 'macd') containerId = 'macd-chart'
  else if (chartType === 'candle') containerId = 'tradingview-chart'
  else if (chartType === 'orderbook') containerId = 'orderbook-container'

  if (containerId) {
    const container = document.getElementById(containerId)
    if (container && container.parentElement) {
      container.parentElement.style.height = height + 'px'
    }
  }
}

export function useChartConfig() {
  return {
    chartHeights,
    showVolume,
    showMACD,
    showRSI,
    updateChartHeight
  }
}