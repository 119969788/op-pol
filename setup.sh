#!/bin/bash

# Polymarket & Opinion.trade 套利机器人 - 自动安装脚本
# 适用于 Ubuntu/Debian 系统

set -e  # 遇到错误立即退出

echo "=========================================="
echo "套利机器人自动安装脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为 root 用户
if [ "$EUID" -eq 0 ]; then 
   echo -e "${RED}请不要使用 root 用户运行此脚本${NC}"
   exit 1
fi

# 检查操作系统
echo -e "${YELLOW}[1/8] 检查系统环境...${NC}"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VER=$VERSION_ID
    echo "检测到系统: $OS $VER"
else
    echo -e "${RED}无法检测操作系统${NC}"
    exit 1
fi

# 检查 Python
echo -e "${YELLOW}[2/8] 检查 Python 版本...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "Python 版本: $PYTHON_VERSION"
    
    # 检查版本是否 >= 3.9
    if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
        echo -e "${RED}需要 Python 3.9 或更高版本${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Python 3 未安装，正在安装...${NC}"
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        sudo apt update
        sudo apt install -y python3 python3-pip python3-venv
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        sudo yum install -y python3 python3-pip
    else
        echo -e "${RED}不支持的操作系统，请手动安装 Python 3.9+${NC}"
        exit 1
    fi
fi

# 检查 Git
echo -e "${YELLOW}[3/8] 检查 Git...${NC}"
if ! command -v git &> /dev/null; then
    echo "Git 未安装，正在安装..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        sudo apt install -y git
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        sudo yum install -y git
    fi
else
    echo "Git 已安装"
fi

# 选择安装目录
echo -e "${YELLOW}[4/8] 选择安装目录...${NC}"
INSTALL_DIR="${HOME}/op-pol"
read -p "安装目录 (默认: $INSTALL_DIR): " user_input
if [ ! -z "$user_input" ]; then
    INSTALL_DIR="$user_input"
fi

echo "安装目录: $INSTALL_DIR"

# 克隆或更新项目
echo -e "${YELLOW}[5/8] 获取项目代码...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    echo "目录已存在，更新代码..."
    cd "$INSTALL_DIR"
    git pull || echo "更新失败，继续使用现有代码"
else
    echo "克隆项目..."
    git clone https://github.com/119969788/op-pol.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# 创建虚拟环境
echo -e "${YELLOW}[6/8] 创建 Python 虚拟环境...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}虚拟环境创建成功${NC}"
else
    echo "虚拟环境已存在"
fi

# 激活虚拟环境并安装依赖
echo -e "${YELLOW}[7/8] 安装依赖包...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}依赖安装完成${NC}"

# 配置环境变量
echo -e "${YELLOW}[8/8] 配置环境变量...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}.env 文件已创建${NC}"
        echo -e "${YELLOW}请编辑 .env 文件并填入你的 API 密钥:${NC}"
        echo "  vim $INSTALL_DIR/.env"
        echo "  或"
        echo "  nano $INSTALL_DIR/.env"
    else
        echo -e "${YELLOW}创建 .env 文件...${NC}"
        cat > .env << EOF
# Polymarket 配置
POLYMARKET_PRIVATE_KEY=your_polymarket_private_key_here

# Opinion.trade 配置
OPINION_TRADE_API_KEY=your_opinion_trade_api_key_here
EOF
        chmod 600 .env
        echo -e "${GREEN}.env 文件已创建${NC}"
    fi
else
    echo ".env 文件已存在，跳过"
fi

# 完成
echo ""
echo -e "${GREEN}=========================================="
echo "安装完成！"
echo "==========================================${NC}"
echo ""
echo "项目目录: $INSTALL_DIR"
echo ""
echo "下一步操作:"
echo "1. 编辑 .env 文件，填入 API 密钥:"
echo "   cd $INSTALL_DIR"
echo "   vim .env"
echo ""
echo "2. 测试连接:"
echo "   cd $INSTALL_DIR"
echo "   source venv/bin/activate"
echo "   python test_connection.py"
echo ""
echo "3. 运行程序:"
echo "   cd $INSTALL_DIR"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "4. 后台运行（使用 screen）:"
echo "   screen -S bot"
echo "   cd $INSTALL_DIR && source venv/bin/activate && python main.py"
echo "   # 按 Ctrl+A, D 分离会话"
echo ""
echo "详细文档请查看: INSTALL_SERVER.md"
echo ""
