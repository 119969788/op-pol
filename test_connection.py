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
            if "data" in market_info and isinstance(market_info["data"], list):
                print(f"  市场数量: {len(market_info['data'])}")
        elif isinstance(market_info, list):
            print(f"  列表长度: {len(market_info)}")
    else:
        print("✗ 无法获取市场信息")
        print("  提示: 可能需要调整 API 端点或认证方式")
    
    # 测试使用 token_id 获取价格
    print("\n2. 测试使用 token_id 获取价格...")
    from config import POLYMARKET_UP_TOKEN_ID, POLYMARKET_DOWN_TOKEN_ID
    
    if POLYMARKET_UP_TOKEN_ID:
        print(f"  测试 UP Token ID: {POLYMARKET_UP_TOKEN_ID[:20]}...")
        up_price = client.get_best_price_from_token_id(POLYMARKET_UP_TOKEN_ID)
        if up_price is not None:
            print(f"  ✓ UP 价格: {up_price:.4f} ({up_price*100:.2f}%)")
        else:
            print(f"  ✗ 无法获取 UP 价格")
    else:
        print("  ⚠ 未配置 POLYMARKET_UP_TOKEN_ID")
    
    if POLYMARKET_DOWN_TOKEN_ID:
        print(f"  测试 DOWN Token ID: {POLYMARKET_DOWN_TOKEN_ID[:20]}...")
        down_price = client.get_best_price_from_token_id(POLYMARKET_DOWN_TOKEN_ID)
        if down_price is not None:
            print(f"  ✓ DOWN 价格: {down_price:.4f} ({down_price*100:.2f}%)")
        else:
            print(f"  ✗ 无法获取 DOWN 价格")
    else:
        print("  ⚠ 未配置 POLYMARKET_DOWN_TOKEN_ID")


def test_opinion_trade():
    """测试 Opinion.trade API 连接"""
    print("\n" + "=" * 60)
    print("测试 Opinion.trade API")
    print("=" * 60)
    
    client = OpinionTradeClient()
    
    # 测试 API Key
    print("\n1. 测试 API Key...")
    if client.test_api_key():
        print("✓ API Key 有效")
    else:
        print("✗ API Key 无效或没有权限")
        print("  提示: 请检查 .env 文件中的 OPINION_API_KEY 配置")
        return
    
    # 测试获取市场价格数据
    print("\n2. 获取市场数据...")
    try:
        import requests
        from config import OPINION_API_BASE, OPINION_API_KEY
        
        url = f"{OPINION_API_BASE}/openapi/market"
        params = {"limit": 5}
        headers = {
            "apikey": OPINION_API_KEY,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 成功获取市场数据")
            print(f"  响应类型: {type(data)}")
            if isinstance(data, dict):
                print(f"  键: {list(data.keys())[:10]}")
                if "data" in data:
                    print(f"  数据条数: {len(data.get('data', []))}")
            elif isinstance(data, list):
                print(f"  数据条数: {len(data)}")
        else:
            print(f"✗ 获取市场数据失败: {response.status_code}")
            print(f"  响应: {response.text[:200]}")
    except Exception as e:
        print(f"✗ 获取市场数据异常: {e}")
    
    # 测试获取价格（如果已实现）
    print("\n3. 获取价格...")
    price = client.get_market_price()
    if price is not None:
        print(f"✓ 成功获取价格: {price:.4f} ({price*100:.2f}%)")
    else:
        print("⚠ 价格获取功能尚未实现")
        print("  提示: 需要根据实际 Opinion.trade API 文档实现价格获取逻辑")


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
