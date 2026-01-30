# 如何获取 Polymarket Condition ID

如果程序无法自动获取 `condition_id`，你需要手动配置。以下是几种获取方法：

## 方法 1: 使用浏览器开发者工具（推荐）

### 步骤：

1. **打开浏览器开发者工具**
   - Chrome/Edge: 按 `F12` 或 `Ctrl+Shift+I`
   - Firefox: 按 `F12` 或 `Ctrl+Shift+I`

2. **切换到 Network 标签页**
   - 点击 "Network" 或 "网络" 标签

3. **访问 Polymarket 事件页面**
   - 打开你要监控的事件页面，例如：
   - https://polymarket.com/event/bitcoin-up-or-down-january-28-10am-et

4. **筛选 API 请求**
   - 在 Network 标签页的筛选框中输入 `api` 或 `clob`
   - 或者选择 "XHR" 或 "Fetch" 类型

5. **查找市场数据请求**
   - 查找包含市场信息的请求，通常名称包含：
     - `markets`
     - `events`
     - `conditions`
     - `orderbook`

6. **查看响应内容**
   - 点击请求，切换到 "Response" 或 "响应" 标签
   - 查找包含 `conditionId` 或 `token_id` 的字段

7. **复制 condition_id**
   - 找到类似这样的字段：
     ```json
     {
       "conditionId": "0x1234567890abcdef...",
       "token_id": "0x1234567890abcdef...",
       ...
     }
     ```
   - 复制这个值

## 方法 2: 使用 curl 命令

```bash
# 替换 YOUR_EVENT_SLUG 为实际的事件标识符
curl "https://clob.polymarket.com/markets?slug=bitcoin-up-or-down-january-28-10am-et" | jq '.[0].conditionId'

# 如果没有 jq，使用 grep
curl "https://clob.polymarket.com/markets?slug=bitcoin-up-or-down-january-28-10am-et" | grep -o '"conditionId":"[^"]*"' | head -1
```

## 方法 3: 使用 Python 脚本

创建一个临时脚本 `get_condition_id.py`:

```python
import requests
import json

event_slug = "bitcoin-up-or-down-january-28-10am-et"
url = f"https://clob.polymarket.com/markets"
params = {"slug": event_slug}

response = requests.get(url, params=params)
data = response.json()

print("完整响应:")
print(json.dumps(data, indent=2))

# 尝试提取 condition_id
if isinstance(data, list) and len(data) > 0:
    market = data[0]
    condition_id = (
        market.get("conditionId") or 
        market.get("condition_id") or
        market.get("token_id")
    )
    if condition_id:
        print(f"\n找到 condition_id: {condition_id}")
    else:
        print("\n未找到 condition_id，请查看上面的完整响应")
elif isinstance(data, dict):
    condition_id = (
        data.get("conditionId") or 
        data.get("condition_id") or
        data.get("token_id")
    )
    if condition_id:
        print(f"\n找到 condition_id: {condition_id}")
    else:
        print("\n未找到 condition_id，请查看上面的完整响应")
```

运行脚本：
```bash
python get_condition_id.py
```

## 配置 condition_id

获取到 `condition_id` 后，有两种配置方式：

### 方式 1: 在 .env 文件中配置（推荐）

编辑 `.env` 文件：
```env
POLYMARKET_CONDITION_ID=0x1234567890abcdef...
```

### 方式 2: 在 config.py 中直接配置

编辑 `config.py`：
```python
POLYMARKET_CONDITION_ID = "0x1234567890abcdef..."
```

## 验证配置

配置完成后，运行测试脚本验证：

```bash
python test_connection.py
```

或者运行主程序，查看日志中是否成功获取价格。

## 常见问题

### Q: 找不到 condition_id？

**A**: 可能的原因：
1. API 端点或响应格式已更改
2. 事件页面结构不同
3. 需要使用不同的 API 端点

**解决方法**：
1. 设置 `LOG_LEVEL=DEBUG` 查看详细的 API 响应
2. 查看 `arbitrage_bot.log` 日志文件
3. 检查 Polymarket API 文档是否有更新

### Q: condition_id 格式是什么？

**A**: 通常是：
- 以太坊地址格式：`0x` 开头的 42 个字符的十六进制字符串
- 例如：`0x1234567890abcdef1234567890abcdef12345678`

### Q: 需要为每个事件单独配置吗？

**A**: 是的，每个事件都有唯一的 `condition_id`。如果监控多个事件，需要为每个事件配置。

## 调试技巧

如果仍然无法获取，可以：

1. **启用调试日志**：
   ```python
   # 在 config.py 中
   LOG_LEVEL = "DEBUG"
   ```

2. **查看完整 API 响应**：
   程序会在 DEBUG 级别记录完整的 API 响应，查看日志文件了解实际的数据结构。

3. **手动测试 API**：
   使用上面的 Python 脚本或 curl 命令直接测试 API，查看实际返回的数据格式。
