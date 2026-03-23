<template>
  <div :class="['decision-card', adviceClass]">
    <div class="card-title">
      <span class="title-icon">{{ adviceIcon }}</span>
      <span>智能决策</span>
    </div>
    <div class="decision-content">
      <div class="decision-status">
        <span class="status-main">{{ adviceTitle }}</span>
        <span class="status-action">{{ action }}</span>
      </div>
      <div class="decision-metrics">
        <div class="decision-metric">
          <span class="dm-label">趋势</span>
          <span :class="['dm-value', state > 0 ? 'bullish' : (state < 0 ? 'bearish' : 'neutral')]">
            {{ state > 0 ? '上涨' : (state < 0 ? '下跌' : '震荡') }}
          </span>
        </div>
        <div class="decision-metric">
          <span class="dm-label">阶段</span>
          <span :class="['dm-value', stageClass]">{{ stageLabel }}</span>
        </div>
        <div class="decision-metric">
          <span class="dm-label">偏离</span>
          <span :class="['dm-value', isOverextended ? 'warning' : '']">{{ biasRatio }}%</span>
        </div>
        <div class="decision-metric">
          <span class="dm-label">根数/时间</span>
          <span class="dm-value">{{ trendBars }}根 / {{ timeStr }}</span>
        </div>
      </div>
      <div class="warning-flags">
        <span v-if="isDivergence" class="flag danger">⚠️ 背驰</span>
        <span v-if="isVolSpike" class="flag warning">⚠️ 天量</span>
        <span v-if="isClimaxTop" class="flag danger">🚨 出货</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  state: { type: Number, default: 0 },
  trendBars: { type: Number, default: 0 },
  timeStr: { type: String, default: '0分' },
  stageLabel: { type: String, default: '【震荡期】' },
  stageClass: { type: String, default: 'neutral' },
  isDivergence: { type: Boolean, default: false },
  isVolSpike: { type: Boolean, default: false },
  isClimaxTop: { type: Boolean, default: false },
  isOverextended: { type: Boolean, default: false },
  biasRatio: { type: String, default: '0.00' },
  adviceTitle: { type: String, default: '博弈平衡区' },
  adviceIcon: { type: String, default: '⚖️' },
  adviceClass: { type: String, default: 'neutral' },
  action: { type: String, default: '观望' },
  actionClass: { type: String, default: 'neutral' }
})
</script>

<style scoped>
.decision-card {
  background: linear-gradient(135deg, #1a1f2e 0%, #161b22 100%);
  border-radius: 12px;
  padding: 12px;
  border: 1px solid #21262d;
  display: flex;
  flex-direction: column;
}

.decision-card.neutral { border-color: #8b949e; }
.decision-card.bullish { border-color: #26de81; }
.decision-card.warning { border-color: #f39c12; }
.decision-card.danger { border-color: #e74c3c; }
.decision-card.stable { border-color: #3498db; }

.card-title {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #e6edf3;
}

.title-icon {
  font-size: 14px;
}

.decision-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.decision-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-main {
  font-size: 12px;
  font-weight: 600;
}

.decision-card.neutral .status-main { color: #8b949e; }
.decision-card.bullish .status-main { color: #26de81; }
.decision-card.warning .status-main { color: #f39c12; }
.decision-card.danger .status-main { color: #e74c3c; }
.decision-card.stable .status-main { color: #3498db; }

.status-action {
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
  background: rgba(255,255,255,0.1);
}

.decision-card.neutral .status-action { color: #8b949e; }
.decision-card.bullish .status-action { color: #26de81; }
.decision-card.warning .status-action { color: #f39c12; }
.decision-card.danger .status-action { color: #fc5c7d; }
.decision-card.stable .status-action { color: #3498db; }

.decision-metrics {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3px;
}

.decision-metric {
  text-align: center;
  padding: 3px;
  background: #0d1117;
  border-radius: 3px;
}

.dm-label {
  display: block;
  font-size: 8px;
  color: #8b949e;
}

.dm-value {
  font-size: 10px;
  font-weight: 600;
}

.dm-value.bullish { color: #26de81; }
.dm-value.bearish { color: #fc5c7d; }
.dm-value.neutral { color: #8b949e; }
.dm-value.warning { color: #f39c12; }
.dm-value.stable { color: #3498db; }

.warning-flags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.flag {
  font-size: 9px;
  padding: 2px 4px;
  border-radius: 3px;
}

.flag.danger {
  background: rgba(252, 92, 125, 0.2);
  color: #fc5c7d;
}

.flag.warning {
  background: rgba(243, 156, 18, 0.2);
  color: #f39c12;
}
</style>