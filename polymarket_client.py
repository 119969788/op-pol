"""
Polymarket API 客户端
"""
import requests
import logging
from typing import Optional, Dict
from config import POLYMARKET_API_BASE, POLYMARKET_EVENT_SLUG
from utils import extract_polymarket_event_id

logger = logging.getLogger(__name__)


class PolymarketClient:
    """Polymarket API 客户端"""
    
    def __init__(self):
        self.base_url = POLYMARKET_API_BASE
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })
    
    def get_market_info(self, event_slug: str = None) -> Optional[Dict]:
        """
        获取市场信息
        
        Args:
            event_slug: 事件标识符（从URL中提取），默认使用配置中的值
            
        Returns:
            市场信息字典，包含价格等
        """
        try:
            event_slug = event_slug or POLYMARKET_EVENT_SLUG
            
            # Polymarket API 端点（需要根据实际API文档调整）
            # 方法1: 通过 slug 获取市场信息
            url = f"{self.base_url}/markets"
            params = {"slug": event_slug}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data
        except Exception as e:
            logger.error(f"获取 Polymarket 市场信息失败: {e}")
            # 如果API端点不同，可能需要尝试其他方法
            logger.debug("尝试备用方法获取市场信息...")
            return None
    
    def get_orderbook(self, condition_id: str) -> Optional[Dict]:
        """
        获取订单簿数据
        
        Args:
            condition_id: 条件ID
            
        Returns:
            订单簿数据
        """
        try:
            url = f"{self.base_url}/book"
            params = {"token_id": condition_id}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logger.error(f"获取 Polymarket 订单簿失败: {e}")
            return None
    
    def get_best_price(self, condition_id: str, outcome: str = "YES") -> Optional[float]:
        """
        获取最佳价格
        
        Args:
            condition_id: 条件ID
            outcome: 结果类型 (YES/NO)
            
        Returns:
            最佳价格（0-1之间）
        """
        try:
            orderbook = self.get_orderbook(condition_id)
            if not orderbook:
                return None
            
            # 解析订单簿获取最佳买入价格
            # 这里需要根据实际的API响应格式调整
            if "bids" in orderbook and orderbook["bids"]:
                # 获取最高出价（买入YES的价格）
                best_bid = orderbook["bids"][0]
                if isinstance(best_bid, list):
                    price = float(best_bid[0])
                else:
                    price = float(best_bid.get("price", 0))
                return price
            
            return None
        except Exception as e:
            logger.error(f"获取 Polymarket 最佳价格失败: {e}")
            return None
    
    def place_order(self, condition_id: str, outcome: str, size: float, price: float) -> bool:
        """
        下单
        
        Args:
            condition_id: 条件ID
            outcome: 结果类型 (YES/NO)
            size: 数量
            price: 价格
            
        Returns:
            是否成功
        """
        try:
            # 这里需要实现实际的订单API调用
            # 通常需要签名和认证
            logger.info(f"Polymarket 下单: {outcome} {size} @ {price}")
            # TODO: 实现实际的API调用
            return True
        except Exception as e:
            logger.error(f"Polymarket 下单失败: {e}")
            return False
