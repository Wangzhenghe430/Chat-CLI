import tiktoken
import re
import json
from typing import List, Dict

# 配置（可自由修改）
MAX_TOKENS = 4096
ENCODING_NAME = "o200k_base"
DEFAULT_CHAT_FILE = "chat_history.json"

# 初始化编码器（全局一次即可）
encoding = tiktoken.get_encoding(ENCODING_NAME)

def count_tokens(text: str) -> int:
    """计算文本token数（精准）"""
    return len(encoding.encode(text)) if text else 0

def truncate_tokens(chat_history: List[Dict]) -> List[Dict]:
    """
    截断对话历史：保留最新消息，不超过最大token
    """
    total = 0
    new_history = []

    # 倒序遍历 → 保留最新对话
    for msg in reversed(chat_history):
        tokens = count_tokens(msg.get("content", ""))
        if total + tokens > MAX_TOKENS:
            break
        new_history.insert(0, msg)
        total += tokens

    return new_history

def format_code(text: str) -> str:
    """美化终端代码块显示"""
    pattern = r"```(\w*)\n(.*?)```"
    return re.sub(pattern, r"\n[bold blue]【代码块】[/bold blue]\n[green]\1[/green]\n```\1\n\2```\n", 
                  text, flags=re.DOTALL)

def read_file(file_path: str) -> str:
    """读取文件（UTF-8）"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"❌ 文件读取失败：{str(e)}"

def save_chat_history(history: List[Dict], file_path: str = DEFAULT_CHAT_FILE) -> bool:
    """保存对话历史到JSON，返回是否成功"""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ 保存失败：{str(e)}")
        return False