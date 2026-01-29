"""
工具函数
"""
import re
from typing import Optional, Dict
from urllib.parse import urlparse, parse_qs


def extract_polymarket_event_id(url: str) -> Optional[str]:
    """
    从 Polymarket URL 中提取事件标识符
    
    Args:
        url: Polymarket 事件URL
        
    Returns:
        事件标识符（slug）
    """
    try:
        # 从 URL 中提取事件 slug
        # 例如: https://polymarket.com/event/bitcoin-up-or-down-january-28-10am-et
        match = re.search(r'/event/([^/?]+)', url)
        if match:
            return match.group(1)
        return None
    except Exception:
        return None


def extract_opinion_trade_topic_id(url: str) -> Optional[str]:
    """
    从 Opinion.trade URL 中提取话题ID
    
    Args:
        url: Opinion.trade 话题URL
        
    Returns:
        话题ID
    """
    try:
        # 从 URL 中提取 topicId
        # 例如: https://app.opinion.trade/detail?topicId=4866
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if 'topicId' in params:
            return params['topicId'][0]
        return None
    except Exception:
        return None


def calculate_position_size(total_investment: float, price1: float, price2: float) -> Dict[str, float]:
    """
    计算两个平台的持仓分配
    
    Args:
        total_investment: 总投资金额
        price1: 平台1的价格
        price2: 平台2的价格
        
    Returns:
        包含两个平台持仓金额的字典
    """
    total_cost = price1 + price2
    if total_cost == 0:
        return {"amount1": 0, "amount2": 0}
    
    # 按比例分配投资金额
    amount1 = total_investment * (price1 / total_cost)
    amount2 = total_investment * (price2 / total_cost)
    
    return {
        "amount1": amount1,
        "amount2": amount2
    }


def format_currency(amount: float, decimals: int = 2) -> str:
    """格式化货币金额"""
    return f"${amount:,.{decimals}f}"


def format_percent(value: float, decimals: int = 2) -> str:
    """格式化百分比"""
    return f"{value * 100:.{decimals}f}%"
