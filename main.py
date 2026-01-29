"""
主程序 - Polymarket 和 Opinion.trade 套利机器人
"""
import time
import logging
from datetime import datetime
from arbitrage_detector import ArbitrageDetector
from arbitrage_executor import ArbitrageExecutor
from config import POLL_INTERVAL, LOG_LEVEL

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arbitrage_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ArbitrageBot:
    """套利机器人主类"""
    
    def __init__(self):
        self.detector = ArbitrageDetector()
        self.executor = ArbitrageExecutor()
        self.running = False
        self.stats = {
            "checks": 0,
            "opportunities_found": 0,
            "trades_executed": 0,
            "total_profit": 0.0
        }
    
    def start(self):
        """启动机器人"""
        logger.info("=" * 60)
        logger.info("套利机器人启动")
        logger.info("监控平台: Polymarket & Opinion.trade")
        logger.info(f"轮询间隔: {POLL_INTERVAL} 秒")
        logger.info("=" * 60)
        
        self.running = True
        
        try:
            while self.running:
                self._run_cycle()
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            logger.info("收到停止信号，正在关闭...")
            self.stop()
        except Exception as e:
            logger.error(f"运行时错误: {e}", exc_info=True)
            self.stop()
    
    def _run_cycle(self):
        """运行一个检测周期"""
        try:
            self.stats["checks"] += 1
            
            # 检测套利机会
            opportunity = self.detector.check_arbitrage_opportunity()
            
            if opportunity:
                self.stats["opportunities_found"] += 1
                logger.info(f"发现套利机会: {opportunity['strategy']}")
                logger.info(f"  总成本: ${opportunity['total_cost']:.4f}")
                logger.info(f"  预期利润: ${opportunity['profit']:.4f} ({opportunity['profit_percent']:.2f}%)")
                
                # 执行套利
                success = self.executor.execute_arbitrage(opportunity)
                
                if success:
                    self.stats["trades_executed"] += 1
                    profit = opportunity["profit"] * 100  # 假设投资 $100
                    self.stats["total_profit"] += profit
                    logger.info(f"套利交易执行成功！预期利润: ${profit:.2f}")
                else:
                    logger.warning("套利交易执行失败")
            else:
                # 每100次检查打印一次状态
                if self.stats["checks"] % 100 == 0:
                    logger.debug(f"检查中... (已检查 {self.stats['checks']} 次)")
        
        except Exception as e:
            logger.error(f"检测周期错误: {e}", exc_info=True)
    
    def stop(self):
        """停止机器人"""
        self.running = False
        logger.info("=" * 60)
        logger.info("套利机器人停止")
        logger.info(f"统计信息:")
        logger.info(f"  总检查次数: {self.stats['checks']}")
        logger.info(f"  发现机会: {self.stats['opportunities_found']}")
        logger.info(f"  执行交易: {self.stats['trades_executed']}")
        logger.info(f"  总利润: ${self.stats['total_profit']:.2f}")
        logger.info("=" * 60)
    
    def print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("套利机器人统计")
        print("=" * 60)
        for key, value in self.stats.items():
            print(f"{key}: {value}")
        print("=" * 60 + "\n")


def main():
    """主函数"""
    bot = ArbitrageBot()
    
    try:
        bot.start()
    except Exception as e:
        logger.error(f"程序异常退出: {e}", exc_info=True)
    finally:
        bot.print_stats()


if __name__ == "__main__":
    main()
