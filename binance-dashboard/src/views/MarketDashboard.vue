<template>
  <div class="market-dashboard">
    <div class="dashboard-grid">
      <!-- 左侧：行情数据 (2/3) -->
      <div class="market-section">
        <!-- 市场概览指标 -->
        <section class="overview-section">
          <MarketOverview :metrics="globalMetrics" />
        </section>

        <!-- 涨跌幅排行榜 -->
        <section class="rankings-section">
          <div class="rankings-grid">
            <TopGainers :items="topGainers" @select-symbol="goToTrading" />
            <TopLosers :items="topLosers" @select-symbol="goToTrading" />
          </div>
        </section>

        <!-- 热力图和热门币种 -->
        <section class="additional-section">
          <div class="additional-grid">
            <MarketHeatmap :items="heatmapData" @select-symbol="goToTrading" />
            <TrendingCoins :items="trendingCoins" @select-symbol="goToTrading" />
          </div>
        </section>

        <!-- 快速访问热门交易对 -->
        <section class="quick-access">
          <h3>⚡ 快速访问</h3>
          <div class="quick-links">
            <router-link
              v-for="symbol in popularSymbols"
              :key="symbol"
              :to="`/trading/${symbol}`"
              class="quick-link"
            >
              {{ symbol.replace('USDT', '') }}
            </router-link>
          </div>
        </section>
      </div>

      <!-- 右侧：资讯与分析 (1/3) -->
      <div class="info-section">
        <!-- 宏观市场分析 -->
        <section class="market-analysis-section">
          <MarketAIAnalysis :global-metrics="globalMetrics" />
        </section>

        <!-- 资讯板块 -->
        <section class="news-section">
          <NewsFeed />
        </section>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-overlay">
      <LoadingSpinner text="加载市场数据..." />
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMarket } from '@/composables/useMarket'
import MarketOverview from '@/components/market/MarketOverview.vue'
import TopGainers from '@/components/market/TopGainers.vue'
import TopLosers from '@/components/market/TopLosers.vue'
import MarketHeatmap from '@/components/market/MarketHeatmap.vue'
import TrendingCoins from '@/components/market/TrendingCoins.vue'
import NewsFeed from '@/components/market/NewsFeed.vue'
import MarketAIAnalysis from '@/components/market/MarketAIAnalysis.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const router = useRouter()
const {
  globalMetrics,
  topGainers,
  topLosers,
  trendingCoins,
  heatmapData,
  isLoading,
  refreshAllMarketData
} = useMarket()

const popularSymbols = [
  'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT',
  'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT'
]

const goToTrading = (symbol) => {
  router.push(`/trading/${symbol}`)
}

let refreshInterval = null

onMounted(async () => {
  await refreshAllMarketData()
  // 每 30 秒刷新一次
  refreshInterval = setInterval(refreshAllMarketData, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.market-dashboard {
  padding: 20px;
  height: calc(100vh - 60px);
  overflow: hidden;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  height: 100%;
}

/* 左侧行情区域 */
.market-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
  padding-right: 8px;
}

.market-section::-webkit-scrollbar {
  width: 6px;
}

.market-section::-webkit-scrollbar-thumb {
  background: #30363d;
  border-radius: 3px;
}

.overview-section {
  flex-shrink: 0;
}

.rankings-section {
  flex-shrink: 0;
}

.rankings-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.additional-section {
  flex-shrink: 0;
}

.additional-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}

.quick-access {
  flex-shrink: 0;
  background: #161b22;
  border: 1px solid #21262d;
  border-radius: 12px;
  padding: 16px;
}

.quick-access h3 {
  font-size: 14px;
  font-weight: 600;
  color: #e6edf3;
  margin: 0 0 12px 0;
}

.quick-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-link {
  padding: 8px 16px;
  background: #21262d;
  color: #e6edf3;
  text-decoration: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s;
}

.quick-link:hover {
  background: #f0b90b;
  color: #000;
}

/* 右侧资讯分析区域 */
.info-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
  min-height: 0;
}

.market-analysis-section {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

.news-section {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
  }

  .market-section {
    max-height: 60vh;
  }

  .info-section {
    flex-direction: row;
    height: auto;
    min-height: 400px;
  }

  .market-analysis-section,
  .news-section {
    flex: 1;
    height: 100%;
  }
}

@media (max-width: 768px) {
  .rankings-grid,
  .additional-grid {
    grid-template-columns: 1fr;
  }

  .info-section {
    flex-direction: column;
  }

  .market-analysis-section,
  .news-section {
    height: 300px;
  }
}

.loading-overlay {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(13, 17, 23, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}
</style>