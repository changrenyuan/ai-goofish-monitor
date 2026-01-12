"""
测试 AI API 连接
支持 OpenAI 兼容格式的各种 AI 服务
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from openai import OpenAI
    from src.infrastructure.config.settings import settings
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请先运行: pip install -r requirements.txt")
    sys.exit(1)


def test_api_connection():
    """测试 API 连接"""

    print("=" * 50)
    print("AI API 连接测试")
    print("=" * 50)
    print()

    # 显示配置信息
    print("当前配置:")
    print(f"  API Key: {settings.openai_api_key[:20]}...")
    print(f"  Base URL: {settings.openai_base_url}")
    print(f"  Model: {settings.openai_model_name}")
    print()

    # 检查 API Key 是否配置
    if settings.openai_api_key in ["sk-...", "your-api-key-here", ""]:
        print("❌ 错误: API Key 未配置！")
        print()
        print("请编辑 .env 文件，设置 OPENAI_API_KEY")
        print()
        print("Gemini: 访问 https://aistudio.google.com/app/apikey 获取")
        print("OpenAI: 访问 https://platform.openai.com/api-keys 获取")
        return False

    print("正在测试 API 连接...")
    print()

    try:
        # 创建 OpenAI 客户端
        client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )

        # 发送简单的文本请求
        response = client.chat.completions.create(
            model=settings.openai_model_name,
            messages=[
                {
                    "role": "user",
                    "content": "你好，请用一句话介绍你自己。"
                }
            ],
            max_tokens=100,
        )

        # 获取响应
        message = response.choices[0].message.content

        print("✅ API 连接成功！")
        print()
        print("AI 响应:")
        print(f"  {message}")
        print()

        # 检查是否支持图片
        print("检查多模态支持...")
        print(f"  模型: {settings.openai_model_name}")

        multimodal_models = [
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-vision-preview",
        ]

        if any(model in settings.openai_model_name for model in multimodal_models):
            print("  ✅ 支持图片分析")
        else:
            print("  ⚠️  不支持图片分析（本项目需要此功能）")

        print()
        print("=" * 50)
        print("测试完成！API 配置正常。")
        print("=" * 50)
        print()
        print("下一步:")
        print("  1. 运行 start.bat 启动服务")
        print("  2. 访问 http://localhost:5000")
        print("  3. 登录: admin / admin123")

        return True

    except Exception as e:
        print(f"❌ API 连接失败！")
        print()
        print(f"错误信息: {e}")
        print()
        print("可能的原因:")
        print("  1. API Key 错误或已失效")
        print("  2. Base URL 配置错误")
        print("  3. 模型名称不正确")
        print("  4. 网络连接问题")
        print()
        print("请检查 .env 文件中的配置。")
        print()
        print("详细配置指南: GEMINI_API_CONFIG.md")

        return False


def test_image_analysis():
    """测试图片分析功能（如果支持）"""

    print()
    print("=" * 50)
    print("图片分析测试（可选）")
    print("=" * 50)
    print()

    try:
        from openai import OpenAI
        from src.infrastructure.config.settings import settings

        client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )

        # 测试图片 URL（使用一个简单的示例图片）
        test_image_url = "https://via.placeholder.com/100"

        response = client.chat.completions.create(
            model=settings.openai_model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "这张图片是什么？"},
                        {
                            "type": "image_url",
                            "image_url": {"url": test_image_url},
                        },
                    ],
                }
            ],
            max_tokens=50,
        )

        print("✅ 图片分析测试成功！")
        print(f"  AI 响应: {response.choices[0].message.content}")
        print()
        print("图片分析功能正常，可以用于商品图片分析。")

        return True

    except Exception as e:
        print(f"⚠️  图片分析测试失败（这可能正常）")
        print(f"  错误: {e}")
        print()
        print("如果您的模型不支持图片分析，请更换支持多模态的模型。")
        return False


if __name__ == "__main__":
    # 测试基本连接
    success = test_api_connection()

    if success:
        # 询问是否测试图片分析
        print()
        choice = input("是否测试图片分析功能？(y/N): ").strip().lower()
        if choice == "y":
            test_image_analysis()

    print()
    print("配置指南: GEMINI_API_CONFIG.md")
    print("故障排查: LOCAL_TROUBLESHOOTING.md")
    print()
