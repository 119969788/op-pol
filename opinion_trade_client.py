"""
Opinion.trade API 客户端
"""
import requests
import logging
from typing import Optional, Dict
from config import OPINION_TRADE_API_BASE, OPINION_TRADE_TOPIC_ID

logger = logging.getLogger(__name__)


class OpinionTradeClient:
    """Opinion.trade API 客户端"""
    
    def __init__(self):
        self.base_url = OPINION_TRADE_API_BASE
        self.topic_id = OPINION_TRADE_TOPIC_ID
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })
    
    def get_topic_info(self, topic_id: str = None) -> Optional[Dict]:
        """
        获取话题信息
        
        Args:
            topic_id: 话题ID，默认使用配置中的ID
            
        Returns:
            话题信息字典
        """
        try:
            topic_id = topic_id or self.topic_id
            # Opinion.trade API 端点（需要根据实际API文档调整）
            url = f"{self.base_url}/topics/{topic_id}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logger.error(f"获取 Opinion.trade 话题信息失败: {e}")
            return None
    
    def get_market_price(self, topic_id: str = None) -> Optional[float]:
        """
        获取市场价格
        
        Args:
            topic_id: 话题ID
            
        Returns:
            价格（0-1之间）
        """
        try:
            topic_info = self.get_topic_info(topic_id)
            if not topic_info:
                return None
            
            # 根据实际API响应格式解析价格
            # 这里需要根据 Opinion.trade 的实际API结构调整
            if "price" in topic_info:
                return float(topic_info["price"])
            elif "yesPrice" in topic_info:
                return float(topic_info["yesPrice"])
            elif "probability" in topic_info:
                return float(topic_info["probability"])
            
            return None
        except Exception as e:
            logger.error(f"获取 Opinion.trade 价格失败: {e}")
            return None
    
    def place_order(self, topic_id: str, side: str, amount: float, price: float) -> bool:
        """
        下单
        
        Args:
            topic_id: 话题ID
            side: 方向 (YES/NO)
            amount: 数量
            price: 价格
            
        Returns:
            是否成功
        """
        try:
            logger.info(f"Opinion.trade 下单: {side} {amount} @ {price}")
            # TODO: 实现实际的API调用
            return True
        except Exception as e:
            logger.error(f"Opinion.trade 下单失败: {e}")
            return False
