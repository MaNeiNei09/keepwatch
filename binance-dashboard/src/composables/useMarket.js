// 市场概览数据逻辑
import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE = '/api'

// 全局市场指标
const globalMetrics = ref({
  totalMarketCap: 0,
  totalVolume24h: 0,
  btcDominance: 0,
  ethDominance: 0,
  activeCryptocurrencies: 0,
  marketCapChangePercentage24h: 0,
  lastUpdated: null
})

// 涨跌幅排行
const topGainers = ref([])
const topLosers = ref([])
const trendingCoins = ref([])
const heatmapData = ref([])

// 加载状态
const loading = ref({
  global: false,
  gainers: false,
  losers: false,
  trending: false,
  heatmap: false
})

// 获取全局市场指标
const fetchGlobalMetrics = async () => {
  loading.value.global = true
  try {
    const res = await axios.get(`${API_BASE}/market/global`)
    globalMetrics.value = {
      ...res.data,
      lastUpdated: new Date().toISOString()
    }
  } catch (error) {
    console.error('获取全局市场指标失败:', error)
    // 使用模拟数据
    globalMetrics.value = {
      totalMarketCap: 2650000000000,
      totalVolume24h: 85000000000,
      btcDominance: 52.5,
      ethDominance: 17.8,
      activeCryptocurrencies: 12500,
      marketCapChangePercentage24h: 1.2,
      lastUpdated: new Date().toISOString()
    }
  } finally {
    loading.value.global = false
  }
}

// 获取涨幅榜
const fetchTopGainers = async (limit = 10) => {
  loading.value.gainers = true
  try {
    const res = await axios.get(`${API_BASE}/market/gainers`, { params: { limit } })
    topGainers.value = res.data
  } catch (error) {
    console.error('获取涨幅榜失败:', error)
    // 使用模拟数据
    topGainers.value = generateMockGainers(limit)
  } finally {
    loading.value.gainers = false
  }
}

// 获取跌幅榜
const fetchTopLosers = async (limit = 10) => {
  loading.value.losers = true
  try {
    const res = await axios.get(`${API_BASE}/market/losers`, { params: { limit } })
    topLosers.value = res.data
  } catch (error) {
    console.error('获取跌幅榜失败:', error)
    // 使用模拟数据
    topLosers.value = generateMockLosers(limit)
  } finally {
    loading.value.losers = false
  }
}

// 获取热门币种
const fetchTrending = async () => {
  loading.value.trending = true
  try {
    const res = await axios.get(`${API_BASE}/market/trending`)
    trendingCoins.value = res.data
  } catch (error) {
    console.error('获取热门币种失败:', error)
    // 使用模拟数据
    trendingCoins.value = generateMockTrending()
  } finally {
    loading.value.trending = false
  }
}

// 获取热力图数据
const fetchHeatmapData = async () => {
  loading.value.heatmap = true
  try {
    const res = await axios.get(`${API_BASE}/market/heatmap`)
    heatmapData.value = res.data
  } catch (error) {
    console.error('获取热力图数据失败:', error)
    // 使用模拟数据
    heatmapData.value = generateMockHeatmap()
  } finally {
    loading.value.heatmap = false
  }
}

// 刷新所有市场数据
const refreshAllMarketData = async () => {
  await Promise.all([
    fetchGlobalMetrics(),
    fetchTopGainers(),
    fetchTopLosers(),
    fetchTrending(),
    fetchHeatmapData()
  ])
}

// 格式化工具
const formatLargeNumber = (num) => {
  if (!num) return '0'
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T'
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B'
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M'
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K'
  return num.toFixed(2)
}

const formatPrice = (price) => {
  if (!price) return '0.00'
  const num = parseFloat(price)
  if (num >= 1000) return num.toFixed(2)
  if (num >= 1) return num.toFixed(4)
  return num.toFixed(6)
}

const formatChange = (change) => {
  if (!change) return '0.00'
  const num = parseFloat(change)
  const sign = num >= 0 ? '+' : ''
  return `${sign}${num.toFixed(2)}%`
}

// 模拟数据生成器
const generateMockGainers = (limit) => {
  const symbols = ['PEPEUSDT', 'BONKUSDT', 'WIFUSDT', 'FLOKIUSDT', 'SHIBUSDT', 'DOGEUSDT', 'SOLUSDT', 'AVAXUSDT', 'MATICUSDT', 'LINKUSDT']
  return symbols.slice(0, limit).map((symbol, i) => ({
    symbol,
    baseAsset: symbol.replace('USDT', ''),
    price: (Math.random() * 100).toFixed(6),
    change24h: (15 + Math.random() * 30).toFixed(2),
    volume: (Math.random() * 1e9).toFixed(0),
    marketCap: (Math.random() * 1e10).toFixed(0)
  }))
}

const generateMockLosers = (limit) => {
  const symbols = ['APTUSDT', 'ARBUSDT', 'OPUSDT', 'BLURUSDT', 'SUIUSDT', 'SEIUSDT', 'TIAUSDT', 'INJUSDT', 'TWTUSDT', 'GMXUSDT']
  return symbols.slice(0, limit).map((symbol, i) => ({
    symbol,
    baseAsset: symbol.replace('USDT', ''),
    price: (Math.random() * 50).toFixed(6),
    change24h: (-5 - Math.random() * 15).toFixed(2),
    volume: (Math.random() * 5e8).toFixed(0),
    marketCap: (Math.random() * 5e9).toFixed(0)
  }))
}

const generateMockTrending = () => {
  return [
    { symbol: 'BTCUSDT', name: 'Bitcoin', rank: 1 },
    { symbol: 'ETHUSDT', name: 'Ethereum', rank: 2 },
    { symbol: 'SOLUSDT', name: 'Solana', rank: 3 },
    { symbol: 'PEPEUSDT', name: 'Pepe', rank: 4 },
    { symbol: 'WIFUSDT', name: 'dogwifhat', rank: 5 },
    { symbol: 'DOGEUSDT', name: 'Dogecoin', rank: 6 }
  ]
}

const generateMockHeatmap = () => {
  const symbols = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
    'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT', 'LINKUSDT', 'MATICUSDT',
    'DOTUSDT', 'LTCUSDT', 'UNIUSDT', 'ATOMUSDT', 'ETCUSDT'
  ]
  return symbols.map(symbol => ({
    symbol,
    baseAsset: symbol.replace('USDT', ''),
    marketCap: Math.random() * 1e12,
    change24h: (Math.random() * 20 - 10).toFixed(2)
  }))
}

// 计算属性
const isLoading = computed(() =>
  loading.value.global ||
  loading.value.gainers ||
  loading.value.losers ||
  loading.value.trending ||
  loading.value.heatmap
)

export function useMarket() {
  return {
    // 状态
    globalMetrics,
    topGainers,
    topLosers,
    trendingCoins,
    heatmapData,
    loading,
    isLoading,

    // 方法
    fetchGlobalMetrics,
    fetchTopGainers,
    fetchTopLosers,
    fetchTrending,
    fetchHeatmapData,
    refreshAllMarketData,

    // 工具
    formatLargeNumber,
    formatPrice,
    formatChange
  }
}