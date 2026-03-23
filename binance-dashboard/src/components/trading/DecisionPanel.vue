<template>
  <div class="decision-panel">
    <div class="panel-title">
      <span class="title-icon">🎯</span>
      <span>三维共振决策建议</span>
    </div>

    <div class="decision-content">
      <!-- 综合评分 -->
      <div class="score-summary">
        <div class="score-item long">
          <span class="score-label">做多得分</span>
          <div class="score-bar">
            <div class="score-fill long" :style="{ width: (longScore / 12 * 100) + '%' }"></div>
          </div>
          <span class="score-value">{{ longScore }}/12</span>
        </div>
        <div class="score-item short">
          <span class="score-label">做空得分</span>
          <div class="score-bar">
            <div class="score-fill short" :style="{ width: (shortScore / 12 * 100) + '%' }"></div>
          </div>
          <span class="score-value">{{ shortScore }}/12</span>
        </div>
      </div>

      <!-- 决策建议 -->
      <div class="decision-advice" :class="decisionClass">
        <div class="advice-icon">{{ decisionIcon }}</div>
        <div class="advice-content">
          <div class="advice-title">{{ decisionTitle }}</div>
          <div class="advice-detail">{{ decisionDetail }}</div>
        </div>
      </div>

      <!-- 心法提醒 -->
      <div class="mindset-reminder">
        <div class="reminder-title">🧠 大师心法</div>
        <div class="reminder-items">
          <div class="reminder-item">
            <span class="reminder-icon">📌</span>
            <span class="reminder-text">三缺一无效：箱体+斐波那契+缠论背驰/分型，三者缺一不可</span>
          </div>
          <div class="reminder-item">
            <span class="reminder-icon">📌</span>
            <span class="reminder-text">宁可错过，不做错：市场不缺机会，缺的是本金</span>
          </div>
          <div class="reminder-item">
            <span class="reminder-icon">📌</span>
            <span class="reminder-text">突破不看幅度，看结构：无背驰不突破，有背驰必回归</span>
          </div>
        </div>
      </div>

      <!-- 执行纪律 -->
      <div class="execution-rules">
        <div class="rule-title">📋 执行纪律</div>
        <div class="rule-grid">
          <div class="rule-item" :class="{ active: longScore >= 8 }">
            <span class="rule-condition">做多得分 ≥ 8</span>
            <span class="rule-action">执行做多</span>
          </div>
          <div class="rule-item" :class="{ active: shortScore >= 8 }">
            <span class="rule-condition">做空得分 ≥ 8</span>
            <span class="rule-action">执行做空</span>
          </div>
          <div class="rule-item" :class="{ active: longScore >= 6 && shortScore < 5 }">
            <span class="rule-condition">做多≥6 且 做空<5</span>
            <span class="rule-action">轻仓做多</span>
          </div>
          <div class="rule-item" :class="{ active: shortScore >= 6 && longScore < 5 }">
            <span class="rule-condition">做空≥6 且 做多<5</span>
            <span class="rule-action">轻仓做空</span>
          </div>
          <div class="rule-item" :class="{ active: longScore < 5 && shortScore < 5 }">
            <span class="rule-condition">双向得分 < 5</span>
            <span class="rule-action">空仓观望</span>
          </div>
          <div class="rule-item" :class="{ active: Math.abs(longScore - shortScore) < 2 }">
            <span class="rule-condition">得分差距 < 2</span>
            <span class="rule-action">信号不明确</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  longScore: {
    type: Number,
    default: 0
  },
  shortScore: {
    type: Number,
    default: 0
  },
  analysisData: {
    type: Object,
    default: () => ({})
  },
  currentPrice: {
    type: Number,
    default: 0
  }
})

const decisionClass = computed(() => {
  if (props.longScore >= 8 && props.longScore > props.shortScore + 2) return 'strong-long'
  if (props.shortScore >= 8 && props.shortScore > props.longScore + 2) return 'strong-short'
  if (props.longScore >= 6 && props.longScore > props.shortScore) return 'weak-long'
  if (props.shortScore >= 6 && props.shortScore > props.longScore) return 'weak-short'
  return 'neutral'
})

const decisionIcon = computed(() => {
  const cls = decisionClass.value
  if (cls === 'strong-long') return '🚀'
  if (cls === 'strong-short') return '📉'
  if (cls === 'weak-long') return '📈'
  if (cls === 'weak-short') return '🔻'
  return '⏸️'
})

const decisionTitle = computed(() => {
  const cls = decisionClass.value
  if (cls === 'strong-long') return '强烈做多信号'
  if (cls === 'strong-short') return '强烈做空信号'
  if (cls === 'weak-long') return '谨慎做多信号'
  if (cls === 'weak-short') return '谨慎做空信号'
  return '建议观望等待'
})

const decisionDetail = computed(() => {
  const cls = decisionClass.value
  const box = props.analysisData.box
  const price = props.currentPrice

  if (cls === 'strong-long') {
    return `箱体下沿支撑确认，斐波那契黄金位共振，缠论底分型+背驰确认。当前价格 $${price.toFixed(2)} 接近理想入场点。建议入场，止损设在前低下方2%。`
  }
  if (cls === 'strong-short') {
    return `箱体上沿压力确认，斐波那契反弹位共振，缠论顶分型+背驰确认。当前价格 $${price.toFixed(2)} 接近理想入场点。建议入场，止损设在前高上方2%。`
  }
  if (cls === 'weak-long') {
    return `部分条件满足，但信号不够强烈。建议轻仓试探或等待更多确认信号。关注底分型和背驰的确认。`
  }
  if (cls === 'weak-short') {
    return `部分条件满足，但信号不够强烈。建议轻仓试探或等待更多确认信号。关注顶分型和背驰的确认。`
  }
  return `当前市场信号不明确，双向得分均较低或接近。建议空仓观望，等待更清晰的交易机会。耐心是交易者最好的武器。`
})
</script>

<style scoped>
.decision-panel {
  padding: 16px;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #21262d;
}

.title-icon {
  font-size: 18px;
}

.decision-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 评分汇总 */
.score-summary {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.score-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.score-label {
  width: 80px;
  font-size: 12px;
  color: #7d8590;
}

.score-bar {
  flex: 1;
  height: 8px;
  background: #21262d;
  border-radius: 4px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.score-fill.long {
  background: linear-gradient(90deg, #3fb950, #26de81);
}

.score-fill.short {
  background: linear-gradient(90deg, #f85149, #fc5c7d);
}

.score-value {
  width: 50px;
  text-align: right;
  font-size: 13px;
  font-weight: 600;
  color: #e6edf3;
  font-family: monospace;
}

/* 决策建议 */
.decision-advice {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  background: #0d1117;
}

.decision-advice.strong-long {
  border-left: 4px solid #3fb950;
  background: rgba(63, 185, 80, 0.1);
}

.decision-advice.strong-short {
  border-left: 4px solid #f85149;
  background: rgba(248, 81, 73, 0.1);
}

.decision-advice.weak-long {
  border-left: 4px solid #26de81;
  background: rgba(38, 222, 129, 0.05);
}

.decision-advice.weak-short {
  border-left: 4px solid #fc5c7d;
  background: rgba(252, 92, 125, 0.05);
}

.decision-advice.neutral {
  border-left: 4px solid #7d8590;
}

.advice-icon {
  font-size: 28px;
}

.advice-content {
  flex: 1;
}

.advice-title {
  font-size: 16px;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 6px;
}

.advice-detail {
  font-size: 12px;
  color: #7d8590;
  line-height: 1.6;
}

/* 心法提醒 */
.mindset-reminder {
  padding: 12px;
  background: rgba(240, 185, 11, 0.1);
  border-radius: 8px;
  border-left: 3px solid #f0b90b;
}

.reminder-title {
  font-size: 12px;
  font-weight: 600;
  color: #f0b90b;
  margin-bottom: 8px;
}

.reminder-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.reminder-item {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  font-size: 11px;
  color: #7d8590;
}

.reminder-icon {
  flex-shrink: 0;
}

/* 执行纪律 */
.execution-rules {
  padding: 12px;
  background: #0d1117;
  border-radius: 8px;
}

.rule-title {
  font-size: 12px;
  font-weight: 600;
  color: #e6edf3;
  margin-bottom: 10px;
}

.rule-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.rule-item {
  padding: 8px;
  background: #161b22;
  border-radius: 6px;
  border: 1px solid #21262d;
  text-align: center;
  transition: all 0.15s;
}

.rule-item.active {
  background: rgba(240, 185, 11, 0.15);
  border-color: #f0b90b;
}

.rule-condition {
  display: block;
  font-size: 10px;
  color: #7d8590;
  margin-bottom: 4px;
}

.rule-action {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #e6edf3;
}

.rule-item.active .rule-action {
  color: #f0b90b;
}

@media (max-width: 768px) {
  .rule-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>