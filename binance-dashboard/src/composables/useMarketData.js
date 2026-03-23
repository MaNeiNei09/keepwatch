// 市场数据相关逻辑
import { ref } from 'vue'
import axios from 'axios'

// 使用后端代理API
const API_BASE = '/api'

// 状态
const tickerData = ref({ price: 0 })
const ticker24h = ref({})
const orderbook = ref({ bids: [], asks: [] })
const klines = ref([])
const allSymbols = ref([])

// 工具函数
const formatPrice = (price) => {
  if (!price) return '0.00'
  const num = parseFloat(price)
  if (num >= 1000) return num.toFixed(2)
  if (num >= 1) return num.toFixed(4)
  return num.toFixed(6)
}

const formatNumber = (num) => {
  if (!num) return '0'
  const n = parseFloat(num)
  if (n >= 1e9) return (n / 1e9).toFixed(2) + 'B'
  if (n >= 1e6) return (n / 1e6).toFixed(2) + 'M'
  if (n >= 1e3) return (n / 1e3).toFixed(2) + 'K'
  return n.toFixed(2)
}

// API请求
const fetchTicker = async (symbol) => {
  try {
    const [tickerRes, ticker24hRes] = await Promise.all([
      axios.get(`${API_BASE}/ticker/${symbol}`),
      axios.get(`${API_BASE}/ticker/24h/${symbol}`)
    ])
    tickerData.value = tickerRes.data
    ticker24h.value = ticker24hRes.data
  } catch (error) {
    console.error('获取行情数据失败:', error)
  }
}

const fetchOrderbook = async (symbol, limit = 20) => {
  try {
    const res = await axios.get(`${API_BASE}/orderbook/${symbol}`, {
      params: { limit }
    })
    orderbook.value = res.data
  } catch (error) {
    console.error('获取订单簿失败:', error)
  }
}

const fetchKlines = async (symbol, interval, limit = 200) => {
  try {
    const res = await axios.get(`${API_BASE}/klines/${symbol}`, {
      params: { interval, limit }
    })
    klines.value = res.data
  } catch (error) {
    console.error('获取K线数据失败:', error)
  }
}

const fetchAllSymbols = async () => {
  try {
    const res = await axios.get(`${API_BASE}/symbols`)
    allSymbols.value = res.data
  } catch (error) {
    console.error('获取交易对列表失败:', error)
  }
}

// 计算价差
const spread = ref(0)
const maxAskQty = ref(0)
const maxBidQty = ref(0)

const updateOrderbookMetrics = () => {
  if (orderbook.value.asks?.length && orderbook.value.bids?.length) {
    const lowestAsk = parseFloat(orderbook.value.asks[0][0])
    const highestBid = parseFloat(orderbook.value.bids[0][0])
    spread.value = (lowestAsk - highestBid).toFixed(2)

    maxAskQty.value = Math.max(...orderbook.value.asks.slice(0, 10).map(a => parseFloat(a[1])))
    maxBidQty.value = Math.max(...orderbook.value.bids.slice(0, 10).map(b => parseFloat(b[1])))
  }
}

export function useMarketData() {
  return {
    // 状态
    tickerData,
    ticker24h,
    orderbook,
    klines,
    allSymbols,
    spread,
    maxAskQty,
    maxBidQty,

    // 工具函数
    formatPrice,
    formatNumber,

    // API方法
    fetchTicker,
    fetchOrderbook,
    fetchKlines,
    fetchAllSymbols,
    updateOrderbookMetrics
  }
}