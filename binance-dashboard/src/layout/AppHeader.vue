<template>
  <header class="app-header">
    <div class="header-left">
      <router-link to="/" class="logo">
        <span class="logo-icon">📊</span>
        <span class="logo-text">币安行情</span>
      </router-link>
    </div>

    <nav class="header-nav">
      <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
        市场概览
      </router-link>
      <router-link
        v-if="currentSymbol"
        :to="`/trading/${currentSymbol}`"
        class="nav-link"
        :class="{ active: $route.path.startsWith('/trading') }"
      >
        交易详情
      </router-link>
      <router-link to="/checklist" class="nav-link" :class="{ active: $route.path === '/checklist' }">
        交易检测
      </router-link>
    </nav>

    <div class="header-right">
      <SearchBox
        v-model="searchQuery"
        :symbols="symbols"
        placeholder="搜索交易对..."
        @select="handleSearchSelect"
      />
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMarketData } from '@/composables/useMarketData'
import SearchBox from '@/components/common/SearchBox.vue'

const router = useRouter()
const { allSymbols } = useMarketData()

const searchQuery = ref('')

const symbols = computed(() => allSymbols.value)
const currentSymbol = computed(() => {
  const symbol = router.currentRoute.value.params.symbol
  return symbol || null
})

const handleSearchSelect = (symbol) => {
  searchQuery.value = ''
  router.push(`/trading/${symbol}`)
}
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: #0d1117;
  border-bottom: 1px solid #21262d;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #e6edf3;
}

.logo-icon {
  font-size: 20px;
}

.logo-text {
  font-size: 16px;
  font-weight: 700;
}

.header-nav {
  display: flex;
  gap: 4px;
}

.nav-link {
  padding: 8px 16px;
  color: #8b949e;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  border-radius: 6px;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #e6edf3;
  background: #21262d;
}

.nav-link.active {
  color: #f0b90b;
  background: rgba(240, 185, 11, 0.1);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

@media (max-width: 768px) {
  .header-nav {
    display: none;
  }
}
</style>