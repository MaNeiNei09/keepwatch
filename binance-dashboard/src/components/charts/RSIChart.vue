<template>
  <div class="chart-section rsi-section">
    <div class="section-header">
      <h2>RSI (14)</h2>
      <div class="show-hide">
        <label>
          <input type="checkbox" v-model="localShowRSI" @change="emit('update')" />
          显示
        </label>
      </div>
    </div>
    <div class="resize-corner" @mousedown.stop="emit('resizeStart', $event, 'rsi')"></div>
    <div class="chart-container rsi-chart" v-show="localShowRSI" :style="{ height: height + 'px' }">
      <div id="rsi-chart"></div>
      <div class="rsi-zones">
        <div class="rsi-zone overbought">超买区 (>70)</div>
        <div class="rsi-zone neutral">正常区 (30-70)</div>
        <div class="rsi-zone oversold">超卖区 (<30)</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  height: { type: Number, default: 140 },
  showRSI: { type: Boolean, default: true }
})

const emit = defineEmits(['update', 'resizeStart'])

const localShowRSI = ref(props.showRSI)

watch(() => props.showRSI, (val) => {
  localShowRSI.value = val
})
</script>

<style scoped>
.rsi-section {
  margin-top: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.section-header h2 {
  font-size: 14px;
  color: #e6edf3;
  margin: 0;
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

.rsi-chart {
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
</style>