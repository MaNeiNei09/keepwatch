<template>
  <div class="chart-section volume-section">
    <div class="section-header">
      <h2>成交量</h2>
      <div class="show-hide">
        <label>
          <input type="checkbox" v-model="showVolume" @change="emit('update')" />
          显示
        </label>
      </div>
    </div>
    <div class="resize-corner" @mousedown.stop="emit('resizeStart', $event, 'volume')"></div>
    <div class="chart-container volume-chart" v-show="showVolume" :style="{ height: height + 'px' }">
      <div id="volume-chart"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  height: { type: Number, default: 140 },
  showVolume: { type: Boolean, default: true }
})

const emit = defineEmits(['update', 'resizeStart'])

const showVolume = ref(props.showVolume)

watch(() => props.showVolume, (val) => {
  showVolume.value = val
})
</script>

<style scoped>
.volume-section {
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

.volume-chart {
  width: 100%;
  position: relative;
}
</style>