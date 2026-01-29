# Polymarket & Opinion.trade 套利机器人

实时检测 Polymarket 和 Opinion.trade 两个平台之间的套利机会，当赔率相加小于1时自动执行买入操作。

## 📌 目标事件

- **Polymarket**: [Bitcoin Up or Down - January 28 10am ET](https://polymarket.com/event/bitcoin-up-or-down-january-28-10am-et)
- **Opinion.trade**: [Topic #4866](https://app.opinion.trade/detail?topicId=4866)

## 🎯 功能特性

- **实时监控**: 持续监控两个平台的价格变化
- **套利检测**: 自动检测赔率相加小于1的套利机会
- **自动执行**: 发现机会后自动在两个平台同时下单
- **风险控制**: 内置最小利润边际和最大持仓限制
- **日志记录**: 完整的交易日志和统计信息

## 📋 套利原理

当两个平台的赔率相加小于1时，存在无风险套利机会：

- **策略1**: Polymarket YES + Opinion.trade NO
- **策略2**: Polymarket NO + Opinion.trade YES

例如：
- Polymarket YES 价格: $0.48
- Opinion.trade YES 价格: $0.50
- 策略1成本: $0.48 + $0.50 = $0.98
- 利润: $1.00 - $0.98 = $0.02 (2%)

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的API密钥：

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

编辑 `.env` 文件：
```
POLYMARKET_PRIVATE_KEY=your_polymarket_private_key
OPINION_TRADE_API_KEY=your_opinion_trade_api_key
```

### 3. 测试连接（推荐）

在运行主程序前，先测试 API 连接：

```bash
python test_connection.py
```

这将帮助你验证：
- API 密钥是否正确
- 能否成功获取价格
- 套利检测是否正常工作

### 4. 配置参数

编辑 `config.py` 文件，设置：
- 事件URL和话题ID（已默认配置）
- 套利阈值（默认1.0）
- 最小利润边际（默认1%）
- 最大持仓大小（默认$100）
- 轮询间隔（默认1秒）

**重要**: 需要根据实际的 API 文档调整 API 端点。

### 5. 运行程序

```bash
python main.py
```

程序将：
- 每秒检查一次价格
- 检测套利机会
- 自动执行买入操作
- 记录所有交易到日志文件

## 📁 项目结构

```
.
├── main.py                 # 主程序入口
├── config.py              # 配置文件
├── polymarket_client.py   # Polymarket API 客户端
├── opinion_trade_client.py # Opinion.trade API 客户端
├── arbitrage_detector.py  # 套利检测逻辑
├── arbitrage_executor.py  # 套利执行器
├── requirements.txt       # Python 依赖
├── .env.example          # 环境变量示例
└── README.md             # 项目说明
```

## ⚙️ 配置说明

### 套利参数

- `ARBITRAGE_THRESHOLD`: 套利触发阈值（默认1.0）
- `MIN_PROFIT_MARGIN`: 最小利润边际（默认0.01，即1%）
- `MAX_POSITION_SIZE`: 最大单次交易金额（默认$100）

### 监控参数

- `POLL_INTERVAL`: 价格轮询间隔（秒，默认1.0）
- `LOG_LEVEL`: 日志级别（DEBUG/INFO/WARNING/ERROR）

## 🔧 API 集成说明

### Polymarket API

需要实现以下功能：
1. 获取市场信息和订单簿
2. 获取最佳买入价格
3. 执行买入订单

**注意**: 当前代码中的 `condition_id` 需要根据实际的事件ID替换。

### Opinion.trade API

需要实现以下功能：
1. 获取话题信息和价格
2. 执行买入订单

**注意**: 需要根据 Opinion.trade 的实际API文档调整接口调用。

## ⚠️ 重要提示

1. **API密钥安全**: 不要将 `.env` 文件提交到版本控制系统
2. **API集成**: 当前代码提供了框架，但需要根据实际的 Polymarket 和 Opinion.trade API 文档完善实现
3. **测试环境**: 建议先在测试环境或小额资金上测试
4. **API限制**: 注意两个平台的API调用频率限制
5. **网络延迟**: 套利机会可能转瞬即逝，需要考虑网络延迟
6. **滑点风险**: 实际执行价格可能与检测时的价格不同
7. **资金管理**: 确保两个平台都有足够的资金余额
8. **Condition ID**: Polymarket 需要 `condition_id` 才能获取价格和下单，需要从市场信息中提取或手动配置

## 📚 相关文档

- [使用说明](USAGE.md) - 详细的配置和使用指南
- [测试脚本](test_connection.py) - API 连接测试工具

## 📊 日志和监控

程序会生成 `arbitrage_bot.log` 日志文件，记录：
- 价格检查记录
- 套利机会发现
- 交易执行结果
- 错误和异常信息

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 许可证

MIT License

## ⚠️ 免责声明

本程序仅供学习和研究使用。使用本程序进行实际交易存在风险，请自行承担所有责任。作者不对任何损失负责。
