"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Polymarket 配置
POLYMARKET_EVENT_URL = "https://polymarket.com/event/bitcoin-up-or-down-january-28-10am-et"
POLYMARKET_EVENT_SLUG = "bitcoin-up-or-down-january-28-10am-et"  # 从URL中提取
POLYMARKET_API_BASE = "https://clob.polymarket.com"
POLYMARKET_PRIVATE_KEY = os.getenv("POLYMARKET_PRIVATE_KEY", "")

# Opinion.trade 配置
OPINION_TRADE_URL = "https://app.opinion.trade/detail?topicId=4866"
OPINION_TRADE_TOPIC_ID = "4866"
OPINION_TRADE_API_BASE = "https://api.opinion.trade"  # 需要根据实际API调整
OPINION_TRADE_API_KEY = os.getenv("OPINION_TRADE_API_KEY", "")

# 套利参数
ARBITRAGE_THRESHOLD = 1.0  # 赔率相加小于此值时触发套利
MIN_PROFIT_MARGIN = 0.01  # 最小利润边际（1%）
MAX_POSITION_SIZE = 100.0  # 最大单次交易金额（USD）

# 监控参数
POLL_INTERVAL = 1.0  # 轮询间隔（秒）
LOG_LEVEL = "INFO"
