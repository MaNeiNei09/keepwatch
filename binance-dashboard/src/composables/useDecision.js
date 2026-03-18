// 智能决策逻辑
import { ref, computed } from 'vue'

// 决策配置
const config = ref({
  emaFast: 12,
  lookback: 50,
  volMult: 3.0,
  biasLimit: 1.5,
  atrPeriod: 14,
  atrMult: 2.2
})

// 多周期数据
const mtfData = ref({
  trend5m: false,
  trend15m: false,
  trend30m: false,
  trend1h: false,
  trend4h: false,
  trend1d: false
})

// 决策结果
const decision = ref({
  state: 0,           // 1: 多头, -1: 空头, 0: 震荡
  trendBars: 0,
  timeStr: '0分',
  stageLabel: '【震荡期】',
  stageClass: 'neutral',
  isDivergence: false,
  isVolSpike: false,
  isClimaxTop: false,
  isOverextended: false,
  biasRatio: '0.00',
  rigidStopLong: null,
  rigidStopShort: null,
  swingHigh: null,
  swingLow: null,
  adviceTitle: '博弈平衡区',
  adviceBody: '建议观望，等待明确信号',
  adviceIcon: '⚖️',
  action: '观望',
  actionClass: 'neutral'
})

// 趋势节点
const trendNodes = ref([])

// 计算决策
const calculateDecision = (klines, tickerData, ticker24h, atrMultiplier) => {
  if (!klines?.length) return

  const closes = klines.map(k => parseFloat(k[4]))
  const highs = klines.map(k => parseFloat(k[2]))
  const lows = klines.map(k => parseFloat(k[3]))
  const volumes = klines.map(k => parseFloat(k[5]))

  const currentPrice = parseFloat(tickerData?.price || 0)
  const latestClose = closes[closes.length - 1]
  const latestHigh = highs[highs.length - 1]
  const latestLow = lows[lows.length - 1]

  // 计算EMA
  const emaPeriod = config.value.emaFast
  const k = 2 / (emaPeriod + 1)
  let ema = closes.slice(0, emaPeriod).reduce((a, b) => a + b, 0) / emaPeriod
  for (let i = emaPeriod; i < closes.length; i++) {
    ema = closes[i] * k + ema * (1 - k)
  }

  // 计算ATR
  let atr = 0
  const atrPeriod = config.value.atrPeriod
  for (let i = klines.length - atrPeriod; i < klines.length; i++) {
    const tr = Math.max(
      highs[i] - lows[i],
      Math.abs(highs[i] - closes[i - 1]),
      Math.abs(lows[i] - closes[i - 1])
    )
    atr += tr
  }
  atr /= atrPeriod

  // 计算布林带
  const bbPeriod = 20
  const bbStd = 2
  const recentCloses = closes.slice(-bbPeriod)
  const sma = recentCloses.reduce((a, b) => a + b, 0) / bbPeriod
  const variance = recentCloses.reduce((sum, val) => sum + Math.pow(val - sma, 2), 0) / bbPeriod
  const std = Math.sqrt(variance)
  const upperBand = sma + bbStd * std
  const lowerBand = sma - bbStd * std

  // 计算成交量均值
  const volPeriod = 20
  const avgVol = volumes.slice(-volPeriod).reduce((a, b) => a + b, 0) / volPeriod
  const currentVol = volumes[volumes.length - 1]

  // 判断趋势
  let state = 0
  if (latestClose > ema && latestClose > upperBand) {
    state = 1
  } else if (latestClose < ema && latestClose < lowerBand) {
    state = -1
  }

  // 计算偏离度
  const bias = ((latestClose - ema) / ema * 100).toFixed(2)
  const isOverextended = Math.abs(parseFloat(bias)) > config.value.biasLimit

  // 计算趋势持续根数和时间
  let trendBars = 0
  for (let i = closes.length - 2; i >= 0; i--) {
    if (state === 1 && closes[i] > ema) trendBars++
    else if (state === -1 && closes[i] < ema) trendBars++
    else break
  }

  const minutes = trendBars
  let timeStr = ''
  if (minutes < 60) timeStr = `${minutes}分`
  else timeStr = `${Math.floor(minutes / 60)}小时${minutes % 60}分`

  // 判断阶段
  let stageLabel = '【震荡期】'
  let stageClass = 'neutral'
  if (state === 1) {
    if (trendBars < 10) {
      stageLabel = '【初升期】'
      stageClass = 'bullish'
    } else if (trendBars < 30) {
      stageLabel = '【爆发期】'
      stageClass = 'stable'
    } else {
      stageLabel = '【衰竭期】'
      stageClass = 'warning'
    }
  } else if (state === -1) {
    if (trendBars < 10) {
      stageLabel = '【初跌期】'
      stageClass = 'bearish'
    } else if (trendBars < 30) {
      stageLabel = '【恐慌期】'
      stageClass = 'danger'
    } else {
      stageLabel = '【吸筹期】'
      stageClass = 'stable'
    }
  }

  // 判断背驰
  const isDivergence = false
  // (简化判断逻辑)

  // 判断天量
  const isVolSpike = currentVol > avgVol * config.value.volMult

  // 判断出货
  const isClimaxTop = isVolSpike && state === 1 && currentPrice < latestHigh * 0.98

  // 计算止损
  const rigidStopLong = (currentPrice - atr * atrMultiplier).toFixed(2)
  const rigidStopShort = (currentPrice + atr * atrMultiplier).toFixed(2)

  // 计算高低点
  const swingHigh = latestHigh.toFixed(2)
  const swingLow = latestLow.toFixed(2)

  // 生成建议
  let adviceTitle, adviceBody, adviceIcon, action, actionClass

  if (state === 1 && !isOverextended && !isClimaxTop) {
    adviceTitle = '🟢 多头信号'
    adviceBody = `价格突破EMA均线，偏离度${bias}%，趋势持续${trendBars}根K线`
    adviceIcon = '🟢'
    action = '回调做多'
    actionClass = 'bullish'
  } else if (state === -1 && !isOverextended && !isClimaxTop) {
    adviceTitle = '🔴 空头信号'
    adviceBody = `价格跌破EMA均线，偏离度${bias}%，趋势持续${trendBars}根K线`
    adviceIcon = '🔴'
    action = '反弹做空'
    actionClass = 'bearish'
  } else if (isClimaxTop) {
    adviceTitle = '🚨 顶部出货'
    adviceBody = '出现天量滞涨信号，警惕回调风险'
    adviceIcon = '🚨'
    action = '止盈离场'
    actionClass = 'danger'
  } else if (isOverextended) {
    adviceTitle = '⚠️ 过度偏离'
    adviceBody = `价格偏离EMA ${bias}%，注意回调风险`
    adviceIcon = '⚠️'
    action = '谨慎追涨'
    actionClass = 'warning'
  } else {
    adviceTitle = '⚖️ 博弈平衡区'
    adviceBody = '建议观望，等待明确信号'
    adviceIcon = '⚖️'
    action = '观望'
    actionClass = 'neutral'
  }

  // 更新决策结果
  decision.value = {
    state,
    trendBars,
    timeStr,
    stageLabel,
    stageClass,
    isDivergence,
    isVolSpike,
    isClimaxTop,
    isOverextended,
    biasRatio: bias,
    rigidStopLong,
    rigidStopShort,
    swingHigh,
    swingLow,
    adviceTitle,
    adviceBody,
    adviceIcon,
    action,
    actionClass
  }
}

// 生成趋势节点
const generateTrendNodes = (klines) => {
  if (!klines?.length) return

  const closes = klines.map(k => parseFloat(k[4]))
  const emaPeriod = 60
  const k = 2 / (emaPeriod + 1)
  let ema = closes.slice(0, emaPeriod).reduce((a, b) => a + b, 0) / emaPeriod

  for (let i = emaPeriod; i < closes.length; i++) {
    ema = closes[i] * k + ema * (1 - k)
  }

  // 简化逻辑 - 只生成当前节点
  const currentPrice = closes[closes.length - 1]
  const direction = currentPrice > ema ? 'bullish' : 'bearish'

  trendNodes.value = [{
    direction,
    isCurrent: true,
    timeStr: new Date().toLocaleString('zh-CN'),
    duration: '进行中',
    changePercent: '0.00',
    entryPrice: ema.toFixed(2),
    currentPrice: currentPrice.toFixed(2),
    stageLabel: direction === 'bullish' ? '【初升期】' : '【初跌期】',
    stageClass: direction === 'bullish' ? 'bullish' : 'bearish'
  }]
}

export function useDecision() {
  return {
    // 配置和数据
    config,
    mtfData,
    decision,
    trendNodes,

    // 方法
    calculateDecision,
    generateTrendNodes
  }
}