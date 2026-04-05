RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=============================================${NC}"
echo -e "${YELLOW}🚀 硅基流动终端对话工具 自动化测试脚本启动${NC}"
echo -e "${YELLOW}=============================================${NC}\n"


echo -e "${YELLOW}[1/5] 检查Python环境...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python环境正常：${PYTHON_VERSION}${NC}"
else
    echo -e "${RED}❌ 未找到Python3，请先安装Python3.8+${NC}"
    exit 1
fi

echo -e "\n${YELLOW}[2/5] 检查虚拟环境...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ 虚拟环境已存在${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✅ 虚拟环境已激活${NC}"
else
    echo -e "${YELLOW}⚠️  虚拟环境不存在，正在创建...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✅ 虚拟环境创建并激活成功${NC}"
fi


echo -e "\n${YELLOW}[3/5] 安装项目依赖...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 依赖安装成功${NC}"
    else
        echo -e "${RED}❌ 依赖安装失败${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ 未找到requirements.txt文件${NC}"
    exit 1
fi

# 4. 检查API.env配置
echo -e "\n${YELLOW}[4/5] 检查API配置...${NC}"
if [ -f "API.env" ]; then
    API_KEY=$(grep SF_API_KEY API.env | cut -d'=' -f2)
    if [ -n "$API_KEY" ] && [ "$API_KEY" != "你的硅基流动API密钥" ]; then
        echo -e "${GREEN}✅ API密钥配置正常${NC}"
    else
        echo -e "${YELLOW}⚠️  API.env文件存在，但密钥未配置，请手动填写${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  未找到API.env文件，已自动创建模板${NC}"
    echo "SF_API_KEY=你的硅基流动API密钥" > API.env
fi

echo -e "\n${YELLOW}[5/5] 测试程序启动（仅测试语法，不实际调用API）...${NC}"
python3 -c "from main import cli; print('✅ 主程序语法正常')"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 主程序语法检查通过${NC}"
else
    echo -e "${RED}❌ 主程序语法错误，请检查代码${NC}"
    exit 1
fi

python3 -c "from api import SiliconAPI; print('✅ API模块语法正常')"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ API模块语法检查通过${NC}"
else
    echo -e "${RED}❌ API模块语法错误，请检查代码${NC}"
    exit 1
fi

python3 -c "from utils import count_tokens, truncate_tokens, format_code; print('✅ 工具模块语法正常')"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 工具模块语法检查通过${NC}"
else
    echo -e "${RED}❌ 工具模块语法错误，请检查代码${NC}"
    exit 1
fi


echo -e "\n${GREEN}=============================================${NC}"
echo -e "${GREEN}🎉 所有测试通过！项目可正常运行${NC}"
echo -e "${GREEN}=============================================${NC}"
echo -e "\n${YELLOW}📌 后续操作：${NC}"
echo -e "1. 填写API.env中的硅基流动API密钥"
echo -e "2. 执行命令启动程序：python main.py chat"
echo -e "3. 输入/help查看可用命令\n"