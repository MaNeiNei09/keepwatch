#!/usr/bin/env python3
"""
Binance API Server - 为前端提供数据API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time
import sqlite3
import os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api.binance.com/api/v3"

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'news.db')

# 确保数据目录存在
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ==================== 资讯数据库 ====================

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_news_db():
    """初始化资讯数据库"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 创建资讯表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            source TEXT DEFAULT '',
            url TEXT DEFAULT '',
            tags TEXT DEFAULT '',
            importance INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_type ON news(type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_created ON news(created_at)')

    # 检查是否有数据
    cursor.execute('SELECT COUNT(*) FROM news')
    count = cursor.fetchone()[0]

    if count == 0:
        # 初始化近一个月的模拟资讯数据
        init_sample_news(cursor)

    conn.commit()
    conn.close()

def init_sample_news(cursor):
    """初始化示例资讯数据 - 近一个月的资讯"""
    now = datetime.now()

    # 资讯模板数据
    news_templates = [
        # 政策类
        ("policy", "美联储维持利率不变，暗示年内可能降息", "美联储宣布维持联邦基金利率目标区间不变，鲍威尔表示通胀已取得显著进展，市场预期年内可能开始降息周期。", "美联储,降息,利率", 3),
        ("policy", "香港批准首批现货比特币和以太坊ETF", "香港证监会批准嘉实国际、博时国际等机构发行现货加密货币ETF，标志亚洲市场对加密资产的认可。", "香港,ETF,监管", 3),
        ("policy", "欧盟MiCA法规正式生效，加密行业监管趋严", "欧盟加密资产市场监管法案(MiCA)正式生效，为加密行业提供明确监管框架，要求交易所合规运营。", "欧盟,监管,MiCA", 2),
        ("policy", "新加坡金管局发布稳定币监管框架", "新加坡金融管理局发布新的稳定币监管框架，要求发行方持有相应储备资产并定期审计。", "新加坡,稳定币,监管", 2),
        ("policy", "日本金融厅加强对加密交易所监管", "日本金融厅宣布加强对加密货币交易所的监管力度，要求提高客户资产安全保障措施。", "日本,监管,交易所", 2),
        ("policy", "韩国通过虚拟资产用户保护法", "韩国国会通过虚拟资产用户保护法，旨在保护投资者权益并规范市场行为。", "韩国,监管,法律", 2),
        ("policy", "美国SEC主席发表加密货币监管讲话", "美国SEC主席在公开演讲中表示将继续打击加密市场违规行为，保护投资者利益。", "美国,SEC,监管", 3),
        ("policy", "迪拜推出虚拟资产监管新规", "迪拜虚拟资产监管局发布新监管规定，吸引更多加密企业落户。", "迪拜,监管,VASP", 1),

        # 市场类
        ("market", "比特币ETF连续多日净流入，机构需求强劲", "贝莱德和富达的比特币ETF连续多日录得净流入，显示机构投资者对加密资产的兴趣持续增长。", "ETF,机构,BTC", 3),
        ("market", "比特币突破关键阻力位，市场情绪乐观", "比特币价格突破重要技术阻力位，市场分析师普遍看好后续走势。", "BTC,突破,分析", 2),
        ("market", "以太坊Dencun升级成功，Layer2费用大幅降低", "以太坊完成Dencun升级后，主要Layer2网络的交易费用下降90%以上，提升了用户体验。", "ETH,Layer2,升级", 3),
        ("market", "Solana生态持续繁荣，日交易量创历史新高", "Solana网络日交易量突破新高，生态内Meme币和DeFi项目推动链上活动大幅增长。", "SOL,生态,DeFi", 2),
        ("market", "DeFi总锁仓量突破千亿美元", "去中心化金融协议总锁仓量突破1000亿美元，显示DeFi生态持续发展。", "DeFi,TVL,协议", 2),
        ("market", "NFT市场回暖，蓝筹项目交易量上升", "NFT市场近期出现回暖迹象，CryptoPunks和BAYC等蓝筹项目交易量明显上升。", "NFT,交易,蓝筹", 1),
        ("market", "稳定币总市值突破1500亿美元", "稳定币市场总市值突破1500亿美元，USDT和USDC占据主要市场份额。", "稳定币,USDT,USDC", 2),
        ("market", "加密市场总市值突破2.5万亿美元", "加密货币市场总市值突破2.5万亿美元，多个主流币种创年内新高。", "市值,行情,加密", 2),
        ("market", "机构投资者持续增持比特币", "多家上市公司和投资机构披露增持比特币，显示长期看好加密资产。", "机构,增持,BTC", 2),
        ("market", "以太坊质押率创历史新高", "以太坊质押率突破25%，显示投资者对以太坊生态的长期信心。", "ETH,质押,POS", 1),
        ("market", "Meme币热潮席卷市场", "PEPE、WIF等Meme币价格大幅上涨，引发市场广泛关注和讨论。", "Meme,PEPE,WIF", 2),
        ("market", "比特币减半行情预期升温", "随着比特币减半时间临近，市场对减半行情的预期持续升温。", "BTC,减半,行情", 3),

        # 技术类
        ("tech", "以太坊Layer2生态快速扩张", "Arbitrum和Optimism等Layer2网络生态快速扩张，吸引大量开发者和用户。", "ETH,Layer2,Arbitrum", 2),
        ("tech", "比特币闪电网络节点数创新高", "比特币闪电网络节点数量突破历史新高，支付通道数量持续增长。", "BTC,闪电网络,支付", 1),
        ("tech", "跨链桥技术取得重大进展", "多家跨链协议推出新版本，安全性和效率显著提升。", "跨链,桥,协议", 1),
        ("tech", "零知识证明技术广泛应用", "ZK技术被越来越多项目采用，隐私保护和扩容解决方案不断完善。", "ZK,隐私,技术", 2),
        ("tech", "模块化区块链概念兴起", "模块化区块链架构成为行业热点，Celestia等项目获得关注。", "模块化,区块链,Celestia", 1),
        ("tech", "AI与区块链结合趋势加速", "多个AI+区块链项目获得融资，技术融合趋势日益明显。", "AI,区块链,融合", 2),
        ("tech", "账户抽象标准EIP-4337采用率提升", "以太坊账户抽象标准EIP-4337被更多钱包和DApp采用，用户体验改善。", "ETH,AA,EIP-4337", 1),
        ("tech", "Solana推出新开发者工具", "Solana基金会推出新的开发者工具包，降低开发门槛。", "SOL,开发,工具", 1),
    ]

    # 为每条资讯生成随机日期（近30天内）
    import random
    for i, (news_type, title, summary, tags, importance) in enumerate(news_templates):
        # 随机分布在近30天
        days_ago = random.randint(0, 29)
        hours_ago = random.randint(0, 23)
        created_at = now - timedelta(days=days_ago, hours=hours_ago)

        cursor.execute('''
            INSERT INTO news (type, title, summary, tags, importance, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (news_type, title, summary, tags, importance, created_at, created_at))

    # 添加更多重复的资讯来填充近一个月的数据
    additional_news = []
    for day in range(30):
        date = now - timedelta(days=day)
        # 每天添加2-4条资讯
        daily_count = random.randint(2, 4)
        for _ in range(daily_count):
            template = random.choice(news_templates)
            hours_offset = random.randint(0, 23)
            created_at = date - timedelta(hours=hours_offset)
            additional_news.append((
                template[0],  # type
                f"{template[1]}",  # title
                template[2],  # summary
                template[3],  # tags
                template[4],  # importance
                created_at,
                created_at
            ))

    cursor.executemany('''
        INSERT INTO news (type, title, summary, tags, importance, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', additional_news)

    print(f"已初始化 {len(news_templates) + len(additional_news)} 条资讯数据")

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

# ==================== 资讯 API ====================

@app.route('/api/news', methods=['GET'])
def get_news():
    """获取资讯列表"""
    news_type = request.args.get('type', 'all')
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    days = request.args.get('days', 30, type=int)  # 默认近30天

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 计算日期范围
        start_date = datetime.now() - timedelta(days=days)

        if news_type == 'all':
            cursor.execute('''
                SELECT * FROM news
                WHERE created_at >= ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (start_date.isoformat(), limit, offset))
        else:
            cursor.execute('''
                SELECT * FROM news
                WHERE type = ? AND created_at >= ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (news_type, start_date.isoformat(), limit, offset))

        rows = cursor.fetchall()

        # 获取总数
        if news_type == 'all':
            cursor.execute('SELECT COUNT(*) FROM news WHERE created_at >= ?', (start_date.isoformat(),))
        else:
            cursor.execute('SELECT COUNT(*) FROM news WHERE type = ? AND created_at >= ?', (news_type, start_date.isoformat()))
        total = cursor.fetchone()[0]

        conn.close()

        news_list = []
        for row in rows:
            news_list.append({
                'id': row['id'],
                'type': row['type'],
                'title': row['title'],
                'summary': row['summary'],
                'source': row['source'],
                'url': row['url'],
                'tags': row['tags'].split(',') if row['tags'] else [],
                'importance': row['importance'],
                'time': row['created_at']
            })

        return jsonify({
            'data': news_list,
            'total': total,
            'limit': limit,
            'offset': offset
        })
    except Exception as e:
        return jsonify({'error': str(e), 'data': []})

@app.route('/api/news/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    """获取单条资讯详情"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM news WHERE id = ?', (news_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return jsonify({
                'id': row['id'],
                'type': row['type'],
                'title': row['title'],
                'summary': row['summary'],
                'source': row['source'],
                'url': row['url'],
                'tags': row['tags'].split(',') if row['tags'] else [],
                'importance': row['importance'],
                'time': row['created_at']
            })
        else:
            return jsonify({'error': '资讯不存在'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/news', methods=['POST'])
def add_news():
    """添加资讯"""
    data = request.get_json()

    if not data or not data.get('title') or not data.get('type'):
        return jsonify({'error': '标题和类型不能为空'})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO news (type, title, summary, source, url, tags, importance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('type'),
            data.get('title'),
            data.get('summary', ''),
            data.get('source', ''),
            data.get('url', ''),
            ','.join(data.get('tags', [])) if isinstance(data.get('tags'), list) else data.get('tags', ''),
            data.get('importance', 0)
        ))
        conn.commit()
        news_id = cursor.lastrowid
        conn.close()

        return jsonify({'success': True, 'id': news_id})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/news/<int:news_id>', methods=['PUT'])
def update_news(news_id):
    """更新资讯"""
    data = request.get_json()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 构建更新语句
        update_fields = []
        params = []

        for field in ['type', 'title', 'summary', 'source', 'url', 'tags', 'importance']:
            if field in data:
                if field == 'tags' and isinstance(data[field], list):
                    update_fields.append(f'{field} = ?')
                    params.append(','.join(data[field]))
                else:
                    update_fields.append(f'{field} = ?')
                    params.append(data[field])

        if update_fields:
            update_fields.append('updated_at = ?')
            params.append(datetime.now().isoformat())
            params.append(news_id)

            cursor.execute(f'''
                UPDATE news SET {', '.join(update_fields[:-1])}
                WHERE id = ?
            ''', params)
            conn.commit()

        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    """删除资讯"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM news WHERE id = ?', (news_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/news/stats', methods=['GET'])
def get_news_stats():
    """获取资讯统计"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 按类型统计
        cursor.execute('''
            SELECT type, COUNT(*) as count
            FROM news
            WHERE created_at >= ?
            GROUP BY type
        ''', ((datetime.now() - timedelta(days=30)).isoformat(),))
        type_stats = {row['type']: row['count'] for row in cursor.fetchall()}

        # 总数
        cursor.execute('SELECT COUNT(*) FROM news')
        total = cursor.fetchone()[0]

        # 今日新增
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cursor.execute('SELECT COUNT(*) FROM news WHERE created_at >= ?', (today.isoformat(),))
        today_count = cursor.fetchone()[0]

        conn.close()

        return jsonify({
            'total': total,
            'today': today_count,
            'byType': type_stats
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# ==================== 原有 Binance API ====================

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

@app.route('/api/symbols')
def get_symbols():
    """获取所有USDT交易对列表"""
    data = safe_request(f"{BASE_URL}/exchangeInfo")
    if "error" in data:
        return jsonify(data)

    symbols = []
    for s in data.get("symbols", []):
        if s.get("quoteAsset") == "USDT" and s.get("status") == "TRADING":
            symbols.append({
                "symbol": s.get("symbol"),
                "baseAsset": s.get("baseAsset"),
                "quoteAsset": s.get("quoteAsset"),
                "status": s.get("status")
            })

    return jsonify(symbols)

# ==================== 市场数据 API ====================

@app.route('/api/market/global')
def get_market_global():
    """获取全局市场指标"""
    try:
        tickers = safe_request(f"{BASE_URL}/ticker/24hr")
        if "error" in tickers:
            return jsonify({"error": tickers["error"]})

        usdt_tickers = [t for t in tickers if t.get("symbol", "").endswith("USDT")]
        total_volume = sum(float(t.get("quoteVolume", 0)) for t in usdt_tickers)
        btc_ticker = next((t for t in usdt_tickers if t.get("symbol") == "BTCUSDT"), {})
        eth_ticker = next((t for t in usdt_tickers if t.get("symbol") == "ETHUSDT"), {})

        btc_volume = float(btc_ticker.get("quoteVolume", 0)) if btc_ticker else 0
        eth_volume = float(eth_ticker.get("quoteVolume", 0)) if eth_ticker else 0

        btc_dominance = (btc_volume / total_volume * 100) if total_volume > 0 else 0
        eth_dominance = (eth_volume / total_volume * 100) if total_volume > 0 else 0

        return jsonify({
            "totalMarketCap": total_volume * 100,
            "totalVolume24h": total_volume,
            "btcDominance": round(btc_dominance, 2),
            "ethDominance": round(eth_dominance, 2),
            "activeCryptocurrencies": len(usdt_tickers),
            "marketCapChangePercentage24h": float(btc_ticker.get("priceChangePercent", 0)) if btc_ticker else 0
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/market/gainers')
def get_market_gainers():
    """获取涨幅榜"""
    limit = request.args.get('limit', 10, type=int)
    try:
        tickers = safe_request(f"{BASE_URL}/ticker/24hr")
        if "error" in tickers:
            return jsonify([])

        usdt_tickers = [t for t in tickers if t.get("symbol", "").endswith("USDT") and float(t.get("quoteVolume", 0)) > 1000000]
        sorted_tickers = sorted(usdt_tickers, key=lambda x: float(x.get("priceChangePercent", 0)), reverse=True)

        return jsonify([{
            "symbol": t.get("symbol"),
            "baseAsset": t.get("symbol", "").replace("USDT", ""),
            "price": t.get("lastPrice"),
            "change24h": t.get("priceChangePercent"),
            "volume": t.get("quoteVolume"),
            "marketCap": float(t.get("quoteVolume", 0)) * 10
        } for t in sorted_tickers[:limit]])
    except Exception as e:
        return jsonify([])

@app.route('/api/market/losers')
def get_market_losers():
    """获取跌幅榜"""
    limit = request.args.get('limit', 10, type=int)
    try:
        tickers = safe_request(f"{BASE_URL}/ticker/24hr")
        if "error" in tickers:
            return jsonify([])

        usdt_tickers = [t for t in tickers if t.get("symbol", "").endswith("USDT") and float(t.get("quoteVolume", 0)) > 1000000]
        sorted_tickers = sorted(usdt_tickers, key=lambda x: float(x.get("priceChangePercent", 0)))

        return jsonify([{
            "symbol": t.get("symbol"),
            "baseAsset": t.get("symbol", "").replace("USDT", ""),
            "price": t.get("lastPrice"),
            "change24h": t.get("priceChangePercent"),
            "volume": t.get("quoteVolume"),
            "marketCap": float(t.get("quoteVolume", 0)) * 10
        } for t in sorted_tickers[:limit]])
    except Exception as e:
        return jsonify([])

@app.route('/api/market/trending')
def get_market_trending():
    """获取热门币种"""
    try:
        tickers = safe_request(f"{BASE_URL}/ticker/24hr")
        if "error" in tickers:
            return jsonify([])

        usdt_tickers = [t for t in tickers if t.get("symbol", "").endswith("USDT")]

        trending_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'DOGEUSDT', 'ADAUSDT', 'AVAXUSDT']
        result = []
        for i, symbol in enumerate(trending_symbols):
            t = next((x for x in usdt_tickers if x.get("symbol") == symbol), None)
            if t:
                result.append({
                    "symbol": symbol,
                    "name": symbol.replace("USDT", ""),
                    "rank": i + 1,
                    "price": t.get("lastPrice"),
                    "change24h": t.get("priceChangePercent")
                })

        return jsonify(result)
    except Exception as e:
        return jsonify([])

@app.route('/api/market/heatmap')
def get_market_heatmap():
    """获取市场热力图数据"""
    try:
        tickers = safe_request(f"{BASE_URL}/ticker/24hr")
        if "error" in tickers:
            return jsonify([])

        heatmap_symbols = [
            'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT',
            'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT', 'LINKUSDT', 'MATICUSDT',
            'DOTUSDT', 'LTCUSDT', 'UNIUSDT', 'ATOMUSDT', 'ETCUSDT'
        ]

        result = []
        for symbol in heatmap_symbols:
            t = next((x for x in tickers if x.get("symbol") == symbol), None)
            if t:
                result.append({
                    "symbol": symbol,
                    "baseAsset": symbol.replace("USDT", ""),
                    "marketCap": float(t.get("quoteVolume", 0)) * 100,
                    "change24h": t.get("priceChangePercent")
                })

        return jsonify(result)
    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    print("=" * 50)
    print("  币安数据API服务")
    print("  地址: http://localhost:5001")
    print("=" * 50)

    # 初始化资讯数据库
    print("正在初始化资讯数据库...")
    init_news_db()
    print("资讯数据库初始化完成")

    app.run(host='0.0.0.0', port=5001, debug=True)