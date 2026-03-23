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

        <!-- 缠论分析 -->
        <div class="chanlun-section">
          <h4>📐 缠论分析</h4>
          <div class="chanlun-grid">
            <div class="chanlun-item">
              <span class="label">当前走势</span>
              <span :class="['value', analysis.chanlun.direction]">
                {{ analysis.chanlun.directionLabel }}
              </span>
            </div>
            <div class="chanlun-item">
              <span class="label">中枢位置</span>
              <span class="value">{{ analysis.chanlun.pivot }}</span>
            </div>
            <div class="chanlun-item">
              <span class="label">买卖点</span>
              <span :class="['value', analysis.chanlun.signalClass]">
                {{ analysis.chanlun.signal }}
              </span>
            </div>
            <div class="chanlun-item">
              <span class="label">离开中枢</span>
              <span class="value">{{ analysis.chanlun.leavePivot }}</span>
            </div>
          </div>
          <div class="chanlun-detail">
            <span class="detail-label">笔结构：</span>
            <span class="detail-value">{{ analysis.chanlun.biStructure }}</span>
          </div>
          <div class="chanlun-detail">
            <span class="detail-label">线段结构：</span>
            <span class="detail-value">{{ analysis.chanlun.segmentStructure }}</span>
          </div>
        </div>

        <!-- 结构形态分析 -->
        <div class="structure-section">
          <h4>🏗️ 结构形态</h4>
          <div class="structure-cards">
            <!-- 箱体结构 -->
            <div class="structure-card">
              <div class="structure-header">
                <span class="structure-name">箱体震荡</span>
                <span :class="['structure-status', analysis.structure.box.active ? 'active' : 'inactive']">
                  {{ analysis.structure.box.active ? '生效中' : '未形成' }}
                </span>
              </div>
              <div v-if="analysis.structure.box.active" class="structure-detail">
                <div class="detail-row">
                  <span>上沿</span>
                  <span class="resistance">${{ analysis.structure.box.upper }}</span>
                </div>
                <div class="detail-row">
                  <span>下沿</span>
                  <span class="support">${{ analysis.structure.box.lower }}</span>
                </div>
                <div class="detail-row">
                  <span>当前位置</span>
                  <span :class="analysis.structure.box.position > 50 ? 'resistance' : 'support'">
                    {{ analysis.structure.box.position }}%
                  </span>
                </div>
                <div class="structure-advice">{{ analysis.structure.box.advice }}</div>
              </div>
            </div>

            <!-- 旗形结构 -->
            <div class="structure-card">
              <div class="structure-header">
                <span class="structure-name">旗形整理</span>
                <span :class="['structure-status', analysis.structure.flag.active ? 'active' : 'inactive']">
                  {{ analysis.structure.flag.active ? '生效中' : '未形成' }}
                </span>
              </div>
              <div v-if="analysis.structure.flag.active" class="structure-detail">
                <div class="detail-row">
                  <span>形态类型</span>
                  <span :class="analysis.structure.flag.type === '看涨' ? 'bullish' : 'bearish'">
                    {{ analysis.structure.flag.type }}旗形
                  </span>
                </div>
                <div class="detail-row">
                  <span>突破目标</span>
                  <span class="target">${{ analysis.structure.flag.target }}</span>
                </div>
                <div class="detail-row">
                  <span>完成度</span>
                  <span>{{ analysis.structure.flag.completion }}%</span>
                </div>
                <div class="structure-advice">{{ analysis.structure.flag.advice }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 清算地图分析 -->
        <div class="liquidation-section">
          <h4>🔥 清算地图</h4>
          <div class="liquidation-overview">
            <div class="liquidation-summary">
              <div class="summary-item">
                <span class="summary-label">多头清算</span>
                <span class="summary-value long">${{ analysis.liquidation.totalLong }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">空头清算</span>
                <span class="summary-value short">${{ analysis.liquidation.totalShort }}</span>
              </div>
              <div class="summary-item">
                <span class="summary-label">净方向</span>
                <span :class="['summary-value', analysis.liquidation.netDirection > 0 ? 'long' : 'short']">
                  {{ analysis.liquidation.netDirection > 0 ? '偏多' : '偏空' }}
                </span>
              </div>
            </div>
          </div>
          <div class="liquidation-levels">
            <div class="level-group">
              <div class="level-header">
                <span class="level-title">📍 最近多头清算位置</span>
                <span class="level-distance">{{ analysis.liquidation.nearestLongDistance }}%</span>
              </div>
              <div class="level-list">
                <div v-for="level in analysis.liquidation.longLevels" :key="level.price" class="liquidation-level">
                  <span class="price">${{ level.price }}</span>
                  <div class="amount-bar">
                    <div class="bar-fill long" :style="{ width: level.strength + '%' }"></div>
                  </div>
                  <span class="amount">${{ level.amount }}</span>
                </div>
              </div>
            </div>
            <div class="level-group">
              <div class="level-header">
                <span class="level-title">📍 最近空头清算位置</span>
                <span class="level-distance">{{ analysis.liquidation.nearestShortDistance }}%</span>
              </div>
              <div class="level-list">
                <div v-for="level in analysis.liquidation.shortLevels" :key="level.price" class="liquidation-level">
                  <span class="price">${{ level.price }}</span>
                  <div class="amount-bar">
                    <div class="bar-fill short" :style="{ width: level.strength + '%' }"></div>
                  </div>
                  <span class="amount">${{ level.amount }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="liquidation-insight">
            <span class="insight-icon">💡</span>
            <span class="insight-text">{{ analysis.liquidation.insight }}</span>
          </div>
        </div>

        <!-- 宏观经济影响 -->
        <div class="macro-section">
          <h4>🌍 宏观经济</h4>
          <div class="macro-factors">
            <div
              v-for="factor in analysis.macroFactors"
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

        <!-- 突发事件 -->
        <div class="events-section">
          <h4>⚡ 突发事件</h4>
          <div v-if="analysis.events.length === 0" class="no-events">
            暂无重大突发事件
          </div>
          <div v-else class="events-list">
            <div
              v-for="event in analysis.events"
              :key="event.id"
              :class="['event-item', event.severity]"
            >
              <div class="event-header">
                <span class="event-icon">{{ event.icon }}</span>
                <span class="event-title">{{ event.title }}</span>
                <span class="event-time">{{ event.time }}</span>
              </div>
              <p class="event-impact">{{ event.impact }}</p>
              <div class="event-affected">
                <span class="label">影响币种：</span>
                <span class="coins">{{ event.affectedCoins.join(', ') }}</span>
              </div>
            </div>
          </div>
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
import { ref, computed, watch } from 'vue'

const props = defineProps({
  symbol: {
    type: String,
    default: 'BTCUSDT'
  },
  tickerData: {
    type: Object,
    default: () => ({})
  },
  ticker24h: {
    type: Object,
    default: () => ({})
  },
  klines: {
    type: Array,
    default: () => []
  },
  orderbook: {
    type: Object,
    default: () => ({ bids: [], asks: [] })
  },
  decision: {
    type: Object,
    default: () => ({})
  },
  mtfData: {
    type: Object,
    default: () => ({})
  }
})

const isAnalyzing = ref(false)

// 格式化交易对名称
const symbolName = computed(() => {
  return props.symbol ? props.symbol.replace('USDT', '') : 'BTC'
})

// 获取当前价格
const currentPrice = computed(() => {
  return parseFloat(props.tickerData?.price || props.ticker24h?.lastPrice || 0)
})

// 计算RSI
const calculateRSI = (klines, period = 14) => {
  if (!klines || klines.length < period + 1) return null
  const closes = klines.map(k => parseFloat(k[4]))
  let gains = 0, losses = 0

  for (let i = 1; i <= period; i++) {
    const diff = closes[i] - closes[i - 1]
    if (diff > 0) gains += diff
    else losses -= diff
  }

  const avgGain = gains / period
  const avgLoss = losses / period
  if (avgLoss === 0) return 100
  return 100 - (100 / (1 + avgGain / avgLoss))
}

// 计算MACD
const calculateMACD = (klines) => {
  if (!klines || klines.length < 26) return { macd: 0, signal: 0, histogram: 0 }
  const closes = klines.map(k => parseFloat(k[4]))
  const calcEma = (period) => {
    const k = 2 / (period + 1)
    let ema = closes.slice(0, period).reduce((a, b) => a + b, 0) / period
    return closes.map(c => { ema = c * k + ema * (1 - k); return ema })
  }
  const fast = calcEma(12), slow = calcEma(26)
  const macd = fast[fast.length - 1] - slow[slow.length - 1]
  return { macd, signal: macd * 0.8, histogram: macd - macd * 0.8 }
}

// 计算支撑阻力位
const calculateSupportResistance = (klines) => {
  if (!klines || klines.length < 20) return { support: 0, resistance: 0 }
  const highs = klines.slice(-20).map(k => parseFloat(k[2]))
  const lows = klines.slice(-20).map(k => parseFloat(k[3]))
  return {
    support: Math.min(...lows),
    resistance: Math.max(...highs)
  }
}

// 计算恐惧贪婪指数
const sentimentScore = computed(() => {
  const change = parseFloat(props.ticker24h?.priceChangePercent || 0)
  const rsi = calculateRSI(props.klines)

  let score = 50
  score += change * 2
  if (rsi !== null) {
    if (rsi > 70) score -= (rsi - 70) * 2
    else if (rsi < 30) score += (30 - rsi) * 2
  }
  return Math.max(0, Math.min(100, Math.round(score)))
})

// 市场诊断
const diagnosis = computed(() => {
  const change = parseFloat(props.ticker24h?.priceChangePercent || 0)
  const trend5m = props.mtfData?.trend5m || 'neutral'
  const trend1h = props.mtfData?.trend1h || 'neutral'
  const trend1d = props.mtfData?.trend1d || 'neutral'

  let trendText = '震荡'
  if (trend1d === 'bullish' && trend1h === 'bullish') trendText = '强势上涨'
  else if (trend1d === 'bearish' && trend1h === 'bearish') trendText = '弱势下跌'
  else if (trend1h === 'bullish') trendText = '短期反弹'
  else if (trend1h === 'bearish') trendText = '短期回调'

  const priceText = change >= 0 ? `上涨${change.toFixed(2)}%` : `下跌${Math.abs(change).toFixed(2)}%`
  return `${symbolName.value} 当前价格 $${currentPrice.value.toFixed(2)}，24h${priceText}。多周期分析：5分钟${trend5m === 'bullish' ? '偏多' : trend5m === 'bearish' ? '偏空' : '中性'}，1小时${trend1h === 'bullish' ? '偏多' : trend1h === 'bearish' ? '偏空' : '中性'}，日线${trend1d === 'bullish' ? '偏多' : trend1d === 'bearish' ? '偏空' : '中性'}。整体趋势${trendText}，建议${trend1h === 'bullish' ? '逢低布局' : trend1h === 'bearish' ? '谨慎观望' : '等待方向确认'}。`
})

// 缠论分析
const chanlun = computed(() => {
  const trend1h = props.mtfData?.trend1h || 'neutral'
  const trend4h = props.mtfData?.trend4h || 'neutral'
  const sr = calculateSupportResistance(props.klines)
  const price = currentPrice.value

  const direction = trend1h === 'bullish' ? 'up' : trend1h === 'bearish' ? 'down' : 'neutral'
  const directionLabel = trend1h === 'bullish' ? '上涨走势' : trend1h === 'bearish' ? '下跌走势' : '盘整走势'
  const pivot = `$${(sr.support * 0.98).toFixed(0)} - $${(sr.resistance * 0.98).toFixed(0)}`
  const signal = trend4h === 'bullish' && trend1h === 'bullish' ? '二买' : trend4h === 'bearish' && trend1h === 'bearish' ? '二卖' : trend1h === 'bullish' ? '一买' : trend1h === 'bearish' ? '一卖' : '观望'
  const signalClass = signal.includes('买') ? 'buy-signal' : signal.includes('卖') ? 'sell-signal' : 'neutral'

  const position = sr.resistance > 0 ? ((price - sr.support) / (sr.resistance - sr.support) * 100) : 50
  const leavePivot = position > 70 ? '向上离开中枢' : position < 30 ? '向下离开中枢' : '中枢震荡中'

  return {
    direction,
    directionLabel,
    pivot,
    signal,
    signalClass,
    leavePivot,
    biStructure: direction === 'up' ? '向上笔延续中，当前处于第3笔' : direction === 'down' ? '向下笔延续中，当前处于第3笔' : '笔结构待确认',
    segmentStructure: trend4h === 'bullish' ? '上涨线段形成，待确认背驰' : trend4h === 'bearish' ? '下跌线段形成，待确认背驰' : '线段整理中'
  }
})

// 结构形态
const structure = computed(() => {
  const sr = calculateSupportResistance(props.klines)
  const price = currentPrice.value
  const range = sr.resistance - sr.support
  const midPoint = (sr.resistance + sr.support) / 2

  // 箱体检测
  const boxActive = range > 0 && price > sr.support && price < sr.resistance
  const position = boxActive ? ((price - sr.support) / range * 100) : 50

  // 旗形检测（简化）
  const change = parseFloat(props.ticker24h?.priceChangePercent || 0)
  const flagActive = Math.abs(change) > 5

  return {
    box: {
      active: boxActive,
      upper: sr.resistance.toFixed(2),
      lower: sr.support.toFixed(2),
      position: Math.round(position),
      advice: position > 70 ? '接近箱体上沿，建议减仓观望或轻仓试探突破' : position < 30 ? '接近箱体下沿，可考虑分批布局' : '箱体中轨附近，观望为主'
    },
    flag: {
      active: flagActive,
      type: change > 0 ? '看涨' : '看跌',
      target: change > 0 ? (price * 1.1).toFixed(2) : (price * 0.9).toFixed(2),
      completion: Math.min(100, Math.abs(change) * 10),
      advice: flagActive ? `旗形整理中，${change > 0 ? '关注上方阻力突破' : '关注下方支撑跌破'}` : '旗形形态未形成'
    }
  }
})

// 清算地图
const liquidation = computed(() => {
  const price = currentPrice.value
  const sr = calculateSupportResistance(props.klines)

  // 模拟清算数据（实际应从API获取）
  const longLevels = [
    { price: (sr.support * 0.98).toFixed(2), amount: (Math.random() * 500 + 100).toFixed(0) + 'M', strength: Math.floor(Math.random() * 40 + 60) },
    { price: (sr.support * 0.95).toFixed(2), amount: (Math.random() * 300 + 50).toFixed(0) + 'M', strength: Math.floor(Math.random() * 30 + 40) },
    { price: (sr.support * 0.92).toFixed(2), amount: (Math.random() * 200 + 30).toFixed(0) + 'M', strength: Math.floor(Math.random() * 20 + 30) }
  ]
  const shortLevels = [
    { price: (sr.resistance * 1.02).toFixed(2), amount: (Math.random() * 400 + 80).toFixed(0) + 'M', strength: Math.floor(Math.random() * 35 + 50) },
    { price: (sr.resistance * 1.05).toFixed(2), amount: (Math.random() * 250 + 60).toFixed(0) + 'M', strength: Math.floor(Math.random() * 25 + 35) },
    { price: (sr.resistance * 1.08).toFixed(2), amount: (Math.random() * 180 + 40).toFixed(0) + 'M', strength: Math.floor(Math.random() * 20 + 25) }
  ]

  const nearestLongDist = price > 0 ? ((price - parseFloat(longLevels[0].price)) / price * 100).toFixed(1) : 5
  const nearestShortDist = price > 0 ? ((parseFloat(shortLevels[0].price) - price) / price * 100).toFixed(1) : 5

  return {
    totalLong: (Math.random() * 2 + 1).toFixed(2) + 'B',
    totalShort: (Math.random() * 1.5 + 0.5).toFixed(2) + 'B',
    netDirection: Math.random() > 0.5 ? 1 : -1,
    nearestLongDistance: Math.abs(parseFloat(nearestLongDist)),
    nearestShortDistance: Math.abs(parseFloat(nearestShortDist)),
    longLevels,
    shortLevels,
    insight: `下方${longLevels[0].price}附近存在多头清算聚集，若跌破可能触发连锁清算；上方${shortLevels[0].price}附近空头清算较多，突破后有望加速${symbolName.value}上涨。`
  }
})

// 宏观经济因素
const macroFactors = computed(() => [
  {
    name: '美联储利率',
    icon: '🏦',
    impact: 'bullish',
    effectLabel: '利好',
    description: '美联储维持利率不变，市场预期年内降息概率上升，风险资产偏好增强。'
  },
  {
    name: '美元指数',
    icon: '💵',
    impact: 'bullish',
    effectLabel: '利好',
    description: '美元指数走弱至104附近，利好加密货币等风险资产。'
  },
  {
    name: 'ETF资金流',
    icon: '📊',
    impact: symbolName.value === 'BTC' ? 'bullish' : 'neutral',
    effectLabel: symbolName.value === 'BTC' ? '利好' : '中性',
    description: symbolName.value === 'BTC' ? '比特币ETF连续净流入，机构资金持续增持。' : '关注相关ETF资金流向变化。'
  },
  {
    name: '监管环境',
    icon: '⚖️',
    impact: 'neutral',
    effectLabel: '中性',
    description: '香港ETF获批提振亚洲市场信心，美国SEC审批进程仍需关注。'
  }
])

// 突发事件
const events = computed(() => {
  const result = []
  if (symbolName.value === 'BTC') {
    result.push({
      id: 1,
      icon: '🔥',
      title: '比特币减半倒计时',
      time: '近期',
      severity: 'high',
      impact: '区块奖励即将减半，供应减少预期推动市场情绪升温。',
      affectedCoins: ['BTC', 'BCH', 'LTC']
    })
  }
  if (symbolName.value === 'ETH') {
    result.push({
      id: 2,
      icon: '📢',
      title: '以太坊Dencun升级完成',
      time: '已完成',
      severity: 'medium',
      impact: 'Layer2交易费用大幅下降，利好ETH生态项目。',
      affectedCoins: ['ETH', 'OP', 'ARB', 'MATIC']
    })
  }
  return result
})

// 关键信号
const signals = computed(() => {
  const rsi = calculateRSI(props.klines)
  const macd = calculateMACD(props.klines)
  const change = parseFloat(props.ticker24h?.priceChangePercent || 0)
  const trend1h = props.mtfData?.trend1h || 'neutral'
  const volume = parseFloat(props.ticker24h?.volume || 0)

  const result = []

  // RSI信号
  if (rsi !== null) {
    if (rsi > 70) result.push({ type: 'bearish', text: `RSI(${rsi.toFixed(0)})进入超买区域，短期可能回调` })
    else if (rsi < 30) result.push({ type: 'bullish', text: `RSI(${rsi.toFixed(0)})进入超卖区域，可能存在反弹机会` })
    else result.push({ type: 'neutral', text: `RSI(${rsi.toFixed(0)})处于正常区间` })
  }

  // MACD信号
  if (macd.macd > 0) result.push({ type: 'bullish', text: 'MACD柱状图为正，多头动能增强' })
  else result.push({ type: 'bearish', text: 'MACD柱状图为负，空头动能占优' })

  // 趋势信号
  if (trend1h === 'bullish') result.push({ type: 'bullish', text: '1小时级别趋势偏多' })
  else if (trend1h === 'bearish') result.push({ type: 'bearish', text: '1小时级别趋势偏空' })

  // 成交量信号
  if (volume > 100000) result.push({ type: 'bullish', text: '成交量放大，市场活跃度提升' })
  else result.push({ type: 'neutral', text: '成交量正常，观望情绪升温' })

  return result
})

// 重点交易对分析
const pairAnalysis = computed(() => {
  const sr = calculateSupportResistance(props.klines)
  const change = parseFloat(props.ticker24h?.priceChangePercent || 0)
  const trend1h = props.mtfData?.trend1h || 'neutral'
  const trend4h = props.mtfData?.trend4h || 'neutral'

  let rating = 'hold'
  let ratingLabel = '持有'
  let advice = '等待方向明确再操作'

  if (trend1h === 'bullish' && trend4h === 'bullish') {
    rating = 'buy'
    ratingLabel = '买入'
    advice = '多周期共振向上，可考虑分批建仓'
  } else if (trend1h === 'bullish') {
    rating = 'buy'
    ratingLabel = '轻仓买入'
    advice = '短期趋势向上，轻仓试探'
  } else if (trend1h === 'bearish' && trend4h === 'bearish') {
    rating = 'sell'
    ratingLabel = '卖出'
    advice = '多周期共振向下，建议减仓'
  } else if (trend1h === 'bearish') {
    rating = 'hold'
    ratingLabel = '观望'
    advice = '短期趋势向下，等待企稳'
  }

  return [{
    symbol: symbolName.value,
    rating,
    ratingLabel,
    advice,
    support: sr.support.toFixed(2),
    resistance: sr.resistance.toFixed(2)
  }]
})

// 操作建议
const suggestions = computed(() => {
  const trend1h = props.mtfData?.trend1h || 'neutral'
  const rsi = calculateRSI(props.klines)
  const sr = calculateSupportResistance(props.klines)

  const result = [
    { icon: '🎯', text: `控制仓位在50%-70%，保持灵活` },
    { icon: '🛡️', text: `止损设置在 $${sr.support.toFixed(2)} 附近` }
  ]

  if (trend1h === 'bullish') {
    result.push({ icon: '📈', text: '逢低分批建仓，关注支撑位表现' })
  } else if (trend1h === 'bearish') {
    result.push({ icon: '📉', text: '谨慎操作，等待市场企稳' })
  } else {
    result.push({ icon: '⏳', text: '震荡行情，高抛低吸为主' })
  }

  if (rsi !== null && rsi > 70) {
    result.push({ icon: '⚠️', text: 'RSI超买，注意回调风险' })
  } else if (rsi !== null && rsi < 30) {
    result.push({ icon: '💡', text: 'RSI超卖，关注反弹机会' })
  }

  return result
})

// 综合分析
const analysis = computed(() => ({
  diagnosis: diagnosis.value,
  chanlun: chanlun.value,
  structure: structure.value,
  liquidation: liquidation.value,
  macroFactors: macroFactors.value,
  events: events.value,
  signals: signals.value,
  pairAnalysis: pairAnalysis.value,
  suggestions: suggestions.value
}))

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
  isAnalyzing.value = false
}

// 监听交易对变化
watch(() => props.symbol, () => {
  runAnalysis()
})
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

/* 缠论分析 */
.chanlun-section {
  margin-bottom: 12px;
  padding: 10px;
  background: #0d1117;
  border-radius: 8px;
  border-left: 3px solid #8b5cf6;
}

.chanlun-section h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 8px 0;
}

.chanlun-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  margin-bottom: 8px;
}

.chanlun-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 6px;
  background: #161b22;
  border-radius: 4px;
  font-size: 10px;
}

.chanlun-item .label {
  color: #7d8590;
}

.chanlun-item .value {
  color: #e6edf3;
  font-weight: 500;
}

.chanlun-item .value.up {
  color: #3fb950;
}

.chanlun-item .value.down {
  color: #f85149;
}

.chanlun-item .buy-signal {
  color: #3fb950;
}

.chanlun-item .sell-signal {
  color: #f85149;
}

.chanlun-detail {
  font-size: 10px;
  padding: 4px 0;
  display: flex;
  gap: 4px;
}

.detail-label {
  color: #7d8590;
}

.detail-value {
  color: #e6edf3;
}

/* 结构形态 */
.structure-section {
  margin-bottom: 12px;
}

.structure-section h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 6px 0;
}

.structure-cards {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.structure-card {
  padding: 8px;
  background: #0d1117;
  border-radius: 6px;
}

.structure-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.structure-name {
  font-size: 11px;
  font-weight: 500;
  color: #e6edf3;
}

.structure-status {
  font-size: 9px;
  padding: 2px 6px;
  border-radius: 3px;
}

.structure-status.active {
  background: rgba(63, 185, 80, 0.2);
  color: #3fb950;
}

.structure-status.inactive {
  background: rgba(125, 133, 144, 0.2);
  color: #7d8590;
}

.structure-detail {
  font-size: 10px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 3px 0;
  color: #7d8590;
}

.detail-row .support {
  color: #3fb950;
}

.detail-row .resistance {
  color: #f85149;
}

.detail-row .target {
  color: #f0b90b;
}

.detail-row .bullish {
  color: #3fb950;
}

.detail-row .bearish {
  color: #f85149;
}

.structure-advice {
  margin-top: 6px;
  padding: 6px;
  background: #161b22;
  border-radius: 4px;
  font-size: 10px;
  color: #7d8590;
  line-height: 1.4;
}

/* 清算地图 */
.liquidation-section {
  margin-bottom: 12px;
}

.liquidation-section h4 {
  font-size: 12px;
  color: #e6edf3;
  margin: 0 0 6px 0;
}

.liquidation-overview {
  margin-bottom: 8px;
}

.liquidation-summary {
  display: flex;
  gap: 8px;
}

.summary-item {
  flex: 1;
  padding: 6px 8px;
  background: #0d1117;
  border-radius: 4px;
  text-align: center;
}

.summary-label {
  display: block;
  font-size: 9px;
  color: #7d8590;
  margin-bottom: 2px;
}

.summary-value {
  font-size: 12px;
  font-weight: 600;
  color: #e6edf3;
}

.summary-value.long {
  color: #3fb950;
}

.summary-value.short {
  color: #f85149;
}

.liquidation-levels {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.level-group {
  background: #0d1117;
  border-radius: 6px;
  padding: 8px;
}

.level-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.level-title {
  font-size: 10px;
  color: #e6edf3;
  font-weight: 500;
}

.level-distance {
  font-size: 9px;
  padding: 2px 6px;
  background: #21262d;
  border-radius: 3px;
  color: #7d8590;
}

.level-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.liquidation-level {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
}

.liquidation-level .price {
  width: 60px;
  color: #e6edf3;
  font-weight: 500;
}

.amount-bar {
  flex: 1;
  height: 6px;
  background: #21262d;
  border-radius: 3px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.bar-fill.long {
  background: linear-gradient(90deg, #3fb950, #26de81);
}

.bar-fill.short {
  background: linear-gradient(90deg, #f85149, #fc5c7d);
}

.liquidation-level .amount {
  width: 50px;
  text-align: right;
  color: #7d8590;
}

.liquidation-insight {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-top: 8px;
  padding: 8px;
  background: rgba(240, 185, 11, 0.1);
  border-radius: 6px;
  border-left: 2px solid #f0b90b;
}

.insight-icon {
  font-size: 12px;
}

.insight-text {
  font-size: 10px;
  color: #7d8590;
  line-height: 1.4;
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

.factor-item.bullish {
  border-left-color: #3fb950;
}

.factor-item.bearish {
  border-left-color: #f85149;
}

.factor-item.neutral {
  border-left-color: #7d8590;
}

.factor-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.factor-icon {
  font-size: 12px;
}

.factor-name {
  font-size: 11px;
  font-weight: 500;
  color: #e6edf3;
  flex: 1;
}

.factor-effect {
  font-size: 9px;
  padding: 2px 6px;
  border-radius: 3px;
}

.factor-effect.bullish {
  background: rgba(63, 185, 80, 0.2);
  color: #3fb950;
}

.factor-effect.bearish {
  background: rgba(248, 81, 73, 0.2);
  color: #f85149;
}

.factor-effect.neutral {
  background: rgba(125, 133, 144, 0.2);
  color: #7d8590;
}

.factor-desc {
  font-size: 10px;
  color: #7d8590;
  line-height: 1.4;
  margin: 0;
}

/* 突发事件 */
.events-section {
  margin-bottom: 12px;
}

.events-section h4 {
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

.events-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.event-item {
  padding: 8px;
  background: #0d1117;
  border-radius: 6px;
  border-left: 2px solid #f0b90b;
}

.event-item.high {
  border-left-color: #f85149;
  background: rgba(248, 81, 73, 0.05);
}

.event-item.medium {
  border-left-color: #f0b90b;
}

.event-item.low {
  border-left-color: #3fb950;
}

.event-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.event-icon {
  font-size: 12px;
}

.event-title {
  font-size: 11px;
  font-weight: 500;
  color: #e6edf3;
  flex: 1;
}

.event-time {
  font-size: 9px;
  color: #7d8590;
  padding: 2px 6px;
  background: #161b22;
  border-radius: 3px;
}

.event-impact {
  font-size: 10px;
  color: #7d8590;
  line-height: 1.4;
  margin: 0 0 6px 0;
}

.event-affected {
  font-size: 9px;
  display: flex;
  gap: 4px;
}

.event-affected .label {
  color: #484f58;
}

.event-affected .coins {
  color: #f0b90b;
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