<template>
  <div v-if="visible" class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3>指标配置</h3>
        <button class="modal-close" @click="emit('close')">×</button>
      </div>
      <div class="modal-body">
        <div class="indicator-checkboxes">
          <label class="ind-check">
            <input type="checkbox" value="ma" v-model="localIndicators" @change="emit('update', localIndicators)" />
            <span>MA</span>
          </label>
          <label class="ind-check">
            <input type="checkbox" value="ema" v-model="localIndicators" @change="emit('update', localIndicators)" />
            <span>EMA</span>
          </label>
          <label class="ind-check">
            <input type="checkbox" value="bollinger" v-model="localIndicators" @change="emit('update', localIndicators)" />
            <span>布林带</span>
          </label>
          <label class="ind-check">
            <input type="checkbox" value="rsi" v-model="localIndicators" @change="emit('update', localIndicators)" />
            <span>RSI</span>
          </label>
          <label class="ind-check">
            <input type="checkbox" value="macd" v-model="localIndicators" @change="emit('update', localIndicators)" />
            <span>MACD</span>
          </label>
          <label class="ind-check">
            <input type="checkbox" value="volume" v-model="localIndicators" @change="emit('update', localIndicators)" />
            <span>成交量</span>
          </label>
          <label class="ind-check">
            <input type="checkbox" value="atr" v-model="localIndicators" @change="emit('update', localIndicators)" />
            <span>ATR</span>
          </label>
        </div>

        <!-- MA/EMA 参数选择 -->
        <div v-if="localIndicators.includes('ma') || localIndicators.includes('ema')" class="indicator-params">
          <span class="params-label">{{ localIndicators.includes('ema') ? 'EMA' : 'MA' }}周期:</span>
          <div class="param-chips">
            <label v-for="param in (localIndicators.includes('ema') ? emaParams : maParams)" :key="param" class="param-chip">
              <input type="checkbox" :value="param" v-model="localParams" @change="emit('paramsChange', localParams)" />
              <span>{{ param }}</span>
            </label>
          </div>
        </div>

        <!-- 布林带参数 -->
        <div v-if="localIndicators.includes('bollinger')" class="indicator-params">
          <label>
            <span>周期:</span>
            <input type="number" v-model.number="localBollingerPeriod" @change="emit('bollingerChange', { period: localBollingerPeriod, stdDev: localBollingerStdDev })" min="5" max="50" style="width:50px" />
          </label>
          <label>
            <span>倍数:</span>
            <input type="number" v-model.number="localBollingerStdDev" @change="emit('bollingerChange', { period: localBollingerPeriod, stdDev: localBollingerStdDev })" min="1" max="3" step="0.5" style="width:50px" />
          </label>
        </div>

        <!-- RSI参数 -->
        <div v-if="localIndicators.includes('rsi')" class="indicator-params">
          <label>
            <span>RSI周期:</span>
            <input type="number" v-model.number="localRsiPeriod" @change="emit('rsiChange', localRsiPeriod)" min="5" max="30" style="width:50px" />
          </label>
        </div>

        <!-- ATR参数 -->
        <div v-if="localIndicators.includes('atr')" class="indicator-params atr-params">
          <label>
            <span>ATR倍数:</span>
            <input type="number" v-model.number="localAtrMultiplier" @change="emit('atrChange', localAtrMultiplier)" min="0.5" max="10" step="0.5" style="width:50px" />
          </label>
          <span class="atr-hint">上线: 价格 + {{ localAtrMultiplier }}×ATR | 下线: 价格 - {{ localAtrMultiplier }}×ATR</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  indicators: { type: Array, default: () => [] },
  params: { type: Array, default: () => [] },
  bollingerPeriod: { type: Number, default: 20 },
  bollingerStdDev: { type: Number, default: 2 },
  rsiPeriod: { type: Number, default: 14 },
  atrMultiplier: { type: Number, default: 3.5 }
})

const emit = defineEmits(['close', 'update', 'paramsChange', 'bollingerChange', 'rsiChange', 'atrChange'])

const emaParams = [7, 12, 25, 26, 50, 99, 144, 169, 200, 230]
const maParams = [7, 10, 20, 30, 60, 99, 120, 200]

const localIndicators = ref([...props.indicators])
const localParams = ref([...props.params])
const localBollingerPeriod = ref(props.bollingerPeriod)
const localBollingerStdDev = ref(props.bollingerStdDev)
const localRsiPeriod = ref(props.rsiPeriod)
const localAtrMultiplier = ref(props.atrMultiplier)

watch(() => props.indicators, (val) => {
  localIndicators.value = [...val]
}, { immediate: true })

watch(() => props.params, (val) => {
  localParams.value = [...val]
}, { immediate: true })

watch(() => props.bollingerPeriod, (val) => { localBollingerPeriod.value = val }, { immediate: true })
watch(() => props.bollingerStdDev, (val) => { localBollingerStdDev.value = val }, { immediate: true })
watch(() => props.rsiPeriod, (val) => { localRsiPeriod.value = val }, { immediate: true })
watch(() => props.atrMultiplier, (val) => { localAtrMultiplier.value = val }, { immediate: true })
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  width: 90%;
  max-width: 450px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #21262d;
}

.modal-header h3 {
  margin: 0;
  font-size: 14px;
  color: #e6edf3;
}

.modal-close {
  background: none;
  border: none;
  font-size: 20px;
  color: #8b949e;
  cursor: pointer;
}

.modal-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.indicator-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.ind-check {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: #21262d;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  color: #8b949e;
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
  border-radius: 6px;
}

.params-label {
  font-size: 11px;
  color: #8b949e;
}

.param-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.param-chip {
  display: flex;
  align-items: center;
  gap: 3px;
  padding: 2px 5px;
  background: #21262d;
  border-radius: 3px;
  font-size: 10px;
  color: #8b949e;
  cursor: pointer;
}

.param-chip input {
  width: 10px;
  height: 10px;
  accent-color: #f0b90b;
}

.param-chip:has(input:checked) {
  background: rgba(240, 185, 11, 0.3);
  color: #f0b90b;
}

.indicator-params input[type="number"] {
  background: #21262d;
  border: 1px solid #30363d;
  color: #e6edf3;
  padding: 3px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.atr-params {
  background: rgba(38, 222, 129, 0.1) !important;
  border: 1px solid rgba(38, 222, 129, 0.3);
}

.atr-hint {
  font-size: 10px;
  color: #8b949e;
  margin-left: 4px;
}
</style>