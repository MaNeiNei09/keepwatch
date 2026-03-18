#!/usr/bin/env python3
"""
Binance API Server - 为前端提供数据API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api.binance.com/api/v3"

def safe_request(url, params=None, retries=3):
    """带重试的请求"""
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"请求错误 (尝试 {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(0.5)
    return {"error": "请求失败，请稍后重试"}

@app.route('/api/ticker/<symbol>')
def get_ticker(symbol):
    """获取实时价格"""
    data = safe_request(f"{BASE_URL}/ticker/price", {"symbol": symbol})
    return jsonify(data)

@app.route('/api/ticker/24h/<symbol>')
def get_24h_ticker(symbol):
    """获取24小时行情"""
    data = safe_request(f"{BASE_URL}/ticker/24hr", {"symbol": symbol})
    return jsonify(data)

@app.route('/api/orderbook/<symbol>')
def get_orderbook(symbol):
    """获取订单簿"""
    limit = request.args.get('limit', 20, type=int)
    data = safe_request(f"{BASE_URL}/depth", {"symbol": symbol, "limit": limit})
    return jsonify(data)

@app.route('/api/klines/<symbol>')
def get_klines(symbol):
    """获取K线数据"""
    interval = request.args.get('interval', '1m')
    limit = request.args.get('limit', 50, type=int)
    data = safe_request(f"{BASE_URL}/klines", {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    })
    return jsonify(data)

@app.route('/api/klines-mtf/<symbol>')
def get_klines_mtf(symbol):
    """获取多周期K线数据 (5m, 15m, 30m, 1h, 4h, 1d)"""
    intervals = ['5m', '15m', '30m', '1h', '4h', '1d']
    limit = request.args.get('limit', 50, type=int)
    result = {}

    def fetch_klines(interval):
        data = safe_request(f"{BASE_URL}/klines", {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        })
        return interval, data if data else []

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_klines, interval): interval for interval in intervals}
        for future in as_completed(futures):
            interval, data = future.result()
            result[interval] = data

    return jsonify(result)

@app.route('/api/trades/<symbol>')
def get_trades(symbol):
    """获取最近成交"""
    limit = request.args.get('limit', 20, type=int)
    data = safe_request(f"{BASE_URL}/trades", {"symbol": symbol, "limit": limit})
    return jsonify(data)

@app.route('/api/exchange-info')
def get_exchange_info():
    """获取交易对信息"""
    data = safe_request(f"{BASE_URL}/exchangeInfo")
    return jsonify(data)

if __name__ == '__main__':
    print("=" * 50)
    print("  币安数据API服务")
    print("  地址: http://localhost:5001")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5001, debug=True)