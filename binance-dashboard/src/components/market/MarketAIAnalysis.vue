<template>
  <div class="market-ai-analysis">
    <div class="section-header">
      <h3>🌍 宏观市场分析</h3>
      <button class="analyze-btn" @click="runAnalysis" :disabled="isAnalyzing">
        {{ isAnalyzing ? '分析中...' : '刷新分析' }}
      </button>
    </div>

    <div class="analysis-content">
      <div v-if="isAnalyzing" class="loading-state">
        <div class="pulse-loader"></div>
        <span>正在分析宏观经济数据...</span>
      </div>

      <template v-else>
        <!-- 市场情绪仪表 -->
        <div class="sentiment-section">
          <div class="sentiment-gauge">
            <div class="gauge-label">
              <span>整体市场情绪</span>
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
        </div>

        <!-- 今日重点关注 -->
        <div class="focus-section">
          <h4>📅 今日重点关注</h4>
          <div class="event-cards">
            <div
              v-for="event in todayEvents"
              :key="event.id"
              :class="['event-card', event.impact]"
            >
              <div class="event-time">{{ event.time }}</div>
              <div class="event-title">{{ event.title }}</div>
              <div class="event-importance">
                <span v-for="i in event.importance" :key="i" class="star">★</span>
              </div>
              <div class="event-effect">{{ event.effect }}</div>
            </div>
          </div>
        </div>

        <!-- 宏观经济分析 -->
        <div class="macro-section">
          <h4>🏦 宏观经济影响</h4>
          <div class="macro-factors">
            <div
              v-for="factor in macroFactors"
              :key="factor.name"
              :class="['factor-item', factor.impact]"
            >
              <div class="factor-header">
                <span class="factor-icon">{{ factor.icon }}</span>
                <span class="factor-name">{{ factor.name }}</span>
                <span :class="['factor-effect', factor.impact]">{{ factor.effectLabel }}</span>
              </div>
              <p class="factor-desc">{{ factor.description }}</p>
            </div>
          </div>
        </div>

        <!-- 市场概况诊断 -->
        <div class="diagnosis-section">
          <h4>📊 市场概况诊断</h4>
          <p class="diagnosis-text">{{ marketDiagnosis }}</p>
        </div>

        <!-- 突发事件影响 -->
        <div class="breaking-section">
          <h4>⚡ 突发事件影响</h4>
          <div v-if="breakingEvents.length === 0" class="no-events">
            暂无重大突发事件
          </div>
          <div v-else class="breaking-list">
            <div
              v-for="event in breakingEvents"
              :key="event.id"
              :class="['breaking-item', event.severity]"
            >
              <div class="breaking-header">
                <span class="breaking-icon">{{ event.icon }}</span>
                <span class="breaking-title">{{ event.title }}</span>
                <span class="breaking-time">{{ event.time }}</span>
              </div>
              <p class="breaking-impact">{{ event.impact }}</p>
              <div class="breaking-effect">
                <span class="label">市场影响：</span>
                <span :class="['effect-value', event.marketEffect]">{{ event.effectDescription }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作建议 -->
        <div class="suggestion-section">
          <h4>💡 今日策略建议</h4>
          <div class="suggestion-list">
            <div
              v-for="(suggestion, index) in suggestions"
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

const props = defineProps({
  globalMetrics: {
    type: Object,
    default: () => ({})
  }
})

const isAnalyzing = ref(false)
const sentimentScore = ref(55) // 整体市场情绪

// 今日重点关注事件
const todayEvents = computed(() => {
  const today = new Date()
  const hour = today.getHours()

  // 根据当前时间生成今日事件
  const events = [
    {
      id: 1,
      time: '20:30',
      title: '美国非农就业数据',
      importance: 3,
      impact: 'high',
      effect: '高波动预期'
    },
    {
      id: 2,
      time: '22:00',
      title: '美联储官员讲话',
      importance: 2,
      impact: 'medium',
      effect: '关注利率暗示'
    },
    {
      id: 3,
      time: '次日02:00',
      title: 'FOMC会议纪要',
      importance: 3,
      impact: 'high',
      effect: '政策方向指引'
    }
  ]

  return events.slice(0, 3)
})

// 宏观经济因素
const macroFactors = computed(() => [
  {
    name: '美联储利率政策',
    icon: '🏦',
    impact: 'neutral',
    effectLabel: '观望',
    description: '当前利率维持高位，市场预期年内降息1-2次，关注通胀数据和就业数据变化。'
  },
  {
    name: '美元指数',
    icon: '💵',
    impact: 'bearish',
    effectLabel: '利空',
    description: '美元指数持续走强至105附近，对风险资产形成压力，加密货币承压。'
  },
  {
    name: '全球流动性',
    icon: '💧',
    impact: 'neutral',
    effectLabel: '中性',
    description: '全球央行货币政策分化，流动性环境整体偏紧，风险偏好谨慎。'
  },
  {
    name: '监管动态',
    icon: '⚖️',
    impact: 'bullish',
    effectLabel: '利好',
    description: '香港批准加密ETF，亚洲市场开放进程加速，机构入场渠道拓宽。'
  }
])

// 市场概况诊断
const marketDiagnosis = computed(() => {
  const btcDominance = props.globalMetrics?.btcDominance || 52
  const totalVolume = props.globalMetrics?.totalVolume24h || 0
  const change = props.globalMetrics?.marketCapChangePercentage24h || 0

  let trendText = '市场整体震荡'
  if (change > 3) trendText = '市场强势上涨'
  else if (change > 0) trendText = '市场温和上涨'
  else if (change < -3) trendText = '市场大幅下跌'
  else if (change < 0) trendText = '市场小幅回调'

  const dominanceText = btcDominance > 55 ? 'BTC主导地位较强，资金避险情绪明显' :
                        btcDominance < 50 ? '山寨币活跃度提升，市场风险偏好增强' :
                        'BTC与山寨币资金相对均衡'

  return `${trendText}，24h涨跌${change >= 0 ? '+' : ''}${change.toFixed(2)}%。BTC主导率${btcDominance.toFixed(1)}%，${dominanceText}。24h总交易量$${(totalVolume / 1e9).toFixed(2)}B，${totalVolume > 100e9 ? '市场活跃度较高' : '市场活跃度一般'}。建议关注今日宏观经济数据发布，控制仓位风险。`
})

// 突发事件
const breakingEvents = computed(() => {
  // 可以从后端API获取实时突发事件
  return [
    {
      id: 1,
      icon: '🔥',
      title: '美国非农数据即将发布',
      time: '今晚20:30',
      severity: 'high',
      impact: '就业数据将影响美联储利率决策预期，市场波动性可能显著增加。',
      marketEffect: 'volatile',
      effectDescription: '预期高波动'
    }
  ]
})

// 操作建议
const suggestions = computed(() => {
  const change = props.globalMetrics?.marketCapChangePercentage24h || 0
  const result = []

  result.push({ icon: '📅', text: '今日非农数据发布，建议提前调整仓位' })
  result.push({ icon: '🛡️', text: '设置好止损止盈，防范突发波动风险' })

  if (change > 2) {
    result.push({ icon: '⚠️', text: '短期涨幅较大，注意获利了结机会' })
  } else if (change < -2) {
    result.push({ icon: '💡', text: '市场回调中，关注优质资产布局机会' })
  } else {
    result.push({ icon: '⏳', text: '震荡行情，建议观望等待方向明确' })
  }

  result.push({ icon: '📊', text: '关注美联储官员讲话中的政策暗示' })

  return result
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
  await new Promise(r => setTimeout(r, 1500))
  // 可以在这里调用后端API获取最新的宏观分析数据
  isAnalyzing.value = false
}
</script>

<style scoped>
.market-ai-analysis {
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

/* 情绪仪表 */
.sentiment-section {
  margin-bottom: 12px;
}

.sentiment-gauge {
  margin-bottom: 8px;
}

.gauge-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-size: 12px;
  color: #7d8590;
}

.gauge-label .greed, .gauge-label .extreme-greed { color: #3fb950; }
.gauge-label .neutral { color: #7d8590; }
.gauge-label .fear, .gauge-label .extreme-fear { color: #f85149; }

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

/* 今日重点关注 */
.focus-section {
  margin-bottom: 12px;
}

.focus-section h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 6px 0;
}

.event-cards {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.event-card {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  background: #0d1117;
  border-radius: 6px;
  border-left: 3px solid #7d8590;
}

.event-card.high {
  border-left-color: #f85149;
  background: rgba(248, 81, 73, 0.05);
}

.event-card.medium {
  border-left-color: #f0b90b;
}

.event-time {
  font-size: 11px;
  font-weight: 600;
  color: #f0b90b;
  min-width: 45px;
}

.event-title {
  flex: 1;
  font-size: 11px;
  color: #e6edf3;
}

.event-importance {
  color: #f0b90b;
  font-size: 10px;
}

.event-effect {
  font-size: 10px;
  color: #7d8590;
  padding: 2px 6px;
  background: #21262d;
  border-radius: 3px;
}

/* 宏观经济 */
.macro-section {
  margin-bottom: 12px;
}

.macro-section h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 6px 0;
}

.macro-factors {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.factor-item {
  padding: 8px;
  background: #0d1117;
  border-radius: 6px;
  border-left: 2px solid #7d8590;
}

.factor-item.bullish { border-left-color: #3fb950; }
.factor-item.bearish { border-left-color: #f85149; }
.factor-item.neutral { border-left-color: #7d8590; }

.factor-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.factor-icon { font-size: 12px; }
.factor-name { font-size: 11px; font-weight: 500; color: #e6edf3; flex: 1; }

.factor-effect {
  font-size: 9px;
  padding: 2px 6px;
  border-radius: 3px;
}

.factor-effect.bullish { background: rgba(63, 185, 80, 0.2); color: #3fb950; }
.factor-effect.bearish { background: rgba(248, 81, 73, 0.2); color: #f85149; }
.factor-effect.neutral { background: rgba(125, 133, 144, 0.2); color: #7d8590; }

.factor-desc { font-size: 10px; color: #7d8590; line-height: 1.4; margin: 0; }

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

/* 突发事件 */
.breaking-section {
  margin-bottom: 12px;
}

.breaking-section h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 6px 0;
}

.no-events {
  padding: 12px;
  text-align: center;
  color: #7d8590;
  font-size: 11px;
  background: #0d1117;
  border-radius: 6px;
}

.breaking-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.breaking-item {
  padding: 8px;
  background: #0d1117;
  border-radius: 6px;
  border-left: 2px solid #f0b90b;
}

.breaking-item.high {
  border-left-color: #f85149;
  background: rgba(248, 81, 73, 0.05);
}

.breaking-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.breaking-icon { font-size: 12px; }
.breaking-title { font-size: 11px; font-weight: 500; color: #e6edf3; flex: 1; }
.breaking-time { font-size: 9px; color: #7d8590; padding: 2px 6px; background: #21262d; border-radius: 3px; }

.breaking-impact {
  font-size: 10px;
  color: #7d8590;
  line-height: 1.4;
  margin: 0 0 6px 0;
}

.breaking-effect {
  font-size: 10px;
  display: flex;
  gap: 4px;
}

.breaking-effect .label { color: #484f58; }
.breaking-effect .effect-value { font-weight: 500; }
.breaking-effect .effect-value.volatile { color: #f0b90b; }
.breaking-effect .effect-value.bullish { color: #3fb950; }
.breaking-effect .effect-value.bearish { color: #f85149; }

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

.suggestion-icon { font-size: 12px; }

.disclaimer {
  margin-top: auto;
  padding-top: 8px;
  font-size: 10px;
  color: #484f58;
  text-align: center;
  border-top: 1px solid #21262d;
}
</style>