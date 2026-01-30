"""
套利检测器
"""
import logging
import json
from typing import Optional, Dict, Tuple
from polymarket_client import PolymarketClient
from opinion_trade_client import OpinionTradeClient
from config import (
    Config,
    ARBITRAGE_MAX_SUM_PRICE, 
    MIN_PROFIT_MARGIN, 
    POLYMARKET_UP_TOKEN_ID,
    POLYMARKET_DOWN_TOKEN_ID
)

logger = logging.getLogger(__name__)


class ArbitrageDetector:
    """套利机会检测器"""
    
    def __init__(self):
        self.polymarket = PolymarketClient()
        self.opinion_trade = OpinionTradeClient()
    
    def get_prices(self) -> Optional[Dict[str, float]]:
        """
        获取两个平台的价格
        
        Returns:
            包含两个平台价格的字典
        """
        try:
            # 使用配置的 token_id 直接获取价格
            if not POLYMARKET_UP_TOKEN_ID or not POLYMARKET_DOWN_TOKEN_ID:
                logger.error("缺少 POLYMARKET_UP_TOKEN_ID 或 POLYMARKET_DOWN_TOKEN_ID 配置")
                return None
            
            # 获取 Polymarket UP 价格（对应 YES）
            poly_price_up = self.polymarket.get_best_price_from_token_id(POLYMARKET_UP_TOKEN_ID)
            
            # 获取 Polymarket DOWN 价格（对应 NO）
            poly_price_down = self.polymarket.get_best_price_from_token_id(POLYMARKET_DOWN_TOKEN_ID)
            
            if poly_price_up is None:
                logger.warning(f"无法获取 Polymarket UP 价格 (token_id: {POLYMARKET_UP_TOKEN_ID})")
            if poly_price_down is None:
                logger.warning(f"无法获取 Polymarket DOWN 价格 (token_id: {POLYMARKET_DOWN_TOKEN_ID})")
            
            if poly_price_up is None or poly_price_down is None:
                return None
            
            # 获取 Opinion.trade 价格
            opinion_price = self.opinion_trade.get_market_price()
            
            if opinion_price is None:
                logger.warning("无法获取 Opinion.trade 价格")
                return None
            
            logger.debug(f"价格获取成功 - Poly UP: {poly_price_up:.4f}, Poly DOWN: {poly_price_down:.4f}, Opinion: {opinion_price:.4f}")
            
            return {
                "polymarket_up": poly_price_up,
                "polymarket_down": poly_price_down,
                "polymarket_yes": poly_price_up,  # 向后兼容
                "polymarket_no": poly_price_down,  # 向后兼容
                "opinion_trade": opinion_price
            }
        except Exception as e:
            logger.error(f"获取价格失败: {e}", exc_info=True)
            return None
    
    def detect_arbitrage(self, prices: Dict) -> Optional[Dict]:
        """
        检测套利机会
        
        Args:
            prices: 价格字典
            
        Returns:
            套利机会信息，如果没有则返回None
        """
        try:
            poly_up = prices.get("polymarket_up") or prices.get("polymarket_yes")
            poly_down = prices.get("polymarket_down") or prices.get("polymarket_no")
            opinion = prices.get("opinion_trade")
            
            if not all([poly_up, poly_down, opinion]):
                return None
            
            # 策略1: Polymarket UP + Opinion.trade DOWN
            # Opinion.trade DOWN 价格 = 1 - UP 价格
            strategy1_cost = poly_up + (1.0 - opinion)
            strategy1_profit = 1.0 - strategy1_cost
            
            # 策略2: Polymarket DOWN + Opinion.trade UP
            strategy2_cost = poly_down + opinion
            strategy2_profit = 1.0 - strategy2_cost
            
            # 选择最佳策略
            best_strategy = None
            best_profit = 0
            
            if strategy1_cost < ARBITRAGE_MAX_SUM_PRICE and strategy1_profit >= MIN_PROFIT_MARGIN:
                best_strategy = {
                    "strategy": "Poly_UP + Opinion_DOWN",
                    "poly_side": "UP",
                    "poly_token_id": POLYMARKET_UP_TOKEN_ID,
                    "opinion_side": "DOWN",
                    "poly_price": poly_up,
                    "opinion_price": 1.0 - opinion,
                    "total_cost": strategy1_cost,
                    "profit": strategy1_profit,
                    "profit_percent": strategy1_profit * 100
                }
                best_profit = strategy1_profit
            
            if strategy2_cost < ARBITRAGE_MAX_SUM_PRICE and strategy2_profit >= MIN_PROFIT_MARGIN:
                if strategy2_profit > best_profit:
                    best_strategy = {
                        "strategy": "Poly_DOWN + Opinion_UP",
                        "poly_side": "DOWN",
                        "poly_token_id": POLYMARKET_DOWN_TOKEN_ID,
                        "opinion_side": "UP",
                        "poly_price": poly_down,
                        "opinion_price": opinion,
                        "total_cost": strategy2_cost,
                        "profit": strategy2_profit,
                        "profit_percent": strategy2_profit * 100
                    }
            
            return best_strategy
        except Exception as e:
            logger.error(f"套利检测失败: {e}")
            return None
    
    def check_arbitrage_opportunity(self) -> Optional[Dict]:
        """
        检查套利机会（完整流程）
        
        Returns:
            套利机会信息
        """
        prices = self.get_prices()
        if not prices:
            return None
        
        return self.detect_arbitrage(prices)
