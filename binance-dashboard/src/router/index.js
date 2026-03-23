import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'MarketDashboard',
    component: () => import('@/views/MarketDashboard.vue'),
    meta: { title: '市场概览' }
  },
  {
    path: '/trading/:symbol?',
    name: 'TradingPairDetail',
    component: () => import('@/views/TradingPairDetail.vue'),
    meta: { title: '交易对详情' },
    props: true
  },
  {
    path: '/checklist',
    name: 'TradingChecklist',
    component: () => import('@/views/TradingChecklist.vue'),
    meta: { title: '交易检测' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：更新页面标题
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || 'Dashboard'} | 币安行情`
  next()
})

export default router