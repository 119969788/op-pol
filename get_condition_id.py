#!/usr/bin/env python3
"""
获取 Polymarket Condition ID 的辅助脚本
"""
import requests
import json
import sys
from config import POLYMARKET_EVENT_SLUG, POLYMARKET_API_BASE

def get_condition_id(event_slug=None):
    """
    获取指定事件的 condition_id
    
    Args:
        event_slug: 事件标识符，默认使用配置中的值
    """
    event_slug = event_slug or POLYMARKET_EVENT_SLUG
    
    print("=" * 60)
    print("获取 Polymarket Condition ID")
    print("=" * 60)
    print(f"事件标识符: {event_slug}")
    print(f"API 地址: {POLYMARKET_API_BASE}")
    print()
    
    try:
        url = f"{POLYMARKET_API_BASE}/markets"
        params = {"slug": event_slug}
        
        print(f"请求 URL: {url}")
        print(f"参数: {params}")
        print()
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"响应状态码: {response.status_code}")
        print()
        
        if response.status_code != 200:
            print(f"❌ API 请求失败: {response.status_code}")
            print(f"响应内容: {response.text[:500]}")
            return None
        
        data = response.json()
        
        print("=" * 60)
        print("完整 API 响应:")
        print("=" * 60)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print()
        
        # 尝试提取 condition_id
        condition_id = None
        
        if isinstance(data, list) and len(data) > 0:
            print("=" * 60)
            print("尝试从列表响应中提取 condition_id...")
            print("=" * 60)
            
            for i, market in enumerate(data):
                print(f"\n市场 #{i+1}:")
                if isinstance(market, dict):
                    # 尝试多种可能的键名
                    possible_keys = ["conditionId", "condition_id", "token_id", "tokenId", "id"]
                    for key in possible_keys:
                        if key in market:
                            value = market[key]
                            print(f"  ✓ 找到 '{key}': {value}")
                            if not condition_id:
                                condition_id = value
                    
                    # 检查 outcomes
                    if "outcomes" in market:
                        print(f"  发现 'outcomes' 字段")
                        outcomes = market["outcomes"]
                        if isinstance(outcomes, list):
                            for j, outcome in enumerate(outcomes):
                                if isinstance(outcome, dict):
                                    for key in possible_keys:
                                        if key in outcome:
                                            value = outcome[key]
                                            print(f"    结果 #{j+1} - '{key}': {value}")
                                            if not condition_id:
                                                condition_id = value
                    
                    # 检查 conditions
                    if "conditions" in market:
                        print(f"  发现 'conditions' 字段")
                        conditions = market["conditions"]
                        if isinstance(conditions, list):
                            for j, cond in enumerate(conditions):
                                if isinstance(cond, dict):
                                    for key in possible_keys:
                                        if key in cond:
                                            value = cond[key]
                                            print(f"    条件 #{j+1} - '{key}': {value}")
                                            if not condition_id:
                                                condition_id = value
                    
                    # 显示所有键
                    print(f"  所有键: {list(market.keys())}")
        
        elif isinstance(data, dict):
            print("=" * 60)
            print("尝试从字典响应中提取 condition_id...")
            print("=" * 60)
            
            possible_keys = ["conditionId", "condition_id", "token_id", "tokenId", "id"]
            for key in possible_keys:
                if key in data:
                    value = data[key]
                    print(f"✓ 找到 '{key}': {value}")
                    if not condition_id:
                        condition_id = value
            
            # 检查嵌套结构
            if "data" in data and isinstance(data["data"], list):
                print("\n检查 'data' 字段...")
                for item in data["data"]:
                    if isinstance(item, dict):
                        for key in possible_keys:
                            if key in item:
                                value = item[key]
                                print(f"  ✓ 找到 '{key}': {value}")
                                if not condition_id:
                                    condition_id = value
            
            print(f"\n所有键: {list(data.keys())}")
        
        print()
        print("=" * 60)
        if condition_id:
            print(f"✅ 成功找到 condition_id: {condition_id}")
            print("=" * 60)
            print()
            print("配置方法:")
            print("1. 在 .env 文件中添加:")
            print(f"   POLYMARKET_CONDITION_ID={condition_id}")
            print()
            print("2. 或在 config.py 中直接设置:")
            print(f"   POLYMARKET_CONDITION_ID = \"{condition_id}\"")
            print()
            return condition_id
        else:
            print("❌ 未能自动提取 condition_id")
            print("=" * 60)
            print()
            print("请查看上面的完整响应，手动查找包含以下格式的字段:")
            print("  - conditionId")
            print("  - condition_id")
            print("  - token_id")
            print("  - tokenId")
            print()
            print("通常 condition_id 是一个以 '0x' 开头的 42 字符十六进制字符串")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return None
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # 可以从命令行参数获取 event_slug
    event_slug = sys.argv[1] if len(sys.argv) > 1 else None
    
    condition_id = get_condition_id(event_slug)
    
    if condition_id:
        sys.exit(0)
    else:
        sys.exit(1)
