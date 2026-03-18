<template>
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
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useChart } from '@/composables/useChart'
import { useIndicators } from '@/composables/useIndicators'

const { chartHeights, initTradingViewChart, updateChartHeight } = useChart()
const { intervals, selectedInterval, selectedIndicators, selectedParams, bollingerPeriod, bollingerStdDev, rsiPeriod, atrMultiplier } = useIndicators()

const showIndicatorModal = ref(false)

// 切换周期
const changeInterval = (interval) => {
  selectedInterval.value = interval
  // 重新加载K线数据 - 事件通知父组件
}

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
  const maxHeight = 800
  const newHeight = Math.max(200, Math.min(maxHeight, startHeight + deltaY))
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

const emit = defineEmits(['intervalChange', 'updateIndicators', 'openIndicatorModal'])

// 暴露给父组件
defineExpose({
  showIndicatorModal
})
</script>

<style scoped>
.main-chart-section {
  position: relative;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 12px;
}

.section-header h2 {
  font-size: 16px;
  color: #e6edf3;
  margin: 0;
}

.chart-controls {
  display: flex;
  gap: 12px;
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
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
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
  font-size: 12px;
  cursor: pointer;
}

.indicator-btn:hover {
  background: #30363d;
  color: #e6edf3;
}

.main-chart {
  width: 100%;
  position: relative;
}
</style>