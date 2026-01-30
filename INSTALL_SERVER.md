# 服务器安装详细教程

本教程将指导你在 Linux 服务器上安装和运行 Polymarket & Opinion.trade 套利机器人。

## 📋 目录

1. [服务器环境要求](#服务器环境要求)
2. [安装 Python 和依赖](#安装-python-和依赖)
3. [克隆项目](#克隆项目)
4. [配置环境](#配置环境)
5. [测试运行](#测试运行)
6. [后台运行](#后台运行)
7. [监控和维护](#监控和维护)
8. [常见问题](#常见问题)

---

## 服务器环境要求

### 系统要求

- **操作系统**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+ / 其他 Linux 发行版
- **Python**: 3.9 或更高版本
- **内存**: 至少 512MB RAM
- **磁盘空间**: 至少 100MB 可用空间
- **网络**: 稳定的互联网连接

### 检查系统信息

```bash
# 检查操作系统版本
cat /etc/os-release

# 检查 Python 版本
python3 --version

# 检查可用内存
free -h

# 检查磁盘空间
df -h
```

---

## 安装 Python 和依赖

### Ubuntu/Debian 系统

```bash
# 更新系统包
sudo apt update
sudo apt upgrade -y

# 安装 Python 3 和 pip
sudo apt install -y python3 python3-pip python3-venv

# 安装 Git（如果还没有）
sudo apt install -y git

# 安装其他可能需要的工具
sudo apt install -y curl wget vim
```

### CentOS/RHEL 系统

```bash
# 更新系统包
sudo yum update -y

# 安装 Python 3 和 pip
sudo yum install -y python3 python3-pip git

# 或者使用 dnf（CentOS 8+）
sudo dnf install -y python3 python3-pip git
```

### 验证安装

```bash
# 检查 Python 版本（应该是 3.9+）
python3 --version

# 检查 pip 版本
pip3 --version

# 检查 Git 版本
git --version
```

---

## 克隆项目

### 方法 1: 使用 HTTPS（推荐）

```bash
# 进入合适的目录（例如 /opt 或 ~）
cd /opt  # 或 cd ~

# 克隆项目
git clone https://github.com/119969788/op-pol.git

# 进入项目目录
cd op-pol
```

### 方法 2: 使用 SSH

```bash
# 如果你配置了 SSH 密钥
git clone git@github.com:119969788/op-pol.git
cd op-pol
```

### 方法 3: 直接下载 ZIP

```bash
# 下载并解压
wget https://github.com/119969788/op-pol/archive/refs/heads/main.zip
unzip main.zip
mv op-pol-main op-pol
cd op-pol
```

---

## 配置环境

### 1. 创建 Python 虚拟环境（推荐）

```bash
# 在项目目录中创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 你会看到命令提示符前面有 (venv) 标识
```

### 2. 安装 Python 依赖

```bash
# 确保虚拟环境已激活
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 验证安装
pip list
```

### 3. 配置环境变量

```bash
# 创建 .env 文件
cp .env.example .env

# 编辑 .env 文件
vim .env
# 或使用 nano
nano .env
```

在 `.env` 文件中填入你的 API 密钥：

```env
# Polymarket 配置
POLYMARKET_PRIVATE_KEY=your_polymarket_private_key_here

# Opinion.trade 配置
OPINION_TRADE_API_KEY=your_opinion_trade_api_key_here
```

**安全提示**: 确保 `.env` 文件权限正确：

```bash
# 设置文件权限，只有所有者可读写
chmod 600 .env
```

### 4. 配置项目参数（可选）

如果需要修改默认配置，编辑 `config.py`：

```bash
vim config.py
```

主要配置项：
- `ARBITRAGE_THRESHOLD`: 套利触发阈值（默认 1.0）
- `MIN_PROFIT_MARGIN`: 最小利润边际（默认 0.01，即 1%）
- `MAX_POSITION_SIZE`: 最大单次交易金额（默认 $100）
- `POLL_INTERVAL`: 轮询间隔（秒，默认 1.0）

---

## 测试运行

### 1. 测试 API 连接

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 运行测试脚本
python test_connection.py
```

如果测试成功，你会看到：
- ✓ Polymarket API 连接成功
- ✓ Opinion.trade API 连接成功
- ✓ 套利检测功能正常

### 2. 手动运行主程序（测试）

```bash
# 在前台运行，观察输出
python main.py
```

按 `Ctrl+C` 停止程序。

如果看到以下输出，说明运行正常：
```
============================================================
套利机器人启动
监控平台: Polymarket & Opinion.trade
轮询间隔: 1.0 秒
============================================================
```

---

## 后台运行

### 方法 1: 使用 nohup（简单）

```bash
# 激活虚拟环境并运行
cd /opt/op-pol  # 或你的项目路径
source venv/bin/activate

# 使用 nohup 在后台运行
nohup python main.py > bot.log 2>&1 &

# 查看进程 ID
echo $!

# 查看日志
tail -f bot.log
```

**停止程序**:
```bash
# 查找进程
ps aux | grep "python main.py"

# 停止进程（替换 PID 为实际进程ID）
kill PID
```

### 方法 2: 使用 screen（推荐）

```bash
# 安装 screen（如果还没有）
sudo apt install -y screen  # Ubuntu/Debian
# 或
sudo yum install -y screen  # CentOS

# 创建新的 screen 会话
screen -S arbitrage_bot

# 在 screen 中运行
cd /opt/op-pol
source venv/bin/activate
python main.py

# 按 Ctrl+A 然后按 D 来分离会话（程序继续运行）

# 重新连接会话
screen -r arbitrage_bot

# 查看所有会话
screen -ls
```

### 方法 3: 使用 tmux（推荐）

```bash
# 安装 tmux（如果还没有）
sudo apt install -y tmux  # Ubuntu/Debian
# 或
sudo yum install -y tmux  # CentOS

# 创建新的 tmux 会话
tmux new -s arbitrage_bot

# 在 tmux 中运行
cd /opt/op-pol
source venv/bin/activate
python main.py

# 按 Ctrl+B 然后按 D 来分离会话

# 重新连接会话
tmux attach -t arbitrage_bot

# 查看所有会话
tmux ls
```

### 方法 4: 使用 systemd 服务（生产环境推荐）

创建 systemd 服务文件：

```bash
sudo vim /etc/systemd/system/arbitrage-bot.service
```

添加以下内容（根据你的实际路径修改）：

```ini
[Unit]
Description=Polymarket & Opinion.trade Arbitrage Bot
After=network.target

[Service]
Type=simple
User=your_username  # 替换为你的用户名
WorkingDirectory=/opt/op-pol  # 替换为你的项目路径
Environment="PATH=/opt/op-pol/venv/bin"  # 虚拟环境路径
ExecStart=/opt/op-pol/venv/bin/python /opt/op-pol/main.py
Restart=always
RestartSec=10
StandardOutput=append:/opt/op-pol/bot.log
StandardError=append:/opt/op-pol/bot_error.log

[Install]
WantedBy=multi-user.target
```

**使用服务**:

```bash
# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start arbitrage-bot

# 设置开机自启
sudo systemctl enable arbitrage-bot

# 查看服务状态
sudo systemctl status arbitrage-bot

# 查看日志
sudo journalctl -u arbitrage-bot -f

# 停止服务
sudo systemctl stop arbitrage-bot

# 重启服务
sudo systemctl restart arbitrage-bot
```

---

## 监控和维护

### 查看日志

```bash
# 查看主日志文件
tail -f arbitrage_bot.log

# 查看最近的日志（最后 100 行）
tail -n 100 arbitrage_bot.log

# 搜索错误日志
grep -i error arbitrage_bot.log

# 查看特定日期的日志
grep "2024-01-28" arbitrage_bot.log
```

### 监控程序状态

```bash
# 检查进程是否运行
ps aux | grep "python main.py"

# 检查系统资源使用
top -p $(pgrep -f "python main.py")

# 检查网络连接
netstat -an | grep ESTABLISHED
```

### 定期维护

```bash
# 1. 更新代码
cd /opt/op-pol
git pull origin main

# 2. 更新依赖（如果有新依赖）
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 3. 重启服务（如果使用 systemd）
sudo systemctl restart arbitrage-bot

# 4. 清理旧日志（可选）
# 保留最近 7 天的日志
find /opt/op-pol -name "*.log" -mtime +7 -delete
```

### 设置日志轮转

创建 logrotate 配置：

```bash
sudo vim /etc/logrotate.d/arbitrage-bot
```

添加内容：

```
/opt/op-pol/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 your_username your_username
}
```

---

## 常见问题

### 问题 1: Python 版本过低

**错误**: `Python 3.9+ is required`

**解决**:
```bash
# Ubuntu/Debian
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.9 python3.9-venv python3.9-pip

# 使用 Python 3.9 创建虚拟环境
python3.9 -m venv venv
```

### 问题 2: 权限被拒绝

**错误**: `Permission denied`

**解决**:
```bash
# 检查文件权限
ls -la

# 给脚本执行权限
chmod +x main.py

# 检查目录权限
chmod 755 /opt/op-pol
```

### 问题 3: 模块未找到

**错误**: `ModuleNotFoundError: No module named 'xxx'`

**解决**:
```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

### 问题 4: API 连接失败

**错误**: `无法获取价格` 或 `API 连接失败`

**解决**:
1. 检查网络连接: `ping api.polymarket.com`
2. 检查防火墙设置
3. 验证 API 密钥是否正确
4. 检查 API 端点是否正确

### 问题 5: 程序意外退出

**解决**:
```bash
# 查看错误日志
tail -n 50 arbitrage_bot.log

# 使用 systemd 自动重启（推荐）
# 或使用 supervisor 等进程管理工具
```

### 问题 6: 内存不足

**解决**:
```bash
# 检查内存使用
free -h

# 如果内存不足，考虑：
# 1. 增加服务器内存
# 2. 减少 POLL_INTERVAL（降低检查频率）
# 3. 优化代码
```

---

## 安全建议

1. **防火墙配置**: 只开放必要的端口
2. **SSH 密钥**: 使用 SSH 密钥而非密码登录
3. **定期更新**: 保持系统和依赖包更新
4. **备份配置**: 定期备份 `.env` 和配置文件
5. **监控日志**: 定期检查日志，发现异常及时处理
6. **限制访问**: 使用非 root 用户运行程序

---

## 快速参考命令

```bash
# 启动（screen）
screen -S bot
source venv/bin/activate && python main.py
# Ctrl+A, D 分离

# 启动（systemd）
sudo systemctl start arbitrage-bot

# 查看日志
tail -f arbitrage_bot.log

# 查看状态
ps aux | grep "python main.py"

# 停止
sudo systemctl stop arbitrage-bot
# 或
kill $(pgrep -f "python main.py")

# 更新代码
git pull && sudo systemctl restart arbitrage-bot
```

---

## 需要帮助？

如果遇到问题：

1. 查看日志文件: `arbitrage_bot.log`
2. 运行测试脚本: `python test_connection.py`
3. 检查配置文件: `config.py` 和 `.env`
4. 查看 GitHub Issues: https://github.com/119969788/op-pol/issues

---

**祝交易顺利！** 🚀
