# 快速开始指南

## 🚀 一键安装（Linux 服务器）

```bash
# 下载并运行自动安装脚本
wget https://raw.githubusercontent.com/119969788/op-pol/main/setup.sh
chmod +x setup.sh
./setup.sh
```

## 📝 手动安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/119969788/op-pol.git
cd op-pol
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API 密钥

```bash
cp .env.example .env
vim .env  # 填入你的 API 密钥
chmod 600 .env
```

### 5. 测试连接

```bash
python test_connection.py
```

### 6. 运行程序

**前台运行（测试）**:
```bash
python main.py
```

**后台运行（生产）**:
```bash
# 使用 screen
screen -S bot
source venv/bin/activate && python main.py
# 按 Ctrl+A, D 分离

# 或使用 systemd（推荐）
sudo systemctl start arbitrage-bot
```

## 📖 详细文档

- **完整安装教程**: [INSTALL_SERVER.md](INSTALL_SERVER.md)
- **使用说明**: [USAGE.md](USAGE.md)
- **项目说明**: [README.md](README.md)

## ⚡ 常用命令

```bash
# 查看日志
tail -f arbitrage_bot.log

# 查看状态
ps aux | grep "python main.py"

# 停止程序
sudo systemctl stop arbitrage-bot

# 更新代码
git pull && sudo systemctl restart arbitrage-bot
```
