# Release Notes / 版本更新日志

---

## [v2.4.0] - 2026-03-23

### 新增功能

#### AI分析组件重构
- **移动到交易对详情页**：AI智能分析现位于交易对页面的智能趋势分析区域
- **基于当前交易对动态分析**：
  - 根据选择的交易对实时计算各项指标
  - 动态生成缠论分析、结构形态、清算地图
  - 基于K线数据计算RSI、MACD、支撑阻力位
  - 多周期趋势分析（5m/15m/30m/1h/4h/1d）
- **情绪指数动态计算**：基于RSI、涨跌幅实时计算恐惧贪婪指数
- **操作建议智能生成**：根据趋势和指标动态生成操作建议

### 优化
- 市场概览页面简化，只保留资讯板块
- AI分析响应交易对切换，自动重新分析

---

## [v2.3.0] - 2026-03-23

### 新增功能

#### MACD组件优化
- 新增零线显示（白色虚线），更清晰标识多空分界

#### AI智能分析增强
- **清算地图分析**
  - 多头/空头清算总量统计
  - 最近清算位置距离计算
  - 多头清算聚集价位展示（价格、金额、强度）
  - 空头清算聚集价位展示
  - 清算区域洞察分析

### 优化
- 清算地图可视化条形图，直观展示清算强度
- 清算洞察提示，辅助判断市场关键位置

---

## [v2.2.0] - 2026-03-23

### 新增功能

#### AI智能分析增强
- **缠论分析**
  - 当前走势方向判断（上涨/下跌）
  - 中枢位置识别
  - 买卖点信号（一买/二买/一卖/二卖）
  - 离开中枢状态
  - 笔结构和线段结构分析
- **结构形态分析**
  - 箱体震荡检测：上下沿、当前位置、操作建议
  - 旗形整理检测：形态类型、突破目标、完成度
- **宏观经济影响**
  - 美联储利率影响分析
  - 美元指数走势影响
  - ETF资金流向追踪
  - 监管环境变化评估
- **突发事件监控**
  - 重大事件实时提醒
  - 事件影响分析
  - 受影响币种标注
  - 严重程度分级

### 优化
- AI分析组件布局优化，支持滚动查看更多分析内容
- 新增多个分析板块，提供更全面的市场诊断

---

## [v2.1.0] - 2026-03-23

### 新增功能

#### 资讯与趋势分析板块
- 市场概览页面重新布局：左侧 2/3 行情数据，右侧 1/3 资讯与分析
- 新增资讯组件 `NewsFeed.vue`
  - 支持分类筛选：全部/政策/市场/技术
  - 展示资讯标题、摘要、标签、发布时间
  - 从后端 API 加载近 30 天资讯数据
- 新增 AI 分析组件 `AIAnalysis.vue`
  - 市场情绪仪表（恐惧贪婪指数）
  - 市场综合诊断分析
  - 关键信号提示（看涨/看跌/中性）
  - 重点币种分析（BTC/ETH/SOL）
  - 操作建议列表

#### 后端资讯服务
- 新增 SQLite 资讯数据库 (`data/news.db`)
  - 支持资讯的增删改查
  - 自动初始化近一个月示例数据
- 新增资讯 API 端点：
  - `GET /api/news` - 获取资讯列表（支持类型/时间筛选）
  - `GET /api/news/<id>` - 获取资讯详情
  - `POST /api/news` - 添加资讯
  - `PUT /api/news/<id>` - 更新资讯
  - `DELETE /api/news/<id>` - 删除资讯
  - `GET /api/news/stats` - 获取资讯统计

### 优化
- 移除交易详情页独立成交量组件（TradingView 已内置成交量显示）
- 简化 `useChart.js` 配置，移除 volume 相关配置

### 组件变更
- 新增 `components/market/NewsFeed.vue`
- 新增 `components/market/AIAnalysis.vue`
- 删除 `components/charts/VolumeChart.vue`
- 修改 `views/MarketDashboard.vue` 布局结构
- 修改 `views/TradingPairDetail.vue` 移除成交量区块

---

## [v2.0.0] - 2026-03-19

### 重大更新 (Major Update)

#### 新增市场概览页面
- 新增市场概览 Dashboard 页面，展示整体加密货币市场信息
- 市场概览指标：总市值、24h交易量、BTC主导率、ETH主导率、活跃币种数量
- 涨幅榜：展示24h涨幅最大的币种排行
- 跌幅榜：展示24h跌幅最大的币种排行
- 市场热力图：按市值大小和涨跌幅显示币种色块
- 热门币种：基于交易量排序的热门币种列表
- 快速访问：一键跳转常用交易对

#### 路由系统
- 引入 vue-router 实现多页面路由
- 路由配置：
  - `/` - 市场概览首页
  - `/trading/:symbol?` - 交易对详情页

#### 组件拆分重构
- 新增 `views/` 目录存放页面组件
  - `MarketDashboard.vue` - 市场概览页面
  - `TradingPairDetail.vue` - 交易对详情页面（从 App.vue 重构）
- 新增 `layout/` 目录存放布局组件
  - `AppLayout.vue` - 主布局容器
  - `AppHeader.vue` - 顶部导航栏（含全局搜索、导航链接）
- 新增 `components/market/` 目录存放市场组件
  - `MarketOverview.vue` - 市场概览卡片
  - `TopGainers.vue` - 涨幅榜
  - `TopLosers.vue` - 跌幅榜
  - `MarketHeatmap.vue` - 市场热力图
  - `TrendingCoins.vue` - 热门币种
- 新增 `components/common/` 通用组件
  - `SearchBox.vue` - 可复用搜索输入框
  - `LoadingSpinner.vue` - 加载状态指示器

#### Composables 扩展
- 新增 `composables/useMarket.js` - 市场概览数据获取逻辑

#### 后端 API 扩展
- 新增市场数据 API 端点：
  - `GET /api/market/global` - 全局市场指标
  - `GET /api/market/gainers` - 涨幅榜
  - `GET /api/market/losers` - 跌幅榜
  - `GET /api/market/trending` - 热门币种
  - `GET /api/market/heatmap` - 热力图数据

### 目录结构
```
src/
├── views/            # 页面组件
│   ├── MarketDashboard.vue
│   └── TradingPairDetail.vue
├── layout/           # 布局组件
│   ├── AppLayout.vue
│   └── AppHeader.vue
├── components/
│   ├── charts/       # 图表组件
│   ├── cards/        # 卡片组件
│   ├── common/       # 通用组件
│   └── market/       # 市场组件（新增）
├── composables/      # 组合式API
├── router/           # 路由配置（新增）
├── styles/           # 样式文件
├── App.vue           # 根组件
└── main.js           # 入口文件
```

---

## [v1.2.0] - 2026-03-18

### 重构 (Refactoring)
- App.vue 完全重构，使用新的组件和 composables
- 模板中使用新组件: PriceCard, CycleCard, DecisionCard, PositionCard, IndicatorModal
- 脚本中引入并使用所有 composables
- 保留原有的图表初始化和事件处理逻辑

---

## [v1.1.0] - 2026-03-18

### 重构 (Refactoring)
- 按照敏捷迭代原则重构 App.vue 文件
- 提取业务逻辑到 composables 目录:
  - `useTrading.js` - 交易对选择相关状态和逻辑
  - `useChart.js` - K线图表相关逻辑
  - `useMarketData.js` - 市场数据相关逻辑
  - `useIndicators.js` - 技术指标计算逻辑
  - `useDecision.js` - 智能决策逻辑
- 提取组件到 components 目录:
  - `components/charts/` - 图表组件 (CandleChart, VolumeChart, RSIChart, MACDChart)
  - `components/cards/` - 卡片组件 (PriceCard, CycleCard, DecisionCard, PositionCard)
  - `components/common/` - 通用组件 (IndicatorModal)
- 提取样式到独立文件:
  - `styles/global.css` - 全局样式和CSS变量

### 目录结构
```
src/
├── components/
│   ├── charts/       # 图表组件
│   ├── cards/        # 卡片组件
│   └── common/       # 通用组件
├── composables/      # 组合式API (业务逻辑)
├── styles/           # 样式文件
├── App.vue           # 主应用组件
└── main.js           # 入口文件
```

---

## [v1.0.1] - 2026-03-18

### 新增功能
- RSI组件增加右下角拖动点，支持鼠标拖动调整高度
- 订单簿组件支持拖动调整高度（最大1500px）

### 修复
- 修复RSI组件拖动点不显示的问题
- 优化拖动点的可见性（增大尺寸至24x24px，添加对角线标识）
- 调整rsi-zones位置避免遮挡拖动点

---

## [v1.0.0] - 2026-03-18

### 新增功能
- 将RSI从成交量组件中拆分出来，单独作为一个组件
- K线走势图、成交量、RSI、MACD四个组件的高度支持动态调整
- 添加右下角拖动点，支持鼠标拖动调整各组件高度
- 订单簿组件支持拖动调整高度（最大1500px）
- 指标配置改为弹出窗口模式（点击"指标配置"按钮）
- ATR参数默认隐藏，通过指标配置弹窗勾选后显示
- 第一排四个卡片组件高度调整为3/4

### UI优化
- 所有图表组件支持右下角拖拽调整高度
- 第一排卡片内容字体相应缩小

---

## 更新日志格式

```
## [版本号] - 日期

### 新增功能
- 新功能描述

### 优化
- 优化内容

### 修复
- 修复的问题
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v2.4.0 | 2026-03-23 | AI分析移至交易对页面，基于当前交易对动态分析 |
| v2.3.0 | 2026-03-23 | MACD零线、清算地图分析 |
| v2.2.0 | 2026-03-23 | AI分析增强：缠论、箱体/旗形结构、宏观经济、突发事件 |
| v2.1.0 | 2026-03-23 | 资讯与AI分析板块、后端资讯数据库服务 |
| v2.0.0 | 2026-03-19 | 市场概览页面、路由系统、组件拆分重构 |
| v1.2.0 | 2026-03-18 | App.vue 重构，使用新组件和 composables |
| v1.1.0 | 2026-03-18 | 提取业务逻辑到 composables，组件拆分 |
| v1.0.1 | 2026-03-18 | RSI和订单簿拖动点修复 |
| v1.0.0 | 2026-03-18 | 初始版本：RSI拆分、动态高度调整、指标配置弹窗、拖拽调整 |