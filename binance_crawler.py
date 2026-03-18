#!/usr/bin/env python3
"""
Binance Real-time Data Crawler
获取币安实时市场数据
"""

import requests
import time
import json
from datetime import datetime

# API基础URL
BASE_URL = "https://api.binance.com/api/v3"

def get_ticker_price(symbol="BTCUSDT"):
    """获取单个交易对实时价格"""
    url = f"{BASE_URL}/ticker/price"
    params = {"symbol": symbol}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

def get_all_tickers():
    """获取所有交易对的实时价格"""
    url = f"{BASE_URL}/ticker/price"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

def get_24h_ticker(symbol="BTCUSDT"):
    """获取24小时行情统计"""
    url = f"{BASE_URL}/ticker/24hr"
    params = {"symbol": symbol}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

def get_order_book(symbol="BTCUSDT", limit=20):
    """获取订单簿数据"""
    url = f"{BASE_URL}/depth"
    params = {"symbol": symbol, "limit": limit}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

def get_recent_trades(symbol="BTCUSDT", limit=10):
    """获取最近成交记录"""
    url = f"{BASE_URL}/trades"
    params = {"symbol": symbol, "limit": limit}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

def get_klines(symbol="BTCUSDT", interval="1m", limit=10):
    """获取K线数据"""
    url = f"{BASE_URL}/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

def display_price(ticker):
    """格式化显示价格信息"""
    if ticker:
        symbol = ticker.get("symbol", "N/A")
        price = ticker.get("price", "N/A")
        print(f"交易对: {symbol:12} | 价格: {price:>15} USDT")

def display_24h_ticker(ticker):
    """格式化显示24小时行情"""
    if ticker:
        print(f"\n=== {ticker['symbol']} 24小时行情 ===")
        print(f"当前价格:    {ticker['lastPrice']}")
        print(f"24h涨跌:     {ticker['priceChange']} ({ticker['priceChangePercent']}%)")
        print(f"最高价:      {ticker['highPrice']}")
        print(f"最低价:      {ticker['lowPrice']}")
        print(f"24h成交量:   {ticker['volume']}")
        print(f"24h成交额:   {ticker['quoteVolume']}")

def display_order_book(ob):
    """格式化显示订单簿"""
    if ob:
        print(f"\n=== 订单簿 (前5档) ===")
        print(f"{'价格':<15} | {'数量':<15}")
        print("-" * 33)
        # 卖盘（倒序显示）
        for bid in ob.get("bids", [])[:5]:
            print(f"{bid[0]:<15} | {bid[1]:<15}")
        print("-------------------")
        # 买盘
        for ask in ob.get("asks", [])[:5]:
            print(f"{ask[0]:<15} | {ask[1]:<15}")

def display_klines(klines, symbol="BTCUSDT"):
    """格式化显示K线数据"""
    if klines:
        print(f"\n=== {symbol} K线数据 (最近10根) ===")
        print(f"{'时间':<12} | {'开盘':<12} | {'最高':<12} | {'最低':<12} | {'收盘':<12} | {'成交量':<12}")
        print("-" * 80)
        for k in klines:
            # kline格式: [openTime, open, high, low, close, volume, closeTime, ...]
            dt = datetime.fromtimestamp(k[0] / 1000).strftime("%H:%M:%S")
            print(f"{dt:<12} | {k[1]:<12} | {k[2]:<12} | {k[3]:<12} | {k[4]:<12} | {k[5]:<12}")

def main():
    """主函数 - 演示各种API调用"""
    print("=" * 60)
    print("       币安实时数据爬虫")
    print("=" * 60)

    # 1. 获取BTC实时价格
    print("\n--- BTC/USDT 实时价格 ---")
    btc_price = get_ticker_price("BTCUSDT")
    display_price(btc_price)

    # 2. 获取ETH实时价格
    print("\n--- ETH/USDT 实时价格 ---")
    eth_price = get_ticker_price("ETHUSDT")
    display_price(eth_price)

    # 3. 获取24小时行情
    print("\n")
    ticker_24h = get_24h_ticker("BTCUSDT")
    display_24h_ticker(ticker_24h)

    # 4. 获取订单簿
    order_book = get_order_book("BTCUSDT")
    display_order_book(order_book)

    # 5. 获取K线数据
    klines = get_klines("BTCUSDT", "1m", 10)
    display_klines(klines)

    # 6. 获取最近成交
    print("\n--- 最近成交记录 ---")
    trades = get_recent_trades("BTCUSDT", 5)
    if trades:
        for t in trades:
            print(f"价格: {t['price']:<12} 数量: {t['qty']:<10} 时间: {datetime.fromtimestamp(t['time']/1000).strftime('%H:%M:%S')}")

    print("\n" + "=" * 60)
    print("数据获取完成!")
    print("=" * 60)

def live_price_monitor(symbol="BTCUSDT", interval_seconds=5):
    """实时价格监控"""
    print(f"\n开始监控 {symbol} 价格 (每{interval_seconds}秒刷新, Ctrl+C退出)...\n")
    try:
        while True:
            ticker = get_ticker_price(symbol)
            if ticker:
                now = datetime.now().strftime("%H:%M:%S")
                print(f"[{now}] {symbol}: {ticker['price']} USDT")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n监控已停止")

if __name__ == "__main__":
    # 运行演示
    main()

    # 取消注释以下行以启用实时监控:
    # live_price_monitor("BTCUSDT", 3)