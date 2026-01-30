"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """配置类"""
    
    # =========================
    # 基本运行参数
    # =========================
    POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "1.0"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # =========================
    # Polymarket 配置
    # =========================
    POLYMARKET_API_BASE = "https://clob.polymarket.com"
    POLYMARKET_EVENT_SLUG = os.getenv("POLYMARKET_EVENT_SLUG", "bitcoin-up-or-down-january-30-7am-et")
    POLYMARKET_CONDITION_ID = os.getenv("POLYMARKET_CONDITION_ID", "")
    POLYMARKET_UP_TOKEN_ID = os.getenv("POLYMARKET_UP_TOKEN_ID", "")
    POLYMARKET_DOWN_TOKEN_ID = os.getenv("POLYMARKET_DOWN_TOKEN_ID", "")
    POLYMARKET_PRIVATE_KEY = os.getenv("POLYMARKET_PRIVATE_KEY", "")
    
    # =========================
    # Opinion.trade 配置
    # =========================
    OPINION_API_BASE = os.getenv("OPINION_API_BASE", "https://proxy.opinion.trade:8443")
    OPINION_API_KEY = os.getenv("OPINION_API_KEY", "")
    OPINION_UP_TOKEN_ID = os.getenv("OPINION_UP_TOKEN_ID", "")
    OPINION_DOWN_TOKEN_ID = os.getenv("OPINION_DOWN_TOKEN_ID", "")
    
    # =========================
    # 套利参数
    # =========================
    ARBITRAGE_MAX_SUM_PRICE = float(os.getenv("ARBITRAGE_MAX_SUM_PRICE", "1.0"))
    ARBITRAGE_ORDER_USDC = float(os.getenv("ARBITRAGE_ORDER_USDC", "10.0"))
    MIN_PROFIT_MARGIN = 0.01  # 最小利润边际（1%）
    
    @classmethod
    def validate(cls):
        """验证必需的配置项"""
        errors = []
        
        if not cls.POLYMARKET_UP_TOKEN_ID:
            errors.append("缺少 POLYMARKET_UP_TOKEN_ID")
        if not cls.POLYMARKET_DOWN_TOKEN_ID:
            errors.append("缺少 POLYMARKET_DOWN_TOKEN_ID")
        if not cls.OPINION_API_KEY:
            errors.append("缺少 OPINION_API_KEY")
        
        if errors:
            raise ValueError("配置验证失败:\n" + "\n".join(f"  - {e}" for e in errors))
        
        return True


# 为了向后兼容，保留旧的直接访问方式
# 但推荐使用 Config 类
POLL_INTERVAL = Config.POLL_INTERVAL
LOG_LEVEL = Config.LOG_LEVEL
POLYMARKET_API_BASE = Config.POLYMARKET_API_BASE
POLYMARKET_EVENT_SLUG = Config.POLYMARKET_EVENT_SLUG
POLYMARKET_CONDITION_ID = Config.POLYMARKET_CONDITION_ID
POLYMARKET_UP_TOKEN_ID = Config.POLYMARKET_UP_TOKEN_ID
POLYMARKET_DOWN_TOKEN_ID = Config.POLYMARKET_DOWN_TOKEN_ID
POLYMARKET_PRIVATE_KEY = Config.POLYMARKET_PRIVATE_KEY
OPINION_API_BASE = Config.OPINION_API_BASE
OPINION_API_KEY = Config.OPINION_API_KEY
OPINION_UP_TOKEN_ID = Config.OPINION_UP_TOKEN_ID
OPINION_DOWN_TOKEN_ID = Config.OPINION_DOWN_TOKEN_ID
ARBITRAGE_MAX_SUM_PRICE = Config.ARBITRAGE_MAX_SUM_PRICE
ARBITRAGE_ORDER_USDC = Config.ARBITRAGE_ORDER_USDC
MIN_PROFIT_MARGIN = Config.MIN_PROFIT_MARGIN

# 向后兼容的旧变量名
ARBITRAGE_THRESHOLD = ARBITRAGE_MAX_SUM_PRICE
MAX_POSITION_SIZE = ARBITRAGE_ORDER_USDC
OPINION_TRADE_API_BASE = OPINION_API_BASE
OPINION_TRADE_API_KEY = OPINION_API_KEY
