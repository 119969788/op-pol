"""
测试脚本 - 用于验证 API 连接和价格获取
"""
import logging
from polymarket_client import PolymarketClient
from opinion_trade_client import OpinionTradeClient
from arbitrage_detector import ArbitrageDetector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_polymarket():
    """测试 Polymarket API 连接"""
    print("\n" + "=" * 60)
    print("测试 Polymarket API")
    print("=" * 60)
    
    client = PolymarketClient()
    
    # 测试获取市场信息
    print("\n1. 获取市场信息...")
    market_info = client.get_market_info()
    if market_info:
        print(f"✓ 成功获取市场信息")
        print(f"  响应类型: {type(market_info)}")
        if isinstance(market_info, dict):
            print(f"  键: {list(market_info.keys())[:5]}...")  # 只显示前5个键
        elif isinstance(market_info, list):
            print(f"  列表长度: {len(market_info)}")
    else:
        print("✗ 无法获取市场信息")
        print("  提示: 可能需要调整 API 端点或认证方式")
    
    # 测试获取价格（需要 condition_id）
    print("\n2. 获取价格...")
    print("  注意: 需要有效的 condition_id 才能获取价格")
    print("  提示: 可以从市场信息中提取 condition_id")


def test_opinion_trade():
    """测试 Opinion.trade API 连接"""
    print("\n" + "=" * 60)
    print("测试 Opinion.trade API")
    print("=" * 60)
    
    client = OpinionTradeClient()
    
    # 测试获取话题信息
    print("\n1. 获取话题信息...")
    topic_info = client.get_topic_info()
    if topic_info:
        print(f"✓ 成功获取话题信息")
        print(f"  响应类型: {type(topic_info)}")
        if isinstance(topic_info, dict):
            print(f"  键: {list(topic_info.keys())[:5]}...")
    else:
        print("✗ 无法获取话题信息")
        print("  提示: 可能需要调整 API 端点或认证方式")
    
    # 测试获取价格
    print("\n2. 获取价格...")
    price = client.get_market_price()
    if price is not None:
        print(f"✓ 成功获取价格: {price:.4f} ({price*100:.2f}%)")
    else:
        print("✗ 无法获取价格")
        print("  提示: 需要根据实际 API 响应格式调整解析逻辑")


def test_arbitrage_detection():
    """测试套利检测"""
    print("\n" + "=" * 60)
    print("测试套利检测")
    print("=" * 60)
    
    detector = ArbitrageDetector()
    
    print("\n检查套利机会...")
    opportunity = detector.check_arbitrage_opportunity()
    
    if opportunity:
        print("✓ 发现套利机会！")
        print(f"  策略: {opportunity['strategy']}")
        print(f"  总成本: ${opportunity['total_cost']:.4f}")
        print(f"  预期利润: ${opportunity['profit']:.4f} ({opportunity['profit_percent']:.2f}%)")
    else:
        print("✗ 未发现套利机会")
        print("  可能原因:")
        print("    - 价格获取失败")
        print("    - 赔率相加 >= 1.0")
        print("    - 利润边际 < 最小阈值")


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("API 连接测试")
    print("=" * 60)
    print("\n此脚本用于测试 API 连接和基本功能")
    print("如果测试失败，请检查:")
    print("  1. API 密钥是否正确配置 (.env 文件)")
    print("  2. API 端点是否正确")
    print("  3. 网络连接是否正常")
    print("  4. API 文档是否已更新")
    
    try:
        # 测试 Polymarket
        test_polymarket()
        
        # 测试 Opinion.trade
        test_opinion_trade()
        
        # 测试套利检测
        test_arbitrage_detection()
        
        print("\n" + "=" * 60)
        print("测试完成")
        print("=" * 60)
        print("\n提示:")
        print("  - 如果 API 测试失败，需要根据实际 API 文档调整代码")
        print("  - 查看日志文件了解详细错误信息")
        print("  - 参考 USAGE.md 了解配置说明")
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}", exc_info=True)
        print(f"\n✗ 测试失败: {e}")
        print("  请查看错误信息并检查配置")


if __name__ == "__main__":
    main()
