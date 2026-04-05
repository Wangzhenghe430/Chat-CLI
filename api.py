import requests
import os
from dotenv import load_dotenv
from typing import List, Dict


load_dotenv("API.env") 


API_KEY = os.getenv("SF_API_KEY")
if not API_KEY:
    raise ValueError("❌ 错误：未在API.env中找到SF_API_KEY，请检查配置！")

API_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"

DEFAULT_MODEL = "Qwen/Qwen3.5-4B"

class SiliconAPI:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        self.current_model = DEFAULT_MODEL

        self.available_models = [
            "deepseek-ai/DeepSeek-V2-Chat",
            "Qwen/Qwen3.5-4B",
            "PaddlePaddle/PaddleOCR-VL",
            "Pro/MiniMaxAI/MiniMax-M2.5"
        ]

    def get_available_models(self) -> List[str]:
        """获取可用模型列表"""
        return self.available_models

    def set_model(self, model_name: str) -> bool:
        """切换模型，成功返回True，失败返回False"""
        if model_name in self.available_models:
            self.current_model = model_name
            return True
        return False

    def chat(self, chat_history: List[Dict]) -> str:
        """发送对话请求，返回AI回复内容"""
        payload = {
            "model": self.current_model,
            "messages": chat_history,
            "stream": False,
            "temperature": 0.7,
            "max_tokens": 2048
        }

        try:
            response = requests.post(
                API_BASE_URL,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"API请求失败：{str(e)}")