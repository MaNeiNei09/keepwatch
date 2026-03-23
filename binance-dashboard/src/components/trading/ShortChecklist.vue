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

.check-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
</style>