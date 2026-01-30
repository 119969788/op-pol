"""
Polymarket API 客户端
"""
import requests
import logging
import json
from typing import Optional, Dict
from config import (
    POLYMARKET_API_BASE, 
    POLYMARKET_UP_TOKEN_ID, 
    POLYMARKET_DOWN_TOKEN_ID,
    POLYMARKET_EVENT_SLUG
)

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
            
            logger.debug(f"请求 Polymarket API: {url} with params: {params}")
            response = self.session.get(url, params=params, timeout=10)
            
            # 记录响应状态
            logger.debug(f"Polymarket API 响应状态: {response.status_code}")
            
            if response.status_code != 200:
                logger.warning(f"Polymarket API 返回非200状态: {response.status_code}")
                logger.debug(f"响应内容: {response.text[:500]}")
            
            response.raise_for_status()
            
            data = response.json()
            
            # 记录响应结构以便调试
            logger.debug(f"Polymarket API 响应类型: {type(data)}")
            if isinstance(data, dict):
                logger.debug(f"响应键: {list(data.keys())[:10]}")
            elif isinstance(data, list) and len(data) > 0:
                logger.debug(f"响应列表长度: {len(data)}, 第一个元素类型: {type(data[0])}")
                if isinstance(data[0], dict):
                    logger.debug(f"第一个元素键: {list(data[0].keys())[:10]}")
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"获取 Polymarket 市场信息失败 (网络错误): {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.debug(f"错误响应内容: {e.response.text[:500]}")
            return None
        except Exception as e:
            logger.error(f"获取 Polymarket 市场信息失败: {e}", exc_info=True)
            return None
    
    def get_orderbook(self, token_id: str) -> Optional[Dict]:
        """
        获取订单簿数据
        
        Args:
            token_id: Token ID (CLOB token_id)
            
        Returns:
            订单簿数据
        """
        try:
            url = f"{self.base_url}/book"
            params = {"token_id": token_id}
            
            logger.debug(f"获取订单簿: {url}?token_id={token_id}")
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 404:
                logger.warning(f"订单簿不存在 (404): token_id={token_id}")
                return None
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取 Polymarket 订单簿失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.debug(f"错误响应: {e.response.text[:200]}")
            return None
        except Exception as e:
            logger.error(f"获取 Polymarket 订单簿失败: {e}")
            return None
    
    def get_best_price_from_token_id(self, token_id: str) -> Optional[float]:
        """
        从 token_id 获取最佳买入价格
        
        Args:
            token_id: CLOB token_id
            
        Returns:
            最佳买入价格（0-1之间）
        """
        try:
            orderbook = self.get_orderbook(token_id)
            if not orderbook:
                return None
            
            # 解析订单簿获取最佳买入价格（最高出价）
            # Polymarket CLOB API 返回格式: {"bids": [[price, size], ...], "asks": [[price, size], ...]}
            if "bids" in orderbook and orderbook["bids"]:
                # bids 是 [[price, size], ...] 格式，按价格从高到低排序
                best_bid = orderbook["bids"][0]
                if isinstance(best_bid, list) and len(best_bid) > 0:
                    price = float(best_bid[0])
                    logger.debug(f"Token {token_id} 最佳买入价: {price}")
                    return price
                elif isinstance(best_bid, dict):
                    price = float(best_bid.get("price", 0))
                    logger.debug(f"Token {token_id} 最佳买入价: {price}")
                    return price
            
            logger.warning(f"Token {token_id} 订单簿中没有 bids")
            return None
        except Exception as e:
            logger.error(f"获取 Polymarket 最佳价格失败 (token_id={token_id}): {e}")
            return None
    
    def get_best_price(self, condition_id: str, outcome: str = "YES") -> Optional[float]:
        """
        获取最佳价格（兼容旧接口）
        
        Args:
            condition_id: 条件ID 或 token_id
            outcome: 结果类型 (YES/NO/UP/DOWN)
            
        Returns:
            最佳价格（0-1之间）
        """
        # 如果传入的是 token_id，直接使用
        return self.get_best_price_from_token_id(condition_id)
    
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
