"""
套利执行器
"""
import logging
from typing import Dict, Optional
from polymarket_client import PolymarketClient
from opinion_trade_client import OpinionTradeClient
from config import MAX_POSITION_SIZE
from utils import calculate_position_size

logger = logging.getLogger(__name__)


class ArbitrageExecutor:
    """套利执行器"""
    
    def __init__(self):
        self.polymarket = PolymarketClient()
        self.opinion_trade = OpinionTradeClient()
        self.executed_trades = []
    
    def execute_arbitrage(self, opportunity: Dict, position_size: float = None) -> bool:
        """
        执行套利交易
        
        Args:
            opportunity: 套利机会信息
            position_size: 持仓大小（USD），默认使用配置中的最大值
            
        Returns:
            是否成功执行
        """
        if position_size is None:
            position_size = MAX_POSITION_SIZE
        
        try:
            strategy = opportunity["strategy"]
            poly_side = opportunity["poly_side"]
            opinion_side = opportunity["opinion_side"]
            poly_price = opportunity["poly_price"]
            opinion_price = opportunity["opinion_price"]
            
            logger.info(f"开始执行套利: {strategy}")
            logger.info(f"总成本: ${opportunity['total_cost']:.4f}, 预期利润: ${opportunity['profit']:.4f} ({opportunity['profit_percent']:.2f}%)")
            
            # 计算每个平台的持仓数量
            # 按比例分配投资金额，确保总成本等于总投资
            position_allocation = calculate_position_size(
                position_size, poly_price, opinion_price
            )
            poly_amount = position_allocation["amount1"]
            opinion_amount = position_allocation["amount2"]
            
            # 获取条件ID（如果可用）
            condition_id = opportunity.get("condition_id", "condition_id_here")
            
            # 在 Polymarket 下单
            poly_success = self.polymarket.place_order(
                condition_id=condition_id,
                outcome=poly_side,
                size=poly_amount,
                price=poly_price
            )
            
            if not poly_success:
                logger.error("Polymarket 下单失败，取消交易")
                return False
            
            # 在 Opinion.trade 下单
            opinion_success = self.opinion_trade.place_order(
                topic_id="4866",
                side=opinion_side,
                amount=opinion_amount,
                price=opinion_price
            )
            
            if not opinion_success:
                logger.error("Opinion.trade 下单失败，需要处理已执行的订单")
                # TODO: 实现订单撤销逻辑
                return False
            
            # 记录交易
            trade_record = {
                "strategy": strategy,
                "poly_side": poly_side,
                "opinion_side": opinion_side,
                "poly_price": poly_price,
                "opinion_price": opinion_price,
                "position_size": position_size,
                "expected_profit": opportunity["profit"] * position_size,
                "timestamp": self._get_timestamp()
            }
            
            self.executed_trades.append(trade_record)
            logger.info(f"套利交易执行成功: {trade_record}")
            
            return True
        except Exception as e:
            logger.error(f"执行套利失败: {e}")
            return False
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_execution_history(self) -> list:
        """获取执行历史"""
        return self.executed_trades.copy()
