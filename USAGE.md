# 使用说明

## 快速开始

### 1. 环境准备

确保已安装 Python 3.9 或更高版本：

```bash
python --version
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API 密钥

创建 `.env` 文件（参考 `.env.example`）：

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 密钥：

```
POLYMARKET_PRIVATE_KEY=your_actual_private_key_here
OPINION_TRADE_API_KEY=your_actual_api_key_here
```

### 4. 配置事件信息

编辑 `config.py` 文件，确保以下配置正确：

```python
# Polymarket 事件
POLYMARKET_EVENT_URL = "https://polymarket.com/event/bitcoin-up-or-down-january-28-10am-et"
POLYMARKET_EVENT_SLUG = "bitcoin-up-or-down-january-28-10am-et"

# Opinion.trade 话题
OPINION_TRADE_TOPIC_ID = "4866"
```

### 5. 运行程序

```bash
python main.py
```

## 重要配置说明

### API 端点配置

**Polymarket API**:
- 当前使用的 API 基地址: `https://clob.polymarket.com`
- 需要根据实际的 Polymarket API 文档调整端点
- 可能需要认证和签名

**Opinion.trade API**:
- 当前使用的 API 基地址: `https://api.opinion.trade`（示例）
- **需要根据 Opinion.trade 的实际 API 文档调整**
- 可能需要不同的认证方式

### 获取 Condition ID

Polymarket 需要 `condition_id` 来获取价格和下单。获取方法：

1. **通过 API**: 调用 `get_market_info()` 从响应中提取
2. **手动查找**: 在 Polymarket 网站上查看事件页面的网络请求
3. **配置文件中**: 如果已知，可以直接在代码中硬编码

### 套利参数调整

在 `config.py` 中调整：

```python
ARBITRAGE_THRESHOLD = 1.0      # 赔率相加小于此值触发
MIN_PROFIT_MARGIN = 0.01       # 最小利润 1%
MAX_POSITION_SIZE = 100.0      # 最大单次交易 $100
POLL_INTERVAL = 1.0            # 每秒检查一次
```

## API 集成注意事项

### Polymarket API

1. **认证**: 可能需要使用私钥签名请求
2. **订单簿**: 需要正确解析订单簿格式获取最佳价格
3. **下单**: 需要实现完整的订单创建流程，包括签名

参考实现示例（需要根据实际API调整）：

```python
def place_order(self, condition_id, outcome, size, price):
    # 1. 构建订单数据
    # 2. 使用私钥签名
    # 3. 发送到 API
    # 4. 处理响应
    pass
```

### Opinion.trade API

1. **API 端点**: 需要查找实际的 API 文档
2. **认证方式**: 可能是 API Key、OAuth 或其他方式
3. **价格格式**: 需要了解价格在 API 响应中的位置

## 测试建议

### 1. 价格获取测试

先测试能否正确获取价格：

```python
from polymarket_client import PolymarketClient
from opinion_trade_client import OpinionTradeClient

poly = PolymarketClient()
opinion = OpinionTradeClient()

# 测试获取价格
poly_price = poly.get_best_price("your_condition_id", "YES")
opinion_price = opinion.get_market_price()

print(f"Polymarket: {poly_price}, Opinion.trade: {opinion_price}")
```

### 2. 套利检测测试

```python
from arbitrage_detector import ArbitrageDetector

detector = ArbitrageDetector()
opportunity = detector.check_arbitrage_opportunity()

if opportunity:
    print(f"发现套利机会: {opportunity}")
else:
    print("暂无套利机会")
```

### 3. 小额测试

在实际交易前：
- 使用最小金额测试（如 $1）
- 确认两个平台的订单都能正确执行
- 验证利润计算是否正确

## 常见问题

### Q: 无法获取价格？

**A**: 
1. 检查 API 密钥是否正确
2. 确认 API 端点是否正确
3. 查看日志文件了解详细错误信息
4. 可能需要调整 API 调用方式

### Q: 检测到套利机会但下单失败？

**A**:
1. 检查账户余额是否充足
2. 确认 API 权限是否包含交易功能
3. 检查网络连接
4. 查看错误日志

### Q: 如何获取 Polymarket 的 condition_id？

**A**:
1. 打开浏览器开发者工具
2. 访问事件页面
3. 查看网络请求，找到包含市场数据的 API 调用
4. 从响应中提取 `conditionId` 或 `token_id`

## 安全建议

1. **保护私钥**: 永远不要将 `.env` 文件提交到版本控制
2. **使用测试环境**: 先在测试环境验证功能
3. **设置限额**: 使用 `MAX_POSITION_SIZE` 限制单次交易金额
4. **监控日志**: 定期检查日志文件，及时发现异常
5. **资金管理**: 不要投入超过你能承受损失的资金

## 下一步

1. 完善 API 集成（根据实际 API 文档）
2. 添加错误处理和重试机制
3. 实现订单状态跟踪
4. 添加通知功能（邮件、Telegram 等）
5. 优化执行速度，减少延迟
