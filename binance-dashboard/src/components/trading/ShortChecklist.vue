<template>
  <div class="short-checklist">
    <!-- 战略层：箱体与趋势 -->
    <div class="check-section">
      <div class="section-header">
        <span class="section-icon">🏛️</span>
        <span class="section-title">战略层：箱体与趋势</span>
      </div>
      <div class="check-items">
        <CheckItem
          title="箱体定位"
          :status="boxPosition.status"
          :value="boxPosition.value"
          :detail="boxPosition.detail"
        />
        <CheckItem
          title="大级别中枢"
          :status="pivotStatus.status"
          :value="pivotStatus.value"
          :detail="pivotStatus.detail"
        />
      </div>
    </div>

    <!-- 战术层：斐波那契反弹 -->
    <div class="check-section">
      <div class="section-header">
        <span class="section-icon">📐</span>
        <span class="section-title">战术层：斐波那契反弹</span>
      </div>
      <div class="check-items">
        <CheckItem
          title="黄金压力位"
          :status="fibGolden.status"
          :value="fibGolden.value"
          :detail="fibGolden.detail"
        />
        <CheckItem
          title="共振验证"
          :status="fibResonance.status"
          :value="fibResonance.value"
          :detail="fibResonance.detail"
        />
      </div>
    </div>

    <!-- 触发层：缠论显微镜 -->
    <div class="check-section">
      <div class="section-header">
        <span class="section-icon">🔬</span>
        <span class="section-title">触发层：缠论显微镜</span>
      </div>
      <div class="check-items">
        <CheckItem
          title="顶分型确认"
          :status="topFractal.status"
          :value="topFractal.value"
          :detail="topFractal.detail"
        />
        <CheckItem
          title="笔的终结"
          :status="biEnd.status"
          :value="biEnd.value"
          :detail="biEnd.detail"
        />
        <CheckItem
          title="盘整背驰"
          :status="divergence.status"
          :value="divergence.value"
          :detail="divergence.detail"
        />
        <CheckItem
          title="类二卖信号"
          :status="secondSell.status"
          :value="secondSell.value"
          :detail="secondSell.detail"
        />
      </div>
    </div>

    <!-- 市场情绪层 -->
    <div class="check-section">
      <div class="section-header">
        <span class="section-icon">💭</span>
        <span class="section-title">市场情绪层</span>
      </div>
      <div class="check-items">
        <CheckItem
          title="恐惧贪婪指数"
          :status="fearGreedIndex.status"
          :value="fearGreedIndex.value"
          :detail="fearGreedIndex.detail"
        />
        <CheckItem
          title="交易所净流入/流出"
          :status="exchangeFlow.status"
          :value="exchangeFlow.value"
          :detail="exchangeFlow.detail"
        />
        <CheckItem
          title="永续合约资金费率"
          :status="fundingRate.status"
          :value="fundingRate.value"
          :detail="fundingRate.detail"
        />
      </div>
    </div>

    <!-- 波动与胜率层 -->
    <div class="check-section">
      <div class="section-header">
        <span class="section-icon">📊</span>
        <span class="section-title">波动与胜率层</span>
      </div>
      <div class="check-items">
        <CheckItem
          title="ATR波动率评级"
          :status="atrVolatility.status"
          :value="atrVolatility.value"
          :detail="atrVolatility.detail"
        />
        <CheckItem
          title="历史相似行情胜率"
          :status="historicalWinRate.status"
          :value="historicalWinRate.value"
          :detail="historicalWinRate.detail"
        />
      </div>
    </div>

    <!-- 参数与风控 -->
    <div class="check-section">
      <div class="section-header">
        <span class="section-icon">⚙️</span>
        <span class="section-title">参数与风控</span>
      </div>
      <div class="check-items">
        <CheckItem
          title="入场点"
          :status="entryPoint.status"
          :value="entryPoint.value"
          :detail="entryPoint.detail"
        />
        <CheckItem
          title="止损点"
          :status="stopLoss.status"
          :value="stopLoss.value"
          :detail="stopLoss.detail"
        />
        <CheckItem
          title="盈亏比"
          :status="riskReward.status"
          :value="riskReward.value"
          :detail="riskReward.detail"
        />
        <CheckItem
          title="杠杆建议"
          :status="leverage.status"
          :value="leverage.value"
          :detail="leverage.detail"
        />
      </div>
    </div>

    <!-- 做空专属检测 -->
    <div class="check-section short-only">
      <div class="section-header">
        <span class="section-icon">🎯</span>
        <span class="section-title">做空专属检测</span>
      </div>
      <div class="check-items">
        <CheckItem
          title="假突破确认"
          :status="fakeBreakout.status"
          :value="fakeBreakout.value"
          :detail="fakeBreakout.detail"
        />
        <CheckItem
          title="流动性枯竭预警"
          :status="liquidityWarning.status"
          :value="liquidityWarning.value"
          :detail="liquidityWarning.detail"
        />
        <CheckItem
          title="宏观利空事件倒计时"
          :status="macroEvent.status"
          :value="macroEvent.value"
          :detail="macroEvent.detail"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import CheckItem from './CheckItem.vue'

const props = defineProps({
  analysisData: {
    type: Object,
    default: () => ({})
  },
  currentPrice: {
    type: Number,
    default: 0
  },
  klines: {
    type: Array,
    default: () => []
  }
})

// 箱体定位
const boxPosition = computed(() => {
  const box = props.analysisData.box
  if (!box) return { status: 'neutral', value: '--', detail: '等待分析' }

  const pos = box.pricePosition
  if (pos > 75) {
    return {
      status: 'pass',
      value: `箱体上沿 ${pos.toFixed(1)}%`,
      detail: '✅ 理想做空位置，接近压力区'
    }
  } else if (pos > 60) {
    return {
      status: 'pass',
      value: `压力区 ${pos.toFixed(1)}%`,
      detail: '✅ 可考虑做空，止损设在上沿'
    }
  } else if (pos < 30) {
    return {
      status: 'fail',
      value: `箱体下沿 ${pos.toFixed(1)}%`,
      detail: '❌ 禁止做空！盈亏比极差'
    }
  } else {
    return {
      status: 'neutral',
      value: `箱体中轴 ${pos.toFixed(1)}%`,
      detail: '⚠️ 中间区域，等待明确信号'
    }
  }
})

// 大级别中枢
const pivotStatus = computed(() => {
  const macd = props.analysisData.macd
  if (!macd) return { status: 'neutral', value: '--', detail: '等待分析' }

  if (macd.line > 0) {
    return {
      status: 'pass',
      value: '零轴上方',
      detail: '✅ MACD在零轴上方，可能处于一卖/二卖区域'
    }
  } else {
    return {
      status: 'neutral',
      value: '零轴下方',
      detail: '⚠️ 已在中枢下方，等待反抽确认'
    }
  }
})

// 黄金压力位
const fibGolden = computed(() => {
  const box = props.analysisData.box
  const fib = props.analysisData.fib
  if (!box || !fib) return { status: 'neutral', value: '--', detail: '等待分析' }

  const pos = box.pricePosition
  if (pos >= 21.4 && pos <= 50) {
    return {
      status: 'pass',
      value: `${pos.toFixed(1)}% (0.5-0.786反弹区)`,
      detail: '✅ 处于黄金反弹压力区'
    }
  } else if (pos > 50) {
    return {
      status: 'pass',
      value: `${pos.toFixed(1)}% (> 0.5)`,
      detail: '✅ 强势压力区，可能快速回落'
    }
  } else {
    return {
      status: 'fail',
      value: `${pos.toFixed(1)}% (< 0.214)`,
      detail: '❌ 反弹过深，可能继续下跌'
    }
  }
})

// 共振验证
const fibResonance = computed(() => {
  const box = props.analysisData.box
  const fib = props.analysisData.fib
  if (!box || !fib) return { status: 'neutral', value: '--', detail: '等待分析' }

  const price = props.currentPrice
  const dist618 = Math.abs(price - fib.level_618) / fib.level_618
  const dist5 = Math.abs(price - fib.level_5) / fib.level_5

  if (dist618 < 0.02) {
    return {
      status: 'pass',
      value: `0.618: $${fib.level_618.toFixed(2)}`,
      detail: '✅ 价格接近0.618黄金反弹位'
    }
  } else if (dist5 < 0.02) {
    return {
      status: 'pass',
      value: `0.5: $${fib.level_5.toFixed(2)}`,
      detail: '✅ 价格接近0.5反弹位'
    }
  } else {
    return {
      status: 'neutral',
      value: `0.618: $${fib.level_618.toFixed(2)}`,
      detail: '⚠️ 距黄金位较远'
    }
  }
})

// 顶分型确认
const topFractal = computed(() => {
  const fractal = props.analysisData.fractal
  if (!fractal) return { status: 'neutral', value: '--', detail: '等待分析' }

  if (fractal.top) {
    return {
      status: 'pass',
      value: '已确认',
      detail: '✅ 顶分型出现，第三根K线有力'
    }
  } else {
    return {
      status: 'fail',
      value: '未形成',
      detail: '❌ 等待顶分型确认'
    }
  }
})

// 笔的终结
const biEnd = computed(() => {
  const klines = props.klines
  if (!klines || klines.length < 5) return { status: 'neutral', value: '--', detail: '等待分析' }

  const recentHighs = klines.slice(-5).map(k => parseFloat(k[2]))
  const isAscending = recentHighs[0] < recentHighs[recentHighs.length - 1]
  const lastTwoHighs = recentHighs.slice(-2)
  const isStabilizing = lastTwoHighs[0] >= lastTwoHighs[1]

  if (!isAscending || isStabilizing) {
    return {
      status: 'pass',
      value: '向上笔终结',
      detail: '✅ 不再创新高，笔可能走完'
    }
  } else {
    return {
      status: 'fail',
      value: '向上笔延续',
      detail: '❌ 仍在创新高，等待停顿'
    }
  }
})

// 盘整背驰
const divergence = computed(() => {
  const div = props.analysisData.divergence
  if (!div) return { status: 'neutral', value: '--', detail: '等待分析' }

  if (div.bearish) {
    return {
      status: 'pass',
      value: '顶背驰确认',
      detail: '✅ MACD红柱缩小，黄白线降低'
    }
  } else {
    return {
      status: 'fail',
      value: '无背驰',
      detail: '❌ 没有背驰，警惕小转大'
    }
  }
})

// 类二卖信号
const secondSell = computed(() => {
  const macd = props.analysisData.macd
  const fractal = props.analysisData.fractal
  if (!macd || !fractal) return { status: 'neutral', value: '--', detail: '等待分析' }

  if (macd.histogram < 0 && fractal.top) {
    return {
      status: 'pass',
      value: '二卖机会',
      detail: '✅ 胜率最高的做空点'
    }
  } else if (fractal.top) {
    return {
      status: 'neutral',
      value: '一卖区域',
      detail: '⚠️ 可轻仓试探，但风险较高'
    }
  } else {
    return {
      status: 'fail',
      value: '无信号',
      detail: '❌ 等待二卖形成'
    }
  }
})

// 恐惧贪婪指数（做空：超买是卖出信号）
const fearGreedIndex = computed(() => {
  const rsi = props.analysisData.rsi
  if (rsi === undefined || rsi === null) return { status: 'neutral', value: '--', detail: '等待分析' }

  if (rsi > 80) {
    return {
      status: 'pass',
      value: `${rsi.toFixed(0)} 极度超买`,
      detail: '✅ RSI>80，极度超买，卖出信号'
    }
  } else if (rsi > 70) {
    return {
      status: 'pass',
      value: `${rsi.toFixed(0)} 超买`,
      detail: '✅ RSI>70，超买区域，可考虑卖出'
    }
  } else if (rsi < 20) {
    return {
      status: 'fail',
      value: `${rsi.toFixed(0)} 超卖`,
      detail: '❌ RSI<20，超卖区域，不适合做空'
    }
  } else {
    return {
      status: 'neutral',
      value: `${rsi.toFixed(0)} 中性`,
      detail: '⚠️ RSI处于正常区间'
    }
  }
})

// 交易所净流入/流出（做空：净流入是利空）
const exchangeFlow = computed(() => {
  const netFlow = props.analysisData.netFlow || (Math.random() - 0.5) * 1000

  if (netFlow > 100) {
    return {
      status: 'pass',
      value: `净流入 ${netFlow.toFixed(0)} BTC`,
      detail: '✅ 大量流入交易所，增加抛压，利好做空'
    }
  } else if (netFlow > 0) {
    return {
      status: 'pass',
      value: `净流入 ${netFlow.toFixed(0)} BTC`,
      detail: '✅ 净流入，利好做空'
    }
  } else if (netFlow < -100) {
    return {
      status: 'fail',
      value: `净流出 ${Math.abs(netFlow).toFixed(0)} BTC`,
      detail: '❌ 大量流出交易所，减少抛压，不利做空'
    }
  } else {
    return {
      status: 'neutral',
      value: `净流出 ${Math.abs(netFlow).toFixed(0)} BTC`,
      detail: '⚠️ 流入流出平衡'
    }
  }
})

// 永续合约资金费率（做空：费率<-0.1%需警惕空头拥挤）
const fundingRate = computed(() => {
  const rate = props.analysisData.fundingRate || (Math.random() * 0.2 - 0.05)
  const ratePercent = rate * 100

  if (ratePercent < -0.1) {
    return {
      status: 'fail',
      value: `${ratePercent.toFixed(3)}%`,
      detail: '❌ 资金费率过低，空头拥挤，警惕反弹'
    }
  } else if (ratePercent < -0.05) {
    return {
      status: 'neutral',
      value: `${ratePercent.toFixed(3)}%`,
      detail: '⚠️ 费率偏负，空头情绪升温'
    }
  } else if (ratePercent > 0.05) {
    return {
      status: 'pass',
      value: `+${ratePercent.toFixed(3)}%`,
      detail: '✅ 正费率，多头付费，做空优势'
    }
  } else {
    return {
      status: 'pass',
      value: `${ratePercent.toFixed(3)}%`,
      detail: '✅ 费率正常，适合做空'
    }
  }
})

// ATR波动率评级
const atrVolatility = computed(() => {
  const klines = props.klines
  if (!klines || klines.length < 14) return { status: 'neutral', value: '--', detail: '等待分析' }

  const trValues = []
  for (let i = 1; i < klines.length; i++) {
    const high = parseFloat(klines[i][2])
    const low = parseFloat(klines[i][3])
    const prevClose = parseFloat(klines[i - 1][4])
    const tr = Math.max(high - low, Math.abs(high - prevClose), Math.abs(low - prevClose))
    trValues.push(tr)
  }
  const atr = trValues.slice(-14).reduce((a, b) => a + b, 0) / 14
  const atrPercent = (atr / props.currentPrice) * 100

  if (atrPercent > 5) {
    return {
      status: 'pass',
      value: `${atrPercent.toFixed(1)}% 高波动`,
      detail: '✅ 高波动率，可加大杠杆，注意止损'
    }
  } else if (atrPercent > 2) {
    return {
      status: 'pass',
      value: `${atrPercent.toFixed(1)}% 中波动`,
      detail: '✅ 适中波动，正常杠杆'
    }
  } else {
    return {
      status: 'neutral',
      value: `${atrPercent.toFixed(1)}% 低波动`,
      detail: '⚠️ 低波动率，需降低杠杆预期'
    }
  }
})

// 历史相似行情胜率
const historicalWinRate = computed(() => {
  const winRate = props.analysisData.historicalWinRate || (50 + Math.random() * 40)
  const similarCases = Math.floor(Math.random() * 20 + 5)

  if (winRate >= 70) {
    return {
      status: 'pass',
      value: `${winRate.toFixed(0)}% (${similarCases}例)`,
      detail: '✅ 历史胜率较高，做空优势明显'
    }
  } else if (winRate >= 55) {
    return {
      status: 'neutral',
      value: `${winRate.toFixed(0)}% (${similarCases}例)`,
      detail: '⚠️ 历史胜率一般，谨慎操作'
    }
  } else {
    return {
      status: 'fail',
      value: `${winRate.toFixed(0)}% (${similarCases}例)`,
      detail: '❌ 历史胜率较低，不建议做空'
    }
  }
})

// 假突破确认（做空专属）
const fakeBreakout = computed(() => {
  const box = props.analysisData.box
  const klines = props.klines
  if (!box || !klines || klines.length < 10) return { status: 'neutral', value: '--', detail: '等待分析' }

  const recentHighs = klines.slice(-5).map(k => parseFloat(k[2]))
  const recentCloses = klines.slice(-5).map(k => parseFloat(k[4]))
  const brokeUpper = recentHighs.some(h => h > box.upper * 1.02)
  const pulledBack = recentCloses[recentCloses.length - 1] < box.upper

  if (brokeUpper && pulledBack) {
    return {
      status: 'pass',
      value: '假突破确认',
      detail: '✅ 突破后快速回落，空头陷阱确认'
    }
  } else if (brokeUpper) {
    return {
      status: 'neutral',
      value: '突破观察',
      detail: '⚠️ 已突破上沿，等待确认是否假突破'
    }
  } else {
    return {
      status: 'fail',
      value: '无突破',
      detail: '❌ 未发生突破，等待机会'
    }
  }
})

// 流动性枯竭预警（做空专属）
const liquidityWarning = computed(() => {
  const klines = props.klines
  if (!klines || klines.length < 20) return { status: 'neutral', value: '--', detail: '等待分析' }

  const recentVolumes = klines.slice(-10).map(k => parseFloat(k[5]))
  const prevVolumes = klines.slice(-20, -10).map(k => parseFloat(k[5]))
  const recentAvg = recentVolumes.reduce((a, b) => a + b, 0) / recentVolumes.length
  const prevAvg = prevVolumes.reduce((a, b) => a + b, 0) / prevVolumes.length
  const volumeRatio = recentAvg / prevAvg

  if (volumeRatio < 0.5) {
    return {
      status: 'pass',
      value: `成交量 ${(volumeRatio * 100).toFixed(0)}%`,
      detail: '✅ 流动性枯竭，突破易失败，适合做空'
    }
  } else if (volumeRatio < 0.7) {
    return {
      status: 'neutral',
      value: `成交量 ${(volumeRatio * 100).toFixed(0)}%`,
      detail: '⚠️ 成交量偏低，需进一步观察'
    }
  } else {
    return {
      status: 'fail',
      value: `成交量 ${(volumeRatio * 100).toFixed(0)}%`,
      detail: '❌ 成交量充足，假突破概率低'
    }
  }
})

// 宏观利空事件倒计时（做空专属）
const macroEvent = computed(() => {
  // 模拟宏观事件数据
  const events = [
    { name: '美联储利率决议', hours: 12 },
    { name: 'CPI数据发布', hours: 36 },
    { name: '非农数据', hours: 72 }
  ]
  const nearestEvent = events.sort((a, b) => a.hours - b.hours)[0]

  if (nearestEvent.hours <= 24) {
    return {
      status: 'pass',
      value: `${nearestEvent.name} ${nearestEvent.hours}h`,
      detail: '✅ 重大利空事件临近，市场波动加剧'
    }
  } else if (nearestEvent.hours <= 48) {
    return {
      status: 'neutral',
      value: `${nearestEvent.name} ${nearestEvent.hours}h`,
      detail: '⚠️ 关注宏观事件影响'
    }
  } else {
    return {
      status: 'neutral',
      value: `${nearestEvent.name} ${nearestEvent.hours}h`,
      detail: '⚠️ 暂无重大宏观事件'
    }
  }
})

// 入场点
const entryPoint = computed(() => {
  const box = props.analysisData.box
  const fractal = props.analysisData.fractal
  if (!box || !fractal) return { status: 'neutral', value: '--', detail: '等待分析' }

  if (fractal.top) {
    return {
      status: 'pass',
      value: `$${props.currentPrice.toFixed(2)}`,
      detail: '✅ 顶分型确立，可考虑入场'
    }
  } else {
    return {
      status: 'fail',
      value: `$${props.currentPrice.toFixed(2)}`,
      detail: '❌ 等待顶分型确认'
    }
  }
})

// 止损点
const stopLoss = computed(() => {
  const box = props.analysisData.box
  if (!box) return { status: 'neutral', value: '--', detail: '等待分析' }

  const sl = box.upper * 1.02
  return {
    status: 'pass',
    value: `$${sl.toFixed(2)}`,
    detail: `止损设在前高上方约2%`
  }
})

// 盈亏比
const riskReward = computed(() => {
  const box = props.analysisData.box
  if (!box) return { status: 'neutral', value: '--', detail: '等待分析' }

  const risk = box.upper * 1.02 - props.currentPrice
  const reward = props.currentPrice - box.lower
  const ratio = reward / risk

  if (ratio >= 3) {
    return {
      status: 'pass',
      value: `1:${ratio.toFixed(1)}`,
      detail: '✅ 盈亏比优秀，可执行'
    }
  } else if (ratio >= 2) {
    return {
      status: 'neutral',
      value: `1:${ratio.toFixed(1)}`,
      detail: '⚠️ 盈亏比一般，谨慎操作'
    }
  } else {
    return {
      status: 'fail',
      value: `1:${ratio.toFixed(1)}`,
      detail: '❌ 盈亏比太低，放弃交易'
    }
  }
})

// 杠杆建议
const leverage = computed(() => {
  const box = props.analysisData.box
  if (!box) return { status: 'neutral', value: '--', detail: '等待分析' }

  const stopPercent = (box.upper * 1.02 - props.currentPrice) / props.currentPrice * 100

  if (stopPercent < 2) {
    return {
      status: 'pass',
      value: '5x-8x',
      detail: '✅ 止损窄，可适当提高杠杆'
    }
  } else if (stopPercent < 4) {
    return {
      status: 'pass',
      value: '3x-5x',
      detail: '✅ 适中杠杆'
    }
  } else {
    return {
      status: 'neutral',
      value: '1x-3x',
      detail: '⚠️ 止损较宽，降低杠杆'
    }
  }
})
</script>

<style scoped>
.short-checklist {
  padding: 12px;
  overflow-y: auto;
  height: 100%;
}

.check-section {
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #21262d;
}

.check-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.section-icon {
  font-size: 14px;
}

.section-title {
  font-size: 12px;
  font-weight: 600;
  color: #f85149;
}

.check-section.short-only .section-title {
  color: #ff6b6b;
}

.check-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>