"""
套利检测器
"""
import logging
from typing import Optional, Dict, Tuple
from polymarket_client import PolymarketClient
from opinion_trade_client import OpinionTradeClient
from config import ARBITRAGE_THRESHOLD, MIN_PROFIT_MARGIN

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
            # 获取 Polymarket 市场信息
            market_info = self.polymarket.get_market_info()
            
            # 从市场信息中提取条件ID和价格
            # 注意：这里需要根据实际的API响应格式调整
            poly_price_yes = None
            condition_id = None
            
            if market_info:
                # 尝试从市场信息中提取价格
                # 实际格式可能不同，需要根据API文档调整
                if isinstance(market_info, list) and len(market_info) > 0:
                    market = market_info[0]
                    condition_id = market.get("conditionId") or market.get("token_id")
                    # 获取最佳价格
                    if condition_id:
                        poly_price_yes = self.polymarket.get_best_price(condition_id, "YES")
                elif isinstance(market_info, dict):
                    condition_id = market_info.get("conditionId") or market_info.get("token_id")
                    if condition_id:
                        poly_price_yes = self.polymarket.get_best_price(condition_id, "YES")
            
            # 如果无法从市场信息获取，尝试直接使用订单簿
            if poly_price_yes is None:
                # 这里需要实际的 condition_id，可能需要手动配置或从其他地方获取
                logger.warning("无法从市场信息获取价格，可能需要手动配置 condition_id")
                # 临时方案：返回 None，需要用户配置实际的 condition_id
                return None
            
            poly_price_no = 1.0 - poly_price_yes if poly_price_yes else None
            
            # 获取 Opinion.trade 价格
            opinion_price = self.opinion_trade.get_market_price()
            
            if poly_price_yes is None or opinion_price is None:
                return None
            
            return {
                "polymarket_yes": poly_price_yes,
                "polymarket_no": poly_price_no,
                "opinion_trade": opinion_price,
                "condition_id": condition_id  # 保存条件ID用于下单
            }
        except Exception as e:
            logger.error(f"获取价格失败: {e}")
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
            poly_yes = prices.get("polymarket_yes")
            poly_no = prices.get("polymarket_no")
            opinion = prices.get("opinion_trade")
            
            if not all([poly_yes, poly_no, opinion]):
                return None
            
            # 策略1: Polymarket YES + Opinion.trade NO
            # Opinion.trade NO 价格 = 1 - YES 价格
            strategy1_cost = poly_yes + (1.0 - opinion)
            strategy1_profit = 1.0 - strategy1_cost
            
            # 策略2: Polymarket NO + Opinion.trade YES
            strategy2_cost = poly_no + opinion
            strategy2_profit = 1.0 - strategy2_cost
            
            # 选择最佳策略
            best_strategy = None
            best_profit = 0
            
            if strategy1_cost < ARBITRAGE_THRESHOLD and strategy1_profit >= MIN_PROFIT_MARGIN:
                best_strategy = {
                    "strategy": "Poly_YES + Opinion_NO",
                    "poly_side": "YES",
                    "opinion_side": "NO",
                    "poly_price": poly_yes,
                    "opinion_price": 1.0 - opinion,
                    "total_cost": strategy1_cost,
                    "profit": strategy1_profit,
                    "profit_percent": strategy1_profit * 100,
                    "condition_id": prices.get("condition_id")  # 保存条件ID
                }
                best_profit = strategy1_profit
            
            if strategy2_cost < ARBITRAGE_THRESHOLD and strategy2_profit >= MIN_PROFIT_MARGIN:
                if strategy2_profit > best_profit:
                    best_strategy = {
                        "strategy": "Poly_NO + Opinion_YES",
                        "poly_side": "NO",
                        "opinion_side": "YES",
                        "poly_price": poly_no,
                        "opinion_price": opinion,
                        "total_cost": strategy2_cost,
                        "profit": strategy2_profit,
                        "profit_percent": strategy2_profit * 100,
                        "condition_id": prices.get("condition_id")  # 保存条件ID
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
