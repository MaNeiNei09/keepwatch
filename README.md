# 币安实时行情 Dashboard

Vue3 + Python Flask 实时行情展示应用

## 项目结构

```
.
├── binance_crawler.py      # Python数据爬虫脚本
├── binance_server.py       # Flask API后端服务
├── data/                   # 本地数据库存储
│   └── news.db             # 资讯SQLite数据库
├── binance-dashboard/      # Vue3前端项目
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   │   ├── MarketDashboard.vue    # 市场概览页
│   │   │   └── TradingPairDetail.vue  # 交易对详情页
│   │   ├── layout/         # 布局组件
│   │   │   ├── AppLayout.vue          # 主布局容器
│   │   │   └── AppHeader.vue          # 顶部导航栏
│   │   ├── components/     # Vue组件
│   │   │   ├── cards/      # 卡片组件 (价格、仓位、周期、决策)
│   │   │   ├── charts/     # 图表组件 (K线、MACD、RSI)
│   │   │   ├── common/     # 通用组件
│   │   │   └── market/     # 市场组件 (概览、涨跌榜、热力图、资讯、AI分析)
│   │   ├── composables/    # 组合式API逻辑
│   │   │   ├── useChart.js        # K线图表逻辑
│   │   │   ├── useDecision.js     # 交易决策逻辑
│   │   │   ├── useIndicators.js   # 技术指标计算
│   │   │   ├── useMarketData.js   # 市场数据获取
│   │   │   ├── useMarket.js       # 市场概览逻辑
│   │   │   └── useTrading.js      # 交易逻辑
│   │   ├── router/         # 路由配置
│   │   │   └── index.js
│   │   ├── styles/         # 样式文件
│   │   ├── App.vue         # 主组件
│   │   └── main.js         # 入口文件
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── README.md
```

## 快速启动

### 1. 安装依赖

```bash
# 安装Python依赖
pip install flask flask-cors requests

# 安装Vue前端依赖
cd binance-dashboard
npm install
```

### 2. 启动服务

**终端1 - 启动后端API:**
```bash
python binance_server.py
```

**终端2 - 启动前端:**
```bash
cd binance-dashboard
npm run dev
```

### 3. 访问

打开浏览器访问: http://localhost:3000

## 功能特性

### 市场概览页面 (/)
- 市场概览指标：总市值、24h交易量、BTC主导率、ETH主导率
- 涨幅榜/跌幅榜：展示24h涨跌幅最大的币种
- 市场热力图：按市值大小和涨跌幅显示币种色块
- 热门币种：基于交易量排序的热门币种列表
- **宏观市场分析**
  - 今日重点关注事件（非农数据、美联储讲话等）
  - 宏观经济影响分析（利率政策、美元指数、流动性）
  - 市场概况诊断
  - 突发事件影响分析
  - 今日策略建议
- **资讯板块**
  - 市场资讯：政策/市场/技术分类筛选，近30天本地存储
- 快速访问：一键跳转常用交易对

### 交易对详情页 (/trading/:symbol)
- 实时价格展示 (支持所有USDT交易对)
- 24小时涨跌统计
- K线走势图 (TradingView，支持1分/5分/15分/1时/4时/1天)
- MACD指标（含零线显示）
- RSI指标
- 订单簿深度可视化
- 多周期趋势分析 (5m/15m/30m/1h/4h/1d)
- **AI智能分析**
  - 市场情绪仪表（恐惧贪婪指数，基于RSI和涨跌幅动态计算）
  - 缠论分析（走势方向、中枢位置、买卖点、笔/线段结构）
  - 结构形态分析（箱体震荡、旗形整理）
  - 清算地图分析（多空头清算位置、强度可视化）
  - 宏观经济影响（美联储利率、美元指数、ETF资金流、监管环境）
  - 突发事件监控（重大事件及影响币种）
  - 关键信号提示（看涨/看跌/中性）
  - 操作建议（智能生成）
- 自动刷新 (每5秒)

## 后端 API

### 市场数据
- `GET /api/market/global` - 全局市场指标
- `GET /api/market/gainers` - 涨幅榜
- `GET /api/market/losers` - 跌幅榜
- `GET /api/market/trending` - 热门币种
- `GET /api/market/heatmap` - 热力图数据

### 交易数据
- `GET /api/ticker/<symbol>` - 实时价格
- `GET /api/ticker/24h/<symbol>` - 24小时行情
- `GET /api/orderbook/<symbol>` - 订单簿
- `GET /api/klines/<symbol>` - K线数据
- `GET /api/klines-mtf/<symbol>` - 多周期K线
- `GET /api/symbols` - 交易对列表

### 资讯服务
- `GET /api/news` - 获取资讯列表
- `GET /api/news/<id>` - 获取资讯详情
- `POST /api/news` - 添加资讯
- `PUT /api/news/<id>` - 更新资讯
- `DELETE /api/news/<id>` - 删除资讯
- `GET /api/news/stats` - 资讯统计

## 技术栈

- **前端**: Vue 3 + Vite + vue-router + lightweight-charts
- **后端**: Python Flask + SQLite
- **数据源**: Binance API

## 直接使用爬虫脚本

如果只需获取数据，无需启动Web服务:

```bash
python binance_crawler.py
```

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v2.5.0 | 2026-03-23 | 市场概览宏观分析：今日重点关注、宏观经济影响、突发事件 |
| v2.4.0 | 2026-03-23 | AI分析移至交易对页面，基于当前交易对动态分析 |
| v2.3.0 | 2026-03-23 | MACD零线、清算地图分析 |
| v2.2.0 | 2026-03-23 | AI分析增强：缠论、箱体/旗形结构、宏观经济、突发事件 |
| v2.1.0 | 2026-03-23 | 资讯与AI分析板块、后端资讯数据库服务 |
| v2.0.0 | 2026-03-19 | 市场概览页面、路由系统、组件拆分重构 |
| v1.2.0 | 2026-03-18 | App.vue 重构，使用新组件和 composables |
| v1.1.0 | 2026-03-18 | 提取业务逻辑到 composables，组件拆分 |
| v1.0.0 | 2026-03-18 | 初始版本 |