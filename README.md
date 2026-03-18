# 币安实时行情 Dashboard

Vue3 + Python Flask 实时行情展示应用

## 项目结构

```
.
├── binance_crawler.py      # Python数据爬虫脚本
├── binance_server.py       # Flask API后端服务
├── binance-dashboard/      # Vue3前端项目
│   ├── src/
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

- ✅ 实时价格展示 (BTC/ETH/BNB/SOL/XRP/ADA/DOGE)
- ✅ 24小时涨跌统计
- ✅ K线走势图 (支持1分/5分/15分/1时/4时/1天)
- ✅ 订单簿深度可视化
- ✅ 最新成交记录
- ✅ 自动刷新 (每5秒)

## 直接使用爬虫脚本

如果只需获取数据，无需启动Web服务:

```bash
python binance_crawler.py
```