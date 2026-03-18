<template>
  <div class="chart-section macd-section">
    <div class="section-header">
      <h2>MACD (12, 26, 9)</h2>
      <div class="show-hide">
        <label>
          <input type="checkbox" v-model="localShowMACD" @change="emit('update')" />
          显示
        </label>
      </div>
    </div>
    <div class="resize-corner" @mousedown.stop="emit('resizeStart', $event, 'macd')"></div>
    <div class="chart-container macd-chart" v-show="localShowMACD" :style="{ height: height + 'px' }">
      <div id="macd-chart"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  height: { type: Number, default: 150 },
  showMACD: { type: Boolean, default: true }
})

const emit = defineEmits(['update', 'resizeStart'])

const localShowMACD = ref(props.showMACD)

watch(() => props.showMACD, (val) => {
  localShowMACD.value = val
})
</script>

<style scoped>
.macd-section {
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

.macd-chart {
  width: 100%;
  position: relative;
}
</style>