<template>
  <div class="ai-analysis">
    <div class="section-header">
      <h3>🤖 AI 智能分析</h3>
      <button class="analyze-btn" @click="runAnalysis" :disabled="isAnalyzing">
        {{ isAnalyzing ? '分析中...' : '重新分析' }}
      </button>
    </div>

    <!-- 市场情绪指标 -->
    <div class="sentiment-gauge">
      <div class="gauge-label">
        <span>市场情绪</span>
        <span :class="sentimentClass">{{ sentimentLabel }}</span>
      </div>
      <div class="gauge-bar">
        <div class="gauge-fill" :style="{ width: sentimentWidth + '%' }"></div>
        <div class="gauge-marker" :style="{ left: sentimentWidth + '%' }"></div>
      </div>
      <div class="gauge-labels">
        <span>极度恐慌</span>
        <span>恐慌</span>
        <span>中性</span>
        <span>贪婪</span>
        <span>极度贪婪</span>
      </div>
    </div>

    <!-- 分析内容 -->
    <div class="analysis-content">
      <div v-if="isAnalyzing" class="loading-state">
        <div class="pulse-loader"></div>
        <span>AI 正在分析市场数据...</span>
      </div>

      <template v-else>
        <!-- 综合诊断 -->
        <div class="diagnosis-section">
          <h4>📊 市场诊断</h4>
          <p class="diagnosis-text">{{ analysis.diagnosis }}</p>
        </div>

        <!-- 关键信号 -->
        <div class="signals-section">
          <h4>⚠️ 关键信号</h4>
          <div class="signal-list">
            <div
              v-for="(signal, index) in analysis.signals"
              :key="index"
              :class="['signal-item', signal.type]"
            >
              <span class="signal-icon">{{ signal.type === 'bullish' ? '📈' : signal.type === 'bearish' ? '📉' : '➡️' }}</span>
              <span class="signal-text">{{ signal.text }}</span>
            </div>
          </div>
        </div>

        <!-- 重点交易对分析 -->
        <div class="pairs-analysis">
          <h4>🎯 重点币种</h4>
          <div class="pair-cards">
            <div
              v-for="pair in analysis.pairAnalysis"
              :key="pair.symbol"
              class="pair-card"
            >
              <div class="pair-header">
                <span class="pair-symbol">{{ pair.symbol }}</span>
                <span :class="['pair-rating', pair.rating]">{{ pair.ratingLabel }}</span>
              </div>
              <p class="pair-advice">{{ pair.advice }}</p>
              <div class="pair-levels">
                <div class="level">
                  <span>支撑</span>
                  <span class="value support">${{ pair.support }}</span>
                </div>
                <div class="level">
                  <span>阻力</span>
                  <span class="value resistance">${{ pair.resistance }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作建议 -->
        <div class="suggestion-section">
          <h4>💡 操作建议</h4>
          <div class="suggestion-list">
            <div
              v-for="(suggestion, index) in analysis.suggestions"
              :key="index"
              class="suggestion-item"
            >
              <span class="suggestion-icon">{{ suggestion.icon }}</span>
              <span class="suggestion-text">{{ suggestion.text }}</span>
            </div>
          </div>
        </div>
      </template>
    </div>

    <div class="disclaimer">
      ⚠️ 以上分析仅供参考，不构成投资建议
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const isAnalyzing = ref(false)
const sentimentScore = ref(65) // 0-100, 恐惧贪婪指数

const analysis = ref({
  diagnosis: '当前市场处于震荡上行趋势，BTC在关键支撑位上方企稳，ETH跟随大盘走势。整体市场情绪偏向乐观，但需警惕短期回调风险。建议保持适度仓位，关注关键支撑位表现。',
  signals: [
    { type: 'bullish', text: 'BTC连续3日收于50日均线上方' },
    { type: 'bullish', text: 'ETF资金持续净流入，机构需求强劲' },
    { type: 'bearish', text: 'RSI进入超买区域，短期可能回调' },
    { type: 'neutral', text: '成交量略有萎缩，观望情绪升温' }
  ],
  pairAnalysis: [
    {
      symbol: 'BTC',
      rating: 'buy',
      ratingLabel: '买入',
      advice: '回调至支撑位可考虑分批建仓',
      support: '67,500',
      resistance: '73,000'
    },
    {
      symbol: 'ETH',
      rating: 'hold',
      ratingLabel: '持有',
      advice: '等待突破关键阻力位再操作',
      support: '3,200',
      resistance: '3,800'
    },
    {
      symbol: 'SOL',
      rating: 'buy',
      ratingLabel: '买入',
      advice: '生态活跃度提升，中期看好',
      support: '140',
      resistance: '180'
    }
  ],
  suggestions: [
    { icon: '🎯', text: '控制仓位在50%-70%，保持灵活' },
    { icon: '🛡️', text: '设置止损位，保护本金安全' },
    { icon: '📊', text: '关注ETF资金流向和市场情绪变化' },
    { icon: '⏰', text: '本周关注美联储会议纪要发布' }
  ]
})

const sentimentLabel = computed(() => {
  if (sentimentScore.value >= 80) return '极度贪婪'
  if (sentimentScore.value >= 60) return '贪婪'
  if (sentimentScore.value >= 40) return '中性'
  if (sentimentScore.value >= 20) return '恐慌'
  return '极度恐慌'
})

const sentimentClass = computed(() => {
  if (sentimentScore.value >= 80) return 'extreme-greed'
  if (sentimentScore.value >= 60) return 'greed'
  if (sentimentScore.value >= 40) return 'neutral'
  if (sentimentScore.value >= 20) return 'fear'
  return 'extreme-fear'
})

const sentimentWidth = computed(() => sentimentScore.value)

const runAnalysis = async () => {
  isAnalyzing.value = true
  await new Promise(r => setTimeout(r, 2000))
  isAnalyzing.value = false
}
</script>

<style scoped>
.ai-analysis {
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 12px;
  padding: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-header h3 {
  font-size: 14px;
  font-weight: 600;
  color: #e6edf3;
  margin: 0;
}

.analyze-btn {
  padding: 4px 10px;
  background: #21262d;
  border: 1px solid #30363d;
  color: #e6edf3;
  font-size: 11px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s;
}

.analyze-btn:hover:not(:disabled) {
  background: #30363d;
}

.analyze-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 情绪仪表 */
.sentiment-gauge {
  margin-bottom: 16px;
}

.gauge-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-size: 12px;
  color: #7d8590;
}

.gauge-label .greed, .gauge-label .extreme-greed {
  color: #3fb950;
}

.gauge-label .neutral {
  color: #7d8590;
}

.gauge-label .fear, .gauge-label .extreme-fear {
  color: #f85149;
}

.gauge-bar {
  height: 8px;
  background: linear-gradient(to right, #f85149, #f0883e, #7d8590, #3fb950, #238636);
  border-radius: 4px;
  position: relative;
}

.gauge-marker {
  position: absolute;
  top: -4px;
  width: 16px;
  height: 16px;
  background: #fff;
  border-radius: 50%;
  transform: translateX(-50%);
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.gauge-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 4px;
  font-size: 9px;
  color: #484f58;
}

/* 分析内容 */
.analysis-content {
  flex: 1;
  overflow-y: auto;
}

.analysis-content::-webkit-scrollbar {
  width: 4px;
}

.analysis-content::-webkit-scrollbar-thumb {
  background: #30363d;
  border-radius: 2px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #7d8590;
  font-size: 12px;
  gap: 12px;
}

.pulse-loader {
  width: 32px;
  height: 32px;
  border: 3px solid #21262d;
  border-top-color: #f0b90b;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 诊断 */
.diagnosis-section {
  margin-bottom: 12px;
}

.diagnosis-section h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 6px 0;
}

.diagnosis-text {
  font-size: 11px;
  color: #7d8590;
  line-height: 1.6;
  margin: 0;
  padding: 8px;
  background: #0d1117;
  border-radius: 6px;
}

/* 信号 */
.signals-section {
  margin-bottom: 12px;
}

.signals-section h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 6px 0;
}

.signal-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.signal-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  background: #0d1117;
  border-radius: 4px;
  font-size: 11px;
}

.signal-item.bullish {
  border-left: 2px solid #3fb950;
}

.signal-item.bearish {
  border-left: 2px solid #f85149;
}

.signal-item.neutral {
  border-left: 2px solid #7d8590;
}

.signal-icon {
  font-size: 12px;
}

.signal-text {
  color: #e6edf3;
}

/* 币种分析 */
.pairs-analysis {
  margin-bottom: 12px;
}

.pairs-analysis h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 6px 0;
}

.pair-cards {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.pair-card {
  padding: 8px;
  background: #0d1117;
  border-radius: 6px;
}

.pair-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.pair-symbol {
  font-size: 12px;
  font-weight: 600;
  color: #e6edf3;
}

.pair-rating {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 3px;
}

.pair-rating.buy {
  background: rgba(63, 185, 80, 0.2);
  color: #3fb950;
}

.pair-rating.hold {
  background: rgba(240, 185, 11, 0.2);
  color: #f0b90b;
}

.pair-rating.sell {
  background: rgba(248, 81, 73, 0.2);
  color: #f85149;
}

.pair-advice {
  font-size: 10px;
  color: #7d8590;
  margin: 0 0 6px 0;
}

.pair-levels {
  display: flex;
  gap: 12px;
  font-size: 10px;
}

.level {
  display: flex;
  gap: 4px;
  color: #484f58;
}

.level .value {
  font-weight: 500;
}

.level .support {
  color: #3fb950;
}

.level .resistance {
  color: #f85149;
}

/* 建议 */
.suggestion-section {
  margin-bottom: 12px;
}

.suggestion-section h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 6px 0;
}

.suggestion-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  background: #0d1117;
  border-radius: 4px;
  font-size: 11px;
  color: #7d8590;
}

.suggestion-icon {
  font-size: 12px;
}

.disclaimer {
  margin-top: auto;
  padding-top: 8px;
  font-size: 10px;
  color: #484f58;
  text-align: center;
  border-top: 1px solid #21262d;
}
</style>