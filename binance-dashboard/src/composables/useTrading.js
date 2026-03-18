// 交易对选择相关状态和逻辑
import { ref, computed } from 'vue'

// 状态
const selectedSymbol = ref('BTCUSDT')
const searchQuery = ref('')
const showDropdown = ref(false)
const searchWrapper = ref(null)
const allSymbols = ref([])
const defaultSymbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT']

// 常用交易对
const popularSymbols = [
  { symbol: 'BTCUSDT', base: 'BTC', quote: 'USDT' },
  { symbol: 'ETHUSDT', base: 'ETH', quote: 'USDT' },
  { symbol: 'BNBUSDT', base: 'BNB', quote: 'USDT' },
  { symbol: 'SOLUSDT', base: 'SOL', quote: 'USDT' },
  { symbol: 'XRPUSDT', base: 'XRP', quote: 'USDT' }
]

// 计算属性
const filteredSymbols = computed(() => {
  if (!searchQuery.value) return []
  const query = searchQuery.value.toUpperCase()
  return allSymbols.value.filter(s =>
    s.symbol.toUpperCase().includes(query)
  ).slice(0, 10)
})

// 方法
const selectSymbol = (symbol) => {
  selectedSymbol.value = symbol
  showDropdown.value = false
  searchQuery.value = ''
}

const formatSymbol = (symbol) => {
  if (!symbol) return ''
  return symbol.replace('USDT', '/USDT')
}

const onSearchInput = () => {
  showDropdown.value = true
}

const getCoinIcon = (symbol) => {
  const icons = {
    'BTC': '₿', 'ETH': 'Ξ', 'BNB': 'B', 'SOL': 'S',
    'XRP': 'X', 'ADA': 'A', 'DOGE': 'D', 'AVAX': 'A'
  }
  const base = symbol?.replace('USDT', '') || ''
  return icons[base] || '●'
}

const setAllSymbols = (symbols) => {
  allSymbols.value = symbols
}

// 关闭下拉框
const closeDropdown = (event) => {
  if (searchWrapper.value && !searchWrapper.value.contains(event.target)) {
    showDropdown.value = false
  }
}

export function useTrading() {
  return {
    // 状态
    selectedSymbol,
    searchQuery,
    showDropdown,
    searchWrapper,
    allSymbols,
    defaultSymbols,
    popularSymbols,

    // 计算属性
    filteredSymbols,

    // 方法
    selectSymbol,
    formatSymbol,
    onSearchInput,
    getCoinIcon,
    setAllSymbols,
    closeDropdown
  }
}