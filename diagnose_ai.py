#!/usr/bin/env python3
"""
AI 配置诊断脚本
用于检查 AI 客户端配置是否正确
"""
import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure.config.settings import AISettings
from src.infrastructure.external.ai_client import AIClient


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def diagnose():
    """诊断 AI 配置"""
    print_section("AI 配置诊断工具")

    # 1. 检查 .env 文件
    print_section("1. 检查 .env 文件")
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ .env 文件存在: {os.path.abspath(env_file)}")
        # 显示文件大小
        file_size = os.path.getsize(env_file)
        print(f"   文件大小: {file_size} 字节")
    else:
        print(f"❌ .env 文件不存在: {os.path.abspath(env_file)}")
        print("   请创建 .env 文件并配置 AI 相关环境变量")
        return False

    # 2. 加载环境变量
    print_section("2. 加载环境变量")
    load_dotenv(override=True)
    print("✅ 环境变量已加载")

    # 3. 检查关键配置项
    print_section("3. 检查关键配置项")

    # 定义配置检查项
    config_items = [
        ("OPENAI_API_KEY", "API Key"),
        ("OPENAI_BASE_URL", "API 基础 URL"),
        ("OPENAI_MODEL_NAME", "模型名称"),
    ]

    all_valid = True
    for env_name, display_name in config_items:
        value = os.getenv(env_name)
        if value:
            # 检查是否为占位符
            if value in ["your-api-key-here", "your_telegram_bot_token", "sk-..."]:
                print(f"❌ {display_name}: {value} (占位符，未配置)")
                all_valid = False
            elif len(value) < 10:
                print(f"⚠️  {display_name}: {value[:20]}... (长度过短)")
                all_valid = False
            else:
                print(f"✅ {display_name}: {value[:20]}...")
        else:
            print(f"❌ {display_name}: 未设置")
            all_valid = False

    if not all_valid:
        print_section("❌ 配置不完整")
        print("请检查 .env 文件，确保以下配置项正确：")
        print("  1. OPENAI_API_KEY - 你的 API Key（必需）")
        print("  2. OPENAI_BASE_URL - API 基础 URL（必需）")
        print("  3. OPENAI_MODEL_NAME - 模型名称（必需）")
        return False

    # 4. 尝试初始化 AI 设置
    print_section("4. 初始化 AI 设置")
    try:
        ai_settings = AISettings()
        print("✅ AISettings 初始化成功")
    except Exception as e:
        print(f"❌ AISettings 初始化失败: {e}")
        return False

    # 5. 检查配置是否完整
    print_section("5. 检查配置完整性")
    if ai_settings.is_configured():
        print("✅ AI 配置完整")
        print(f"   Base URL: {ai_settings.base_url}")
        print(f"   Model Name: {ai_settings.model_name}")
    else:
        print("❌ AI 配置不完整")
        print(f"   Base URL: {ai_settings.base_url}")
        print(f"   Model Name: {ai_settings.model_name}")
        return False

    # 6. 尝试初始化 AI 客户端
    print_section("6. 初始化 AI 客户端")
    try:
        ai_client = AIClient()
        print("✅ AIClient 初始化成功")
    except Exception as e:
        print(f"❌ AIClient 初始化失败: {e}")
        return False

    # 7. 检查客户端是否可用
    print_section("7. 检查客户端可用性")
    if ai_client.is_available():
        print("✅ AI 客户端可用")
        print(f"   Client: {ai_client.client}")
    else:
        print("❌ AI 客户端不可用")
        print("   可能的原因：")
        print("   1. API Key 无效或过期")
        print("   2. Base URL 配置错误")
        print("   3. 网络连接问题")
        print("   4. 代理配置问题")
        return False

    # 8. 诊断通过
    print_section("✅ 诊断通过")
    print("AI 配置正确，可以正常使用！")
    return True


if __name__ == "__main__":
    try:
        success = diagnose()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 诊断过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
