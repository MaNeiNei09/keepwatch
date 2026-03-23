// 技术指标计算逻辑
import { ref, computed } from 'vue'

// 指标参数
const selectedIndicators = ref([])
const selectedInterval = ref('1m')
const selectedParams = ref([12, 26])
const bollingerPeriod = ref(20)
const bollingerStdDev = ref(2)
const rsiPeriod = ref(14)
const atrMultiplier = ref(3.5)

// EMA/MA 参数选项
const emaParams = [7, 12, 25, 26, 50, 99, 144, 169, 200, 230]
const maParams = [7, 10, 20, 30, 60, 99, 120, 200]

// EMA/MA 颜色配置
const paramColors = {
  7: '#e74c3c',
  10: '#3498db',
  12: '#9b59b6',
  20: '#f0b90b',
  25: '#1abc9c',
  26: '#e67e22',
  30: '#95a5a6',
  50: '#2ecc71',
  60: '#34495e',
  99: '#16a085',
  120: '#8e44ad',
  144: '#f39c12',
  169: '#d35400',
  200: '#27ae60',
  230: '#c0392b'
}

// 时间周期配置
const intervals = [
  { label: '1m', value: '1m', desc: '1分钟' },
  { label: '5m', value: '5m', desc: '5分钟' },
  { label: '15m', value: '15m', desc: '15分钟' },
  { label: '1H', value: '1h', desc: '1小时' },
  { label: '4H', value: '4h', desc: '4小时' },
  { label: '1D', value: '1d', desc: '1天' }
]

// 计算MA
const calculateMA = (klines, period) => {
  const closes = klines.map(k => parseFloat(k[4]))
  const result = []
  for (let i = 0; i < closes.length; i++) {
    if (i < period - 1) {
      result.push({ time: klines[i][0] / 1000, value: null })
      continue
    }
    const sum = closes.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0)
    const ma = sum / period
    result.push({ time: klines[i][0] / 1000, value: ma })
  }
  return result
}

// 计算EMA
const calculateEMA = (klines, period) => {
  const closes = klines.map(k => parseFloat(k[4]))
  const k = 2 / (period + 1)
  let ema = closes.slice(0, period).reduce((a, b) => a + b, 0) / period
  const result = []

  for (let i = 0; i < closes.length; i++) {
    if (i < period - 1) {
      result.push({ time: klines[i][0] / 1000, value: null })
      continue
    }
    if (i === period - 1) {
      result.push({ time: klines[i][0] / 1000, value: ema })
    } else {
      ema = closes[i] * k + ema * (1 - k)
      result.push({ time: klines[i][0] / 1000, value: ema })
    }
  }
  return result
}

// 计算RSI
const calculateRSI = (klines, period = 14) => {
  const closes = klines.map(k => parseFloat(k[4]))
  const result = []
  let gains = 0
  let losses = 0

  for (let i = 1; i < closes.length; i++) {
    const change = closes[i] - closes[i - 1]

    if (i <= period) {
      if (change > 0) gains += change
      else losses -= change

      if (i === period) {
        const avgGain = gains / period
        const avgLoss = losses / period
        const rs = avgGain / (avgLoss || 1)
        const rsi = 100 - (100 / (1 + rs))
        result.push({ time: klines[i][0] / 1000, value: rsi })
      } else {
        result.push({ time: klines[i][0] / 1000, value: null })
      }
    } else {
      const avgGain = (gains / period)
      const avgLoss = (losses / period)
      const currentGain = change > 0 ? change : 0
      const currentLoss = change < 0 ? -change : 0

      const newAvgGain = (avgGain * (period - 1) + currentGain) / period
      const newAvgLoss = (avgLoss * (period - 1) + currentLoss) / period

      gains = newAvgGain * period
      losses = newAvgLoss * period

      const rs = newAvgGain / (newAvgLoss || 1)
      const rsi = 100 - (100 / (1 + rs))
      result.push({ time: klines[i][0] / 1000, value: rsi })
    }
  }

  return result
}

// 计算MACD
const calculateMACD = (klines, fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) => {
  const closes = klines.map(k => parseFloat(k[4]))

  // 计算EMA
  const calculateEma = (period) => {
    const k = 2 / (period + 1)
    let ema = closes.slice(0, period).reduce((a, b) => a + b, 0) / period
    const result = []

    for (let i = 0; i < closes.length; i++) {
      if (i < period - 1) {
        result.push(null)
      } else if (i === period - 1) {
        result.push(ema)
      } else {
        ema = closes[i] * k + ema * (1 - k)
        result.push(ema)
      }
    }
    return result
  }

  const fastEMA = calculateEma(fastPeriod)
  const slowEMA = calculateEma(slowPeriod)

  const macdLine = closes.map((_, i) => {
    if (fastEMA[i] === null || slowEMA[i] === null) return null
    return fastEMA[i] - slowEMA[i]
  })

  // 计算Signal线
  const k = 2 / (signalPeriod + 1)
  let signal = macdLine.slice(slowPeriod, slowPeriod + signalPeriod).reduce((a, b) => a + b, 0) / signalPeriod
  const signalLine = []

  for (let i = 0; i < macdLine.length; i++) {
    if (i < slowPeriod + signalPeriod - 1) {
      signalLine.push(null)
    } else if (i === slowPeriod + signalPeriod - 1) {
      signalLine.push(signal)
    } else {
      if (macdLine[i] !== null) {
        signal = macdLine[i] * k + signal * (1 - k)
        signalLine.push(signal)
      } else {
        signalLine.push(null)
      }
    }
  }

  const histogram = macdLine.map((macd, i) => {
    if (macd === null || signalLine[i] === null) return null
    return macd - signalLine[i]
  })

  return { macdLine, signalLine, histogram }
}

// 计算布林带
const calculateBollingerBands = (klines, period = 20, stdDev = 2) => {
  const closes = klines.map(k => parseFloat(k[4]))
  const result = { upper: [], middle: [], lower: [] }

  for (let i = 0; i < closes.length; i++) {
    if (i < period - 1) {
      result.upper.push({ time: klines[i][0] / 1000, value: null })
      result.middle.push({ time: klines[i][0] / 1000, value: null })
      result.lower.push({ time: klines[i][0] / 1000, value: null })
      continue
  }

    const slice = closes.slice(i - period + 1, i + 1)
    const sma = slice.reduce((a, b) => a + b, 0) / period

    const variance = slice.reduce((sum, val) => sum + Math.pow(val - sma, 2), 0) / period
    const std = Math.sqrt(variance)

    const time = klines[i][0] / 1000
    result.upper.push({ time, value: sma + stdDev * std })
    result.middle.push({ time, value: sma })
    result.lower.push({ time, value: sma - stdDev * std })
  }

  return result
}

// 计算ATR
const calculateATR = (klines, period = 14) => {
  const result = []

  for (let i = 0; i < klines.length; i++) {
    const high = parseFloat(klines[i][2])
    const low = parseFloat(klines[i][3])
    const close = parseFloat(klines[i][4])

    if (i === 0) {
      result.push({ time: klines[i][0] / 1000, value: high - low })
      continue
    }

    const prevClose = parseFloat(klines[i - 1][4])
    const tr = Math.max(
      high - low,
      Math.abs(high - prevClose),
      Math.abs(low - prevClose)
    )

    if (i < period) {
      const sum = result.slice(0).reduce((s, r) => s + r.value, 0) + tr
      const avg = sum / (i + 1)
      result.push({ time: klines[i][0] / 1000, value: avg })
    } else {
      const prevATR = result[i - 1].value
      const atr = (prevATR * (period - 1) + tr) / period
      result.push({ time: klines[i][0] / 1000, value: atr })
    }
  }

  return result
}

export function useIndicators() {
  return {
    // 参数
    selectedIndicators,
    selectedInterval,
    selectedParams,
    bollingerPeriod,
    bollingerStdDev,
    rsiPeriod,
    atrMultiplier,

    // 常量
    emaParams,
    maParams,
    paramColors,
    intervals,

    // 计算函数
    calculateMA,
    calculateEMA,
    calculateRSI,
    calculateMACD,
    calculateBollingerBands,
    calculateATR
  }
}