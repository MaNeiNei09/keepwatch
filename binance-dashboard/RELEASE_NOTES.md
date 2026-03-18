# Release Notes / 版本更新日志

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
| v1.0.1 | 2026-03-18 | RSI和订单簿拖动点修复 |
| v1.0.0 | 2026-03-18 | 初始版本：RSI拆分、动态高度调整、指标配置弹窗、拖拽调整 |