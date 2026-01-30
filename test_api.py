#!/usr/bin/env python3
"""
测试 API 连接的脚本
验证 Polymarket 和 Opinion.trade API 是否正常工作
"""
import requests
import sys
from config import (
    POLYMARKET_UP_TOKEN_ID,
    POLYMARKET_DOWN_TOKEN_ID,
    OPINION_API_BASE,
    OPINION_API_KEY,
    Config
)

def test_polymarket_orderbook():
    """测试 Polymarket 订单簿 API"""
    print("=" * 60)
    print("测试 1: Polymarket 订单簿 API")
    print("=" * 60)
    
    if not POLYMARKET_UP_TOKEN_ID:
        print("❌ 缺少 POLYMARKET_UP_TOKEN_ID 配置")
        return False
    
    url = "https://clob.polymarket.com/book"
    params = {"token_id": POLYMARKET_UP_TOKEN_ID}
    
    print(f"请求 URL: {url}")
    print(f"Token ID: {POLYMARKET_UP_TOKEN_ID}")
    print()
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "bids" in data and data["bids"]:
                best_bid = data["bids"][0]
                price = float(best_bid[0]) if isinstance(best_bid, list) else float(best_bid.get("price", 0))
                print(f"✅ 成功获取订单簿")
                print(f"   最佳买入价: {price:.4f} ({price*100:.2f}%)")
                return True
            else:
                print("⚠️  订单簿为空（没有 bids）")
                return False
        elif response.status_code == 404:
            print("❌ 订单簿不存在 (404)")
            print("   响应: No orderbook exists")
            return False
        else:
            print(f"❌ API 请求失败: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def test_opinion_api_key():
    """测试 Opinion.trade API Key"""
    print("\n" + "=" * 60)
    print("测试 2: Opinion.trade API Key")
    print("=" * 60)
    
    if not OPINION_API_KEY:
        print("❌ 缺少 OPINION_API_KEY 配置")
        return False
    
    url = f"{OPINION_API_BASE}/openapi/market"
    params = {"limit": 1}
    headers = {
        "apikey": OPINION_API_KEY,
        "Content-Type": "application/json"
    }
    
    print(f"请求 URL: {url}")
    print(f"API Key: {OPINION_API_KEY[:10]}...")
    print()
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ API Key 有效")
                print(f"   响应类型: {type(data)}")
                if isinstance(data, dict):
                    print(f"   响应键: {list(data.keys())[:5]}")
                elif isinstance(data, list):
                    print(f"   响应列表长度: {len(data)}")
                return True
            except:
                print("⚠️  响应不是有效的 JSON")
                return False
        elif response.status_code == 401:
            print("❌ API Key 无效或没有权限 (401)")
            print("   请检查 OPINION_API_KEY 是否正确")
            return False
        else:
            print(f"❌ API 请求失败: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("API 连接测试")
    print("=" * 60)
    print()
    
    # 验证配置
    try:
        Config.validate()
        print("✅ 配置验证通过")
    except ValueError as e:
        print(f"❌ 配置验证失败:")
        print(f"   {e}")
        print("\n请检查 .env 文件中的配置")
        sys.exit(1)
    
    print()
    
    # 测试 Polymarket
    poly_ok = test_polymarket_orderbook()
    
    # 测试 Opinion.trade
    opinion_ok = test_opinion_api_key()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"Polymarket: {'✅ 正常' if poly_ok else '❌ 失败'}")
    print(f"Opinion.trade: {'✅ 正常' if opinion_ok else '❌ 失败'}")
    print()
    
    if poly_ok and opinion_ok:
        print("🎉 所有测试通过！可以运行主程序了")
        return 0
    else:
        print("⚠️  部分测试失败，请检查配置和网络连接")
        return 1


if __name__ == "__main__":
    sys.exit(main())
