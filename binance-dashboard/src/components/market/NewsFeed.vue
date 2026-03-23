<template>
  <div class="news-feed">
    <div class="section-header">
      <h3>📰 市场资讯</h3>
      <span class="update-time">{{ lastUpdate }}</span>
    </div>

    <div class="news-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="['tab-btn', { active: activeTab === tab.key }]"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <div class="news-list" ref="newsListRef">
      <div v-if="isLoading" class="loading-state">
        <div class="pulse-loader"></div>
        <span>加载资讯中...</span>
      </div>

      <template v-else>
        <div
          v-for="news in newsList"
          :key="news.id"
          class="news-item"
          :class="news.type"
        >
          <div class="news-meta">
            <span class="news-type">{{ getTypeLabel(news.type) }}</span>
            <span class="news-time">{{ formatTime(news.time) }}</span>
          </div>
          <h4 class="news-title">{{ news.title }}</h4>
          <p class="news-summary">{{ news.summary }}</p>
          <div v-if="news.tags && news.tags.length" class="news-tags">
            <span v-for="tag in news.tags.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>

        <div v-if="newsList.length === 0" class="empty-state">
          暂无资讯数据
        </div>
      </template>
    </div>

    <div class="news-footer">
      <span class="news-count">共 {{ total }} 条资讯</span>
      <button class="refresh-btn" @click="refreshNews" :disabled="isRefreshing">
        <span :class="{ rotating: isRefreshing }">🔄</span> 刷新
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const API_BASE = '/api'

const activeTab = ref('all')
const isRefreshing = ref(false)
const isLoading = ref(true)
const lastUpdate = ref('刚刚')
const newsList = ref([])
const total = ref(0)
const newsListRef = ref(null)

const tabs = [
  { key: 'all', label: '全部' },
  { key: 'policy', label: '政策' },
  { key: 'market', label: '市场' },
  { key: 'tech', label: '技术' }
]

// 获取资讯列表
const fetchNews = async () => {
  isLoading.value = true
  try {
    const params = {
      type: activeTab.value,
      limit: 50,
      days: 30
    }
    const res = await axios.get(`${API_BASE}/news`, { params })
    if (res.data && res.data.data) {
      newsList.value = res.data.data
      total.value = res.data.total
    }
  } catch (error) {
    console.error('获取资讯失败:', error)
    // 如果请求失败，使用本地缓存或模拟数据
    newsList.value = getFallbackNews()
    total.value = newsList.value.length
  } finally {
    isLoading.value = false
    lastUpdate.value = '刚刚'
  }
}

// 备用资讯数据
const getFallbackNews = () => [
  {
    id: 1,
    type: 'policy',
    title: '美联储暗示年内可能降息，市场情绪转暖',
    summary: '美联储主席鲍威尔表示通胀已取得显著进展，暗示年内可能开始降息周期，加密市场应声上涨。',
    time: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
    tags: ['美联储', '降息', 'BTC']
  },
  {
    id: 2,
    type: 'market',
    title: '比特币ETF连续三日净流入，机构需求强劲',
    summary: '贝莱德和富达的比特币ETF连续三日录得净流入，显示机构投资者对加密资产的兴趣持续增长。',
    time: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    tags: ['ETF', '机构', 'BTC']
  },
  {
    id: 3,
    type: 'tech',
    title: '以太坊Dencun升级成功，Layer2费用大幅降低',
    summary: '以太坊完成Dencun升级后，主要Layer2网络的交易费用下降90%以上，提升了用户体验。',
    time: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    tags: ['ETH', 'Layer2', '升级']
  }
]

const getTypeLabel = (type) => {
  const labels = {
    policy: '📢 政策',
    market: '📈 市场',
    tech: '🔧 技术'
  }
  return labels[type] || type
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const diff = Date.now() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
}

const refreshNews = async () => {
  isRefreshing.value = true
  await fetchNews()
  setTimeout(() => {
    isRefreshing.value = false
  }, 500)
}

// 监听标签切换
watch(activeTab, () => {
  fetchNews()
})

onMounted(() => {
  fetchNews()
})
</script>

<style scoped>
.news-feed {
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

.update-time {
  font-size: 11px;
  color: #7d8590;
}

.news-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 12px;
  border-bottom: 1px solid #21262d;
  padding-bottom: 8px;
}

.tab-btn {
  padding: 4px 10px;
  background: transparent;
  border: none;
  color: #7d8590;
  font-size: 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.15s;
}

.tab-btn:hover {
  color: #e6edf3;
  background: #21262d;
}

.tab-btn.active {
  color: #f0b90b;
  background: rgba(240, 185, 11, 0.1);
}

.news-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.news-list::-webkit-scrollbar {
  width: 4px;
}

.news-list::-webkit-scrollbar-thumb {
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

.empty-state {
  text-align: center;
  padding: 40px;
  color: #7d8590;
  font-size: 12px;
}

.news-item {
  padding: 10px;
  background: #0d1117;
  border-radius: 8px;
  border-left: 3px solid #30363d;
  cursor: pointer;
  transition: all 0.15s;
}

.news-item:hover {
  background: #161b22;
}

.news-item.policy {
  border-left-color: #f0883e;
}

.news-item.market {
  border-left-color: #3fb950;
}

.news-item.tech {
  border-left-color: #58a6ff;
}

.news-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.news-type {
  font-size: 11px;
  color: #7d8590;
}

.news-time {
  font-size: 10px;
  color: #484f58;
}

.news-title {
  font-size: 13px;
  font-weight: 600;
  color: #e6edf3;
  margin: 0 0 4px 0;
  line-height: 1.4;
}

.news-summary {
  font-size: 11px;
  color: #7d8590;
  margin: 0 0 6px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.tag {
  font-size: 10px;
  padding: 2px 6px;
  background: #21262d;
  color: #7d8590;
  border-radius: 3px;
}

.news-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px solid #21262d;
}

.news-count {
  font-size: 11px;
  color: #484f58;
}

.refresh-btn {
  padding: 4px 10px;
  background: transparent;
  border: 1px solid #30363d;
  color: #7d8590;
  font-size: 11px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.refresh-btn:hover:not(:disabled) {
  background: #21262d;
  color: #e6edf3;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.rotating {
  display: inline-block;
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>