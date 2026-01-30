#!/usr/bin/env python3
"""
验证配置和 API 连接
"""
import sys
import requests
from config import Config

def verify_polymarket():
    """验证 Polymarket API"""
    print("=" * 60)
    print("验证 Polymarket API")
    print("=" * 60)
    
    # 检查配置
    if not Config.POLYMARKET_UP_TOKEN_ID:
        print("❌ 缺少 POLYMARKET_UP_TOKEN_ID")
        return False
    
    if not Config.POLYMARKET_DOWN_TOKEN_ID:
        print("❌ 缺少 POLYMARKET_DOWN_TOKEN_ID")
        return False
    
    print(f"✓ UP Token ID: {Config.POLYMARKET_UP_TOKEN_ID}")
    print(f"✓ DOWN Token ID: {Config.POLYMARKET_DOWN_TOKEN_ID}")
    print()
    
    # 测试 UP token 订单簿
    print("测试 UP Token 订单簿...")
    url = f"{Config.POLYMARKET_API_BASE}/book"
    params = {"token_id": Config.POLYMARKET_UP_TOKEN_ID}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "bids" in data and data["bids"]:
                best_price = float(data["bids"][0][0])
                print(f"✓ UP Token 订单簿正常，最佳买入价: {best_price:.4f}")
            else:
                print("⚠ UP Token 订单簿为空（无 bids）")
        elif response.status_code == 404:
            print("❌ UP Token 订单簿不存在 (404)")
            print("   响应: " + response.text[:200])
            return False
        else:
            print(f"❌ UP Token 订单簿请求失败: {response.status_code}")
            print("   响应: " + response.text[:200])
            return False
    except Exception as e:
        print(f"❌ UP Token 订单簿请求异常: {e}")
        return False
    
    print()
    
    # 测试 DOWN token 订单簿
    print("测试 DOWN Token 订单簿...")
    params = {"token_id": Config.POLYMARKET_DOWN_TOKEN_ID}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "bids" in data and data["bids"]:
                best_price = float(data["bids"][0][0])
                print(f"✓ DOWN Token 订单簿正常，最佳买入价: {best_price:.4f}")
            else:
                print("⚠ DOWN Token 订单簿为空（无 bids）")
        elif response.status_code == 404:
            print("❌ DOWN Token 订单簿不存在 (404)")
            print("   响应: " + response.text[:200])
            return False
        else:
            print(f"❌ DOWN Token 订单簿请求失败: {response.status_code}")
            print("   响应: " + response.text[:200])
            return False
    except Exception as e:
        print(f"❌ DOWN Token 订单簿请求异常: {e}")
        return False
    
    print()
    print("✓ Polymarket API 验证通过")
    return True


def verify_opinion():
    """验证 Opinion.trade API"""
    print("=" * 60)
    print("验证 Opinion.trade API")
    print("=" * 60)
    
    # 检查配置
    if not Config.OPINION_API_KEY:
        print("❌ 缺少 OPINION_API_KEY")
        return False
    
    print(f"✓ API Base: {Config.OPINION_API_BASE}")
    print(f"✓ API Key: {Config.OPINION_API_KEY[:10]}...")
    print()
    
    # 测试 API Key
    print("测试 API Key...")
    url = f"{Config.OPINION_API_BASE}/openapi/market"
    params = {"limit": 1}
    headers = {
        "apikey": Config.OPINION_API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✓ API Key 有效，返回数据:")
            print(f"  响应类型: {type(data)}")
            if isinstance(data, dict):
                print(f"  响应键: {list(data.keys())[:10]}")
            elif isinstance(data, list):
                print(f"  响应列表长度: {len(data)}")
            print("✓ Opinion.trade API 验证通过")
            return True
        elif response.status_code == 401:
            print("❌ API Key 无效或没有权限 (401)")
            print("   请检查 OPINION_API_KEY 是否正确")
            return False
        else:
            print(f"❌ API 请求失败: {response.status_code}")
            print("   响应: " + response.text[:500])
            return False
    except Exception as e:
        print(f"❌ API 请求异常: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("配置和 API 验证")
    print("=" * 60)
    print()
    
    # 验证配置
    try:
        Config.validate()
        print("✓ 配置验证通过")
    except ValueError as e:
        print("❌ 配置验证失败:")
        print(str(e))
        print("\n请检查 .env 文件中的配置")
        sys.exit(1)
    
    print()
    
    # 验证 Polymarket
    poly_ok = verify_polymarket()
    print()
    
    # 验证 Opinion.trade
    opinion_ok = verify_opinion()
    print()
    
    # 总结
    print("=" * 60)
    print("验证结果")
    print("=" * 60)
    print(f"Polymarket: {'✓ 通过' if poly_ok else '❌ 失败'}")
    print(f"Opinion.trade: {'✓ 通过' if opinion_ok else '❌ 失败'}")
    print()
    
    if poly_ok and opinion_ok:
        print("🎉 所有验证通过！可以运行主程序了")
        print("\n运行命令:")
        print("  python main.py")
        sys.exit(0)
    else:
        print("❌ 部分验证失败，请检查配置和网络连接")
        sys.exit(1)


if __name__ == "__main__":
    main()
