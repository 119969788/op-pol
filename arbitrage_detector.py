"""
套利检测器
"""
import logging
import json
from typing import Optional, Dict, Tuple
from polymarket_client import PolymarketClient
from opinion_trade_client import OpinionTradeClient
from config import ARBITRAGE_THRESHOLD, MIN_PROFIT_MARGIN, POLYMARKET_CONDITION_ID

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
            poly_price_yes = None
            condition_id = None
            
            # 方法1: 使用手动配置的 condition_id（优先级最高）
            if POLYMARKET_CONDITION_ID:
                condition_id = POLYMARKET_CONDITION_ID
                logger.info(f"使用手动配置的 condition_id: {condition_id}")
                poly_price_yes = self.polymarket.get_best_price(condition_id, "YES")
            
            # 方法2: 从市场信息中自动提取 condition_id
            if poly_price_yes is None:
                market_info = self.polymarket.get_market_info()
                
                if market_info:
                    logger.debug(f"市场信息类型: {type(market_info)}")
                    
                    # 尝试从市场信息中提取价格
                    if isinstance(market_info, list) and len(market_info) > 0:
                        market = market_info[0]
                        logger.debug(f"市场信息（列表）第一个元素: {json.dumps(market, indent=2)[:500]}")
                        
                        # 尝试多种可能的键名
                        condition_id = (
                            market.get("conditionId") or 
                            market.get("condition_id") or
                            market.get("token_id") or
                            market.get("tokenId") or
                            market.get("id")
                        )
                        
                        if condition_id:
                            logger.info(f"从市场信息中提取到 condition_id: {condition_id}")
                            poly_price_yes = self.polymarket.get_best_price(condition_id, "YES")
                        else:
                            logger.warning("无法从市场信息中提取 condition_id")
                            logger.debug(f"可用的键: {list(market.keys()) if isinstance(market, dict) else 'N/A'}")
                            
                    elif isinstance(market_info, dict):
                        logger.debug(f"市场信息（字典）: {json.dumps(market_info, indent=2)[:500]}")
                        
                        # 尝试多种可能的键名
                        condition_id = (
                            market_info.get("conditionId") or 
                            market_info.get("condition_id") or
                            market_info.get("token_id") or
                            market_info.get("tokenId") or
                            market_info.get("id")
                        )
                        
                        # 如果顶层没有，尝试从嵌套结构中查找
                        if not condition_id:
                            # 尝试从 outcomes 或其他嵌套结构中查找
                            if "outcomes" in market_info and isinstance(market_info["outcomes"], list):
                                for outcome in market_info["outcomes"]:
                                    if isinstance(outcome, dict):
                                        condition_id = (
                                            outcome.get("conditionId") or 
                                            outcome.get("condition_id") or
                                            outcome.get("token_id")
                                        )
                                        if condition_id:
                                            break
                            
                            # 尝试从 conditions 中查找
                            if not condition_id and "conditions" in market_info:
                                conditions = market_info["conditions"]
                                if isinstance(conditions, list) and len(conditions) > 0:
                                    condition_id = (
                                        conditions[0].get("conditionId") or
                                        conditions[0].get("condition_id") or
                                        conditions[0].get("id")
                                    )
                        
                        if condition_id:
                            logger.info(f"从市场信息中提取到 condition_id: {condition_id}")
                            poly_price_yes = self.polymarket.get_best_price(condition_id, "YES")
                        else:
                            logger.warning("无法从市场信息中提取 condition_id")
                            logger.debug(f"可用的键: {list(market_info.keys())}")
                    else:
                        logger.warning(f"未知的市场信息格式: {type(market_info)}")
                else:
                    logger.warning("无法获取市场信息")
            
            # 如果仍然无法获取价格，提供详细的帮助信息
            if poly_price_yes is None:
                logger.error("=" * 60)
                logger.error("无法获取 Polymarket 价格")
                logger.error("=" * 60)
                logger.error("解决方法:")
                logger.error("1. 手动配置 condition_id:")
                logger.error("   - 在 .env 文件中添加: POLYMARKET_CONDITION_ID=your_condition_id")
                logger.error("   - 或在 config.py 中直接设置")
                logger.error("")
                logger.error("2. 如何获取 condition_id:")
                logger.error("   a) 打开浏览器开发者工具 (F12)")
                logger.error("   b) 访问事件页面: https://polymarket.com/event/...")
                logger.error("   c) 查看 Network 标签页")
                logger.error("   d) 找到包含市场数据的 API 请求")
                logger.error("   e) 在响应中查找 'conditionId' 或 'token_id'")
                logger.error("")
                logger.error("3. 查看调试日志:")
                logger.error("   - 设置 LOG_LEVEL=DEBUG 查看详细 API 响应")
                logger.error("=" * 60)
                return None
            
            poly_price_no = 1.0 - poly_price_yes if poly_price_yes else None
            
            # 获取 Opinion.trade 价格
            opinion_price = self.opinion_trade.get_market_price()
            
            if poly_price_yes is None or opinion_price is None:
                if opinion_price is None:
                    logger.warning("无法获取 Opinion.trade 价格")
                return None
            
            logger.debug(f"价格获取成功 - Poly YES: {poly_price_yes:.4f}, Poly NO: {poly_price_no:.4f}, Opinion: {opinion_price:.4f}")
            
            return {
                "polymarket_yes": poly_price_yes,
                "polymarket_no": poly_price_no,
                "opinion_trade": opinion_price,
                "condition_id": condition_id  # 保存条件ID用于下单
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
