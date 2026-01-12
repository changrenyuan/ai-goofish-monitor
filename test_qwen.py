#!/usr/bin/env python3
"""
测试阿里云通义千问 API 连接
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from openai import AsyncOpenAI

async def test_qwen_api():
    """测试通义千问 API"""
    print("=" * 60)
    print("测试阿里云通义千问 API 连接")
    print("=" * 60)

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model_name = os.getenv("OPENAI_MODEL_NAME")

    print(f"\n配置信息:")
    print(f"  API Key: {api_key[:20]}...")
    print(f"  Base URL: {base_url}")
    print(f"  Model: {model_name}")

    if not all([api_key, base_url, model_name]):
        print("\n❌ 配置不完整")
        return False

    try:
        print(f"\n正在初始化客户端...")
        client = AsyncOpenAI(api_key=api_key, base_url=base_url)

        print(f"正在发送测试请求...")
        response = await client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "你好，请回复'测试成功'"}],
            temperature=0.1,
            max_tokens=100
        )

        print(f"\n✅ API 调用成功!")
        print(f"响应内容: {response.choices[0].message.content}")
        return True

    except Exception as e:
        print(f"\n❌ API 调用失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_qwen_api())
    sys.exit(0 if success else 1)
