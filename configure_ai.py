#!/usr/bin/env python3
"""
AI 配置工具
用于快速配置 AI API Key 和相关设置
"""
import os
import sys
import re
from dotenv import load_dotenv, set_key

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 预定义的 AI 提供商配置
AI_PROVIDERS = {
    "1": {
        "name": "Google Gemini",
        "api_key_url": "https://aistudio.google.com/app/apikey",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "models": [
            "gemini-2.0-flash-exp (最新，快速，多模态) ★推荐",
            "gemini-2.5-pro (最新Pro版，多模态)",
            "gemini-1.5-pro (稳定，多模态)",
            "gemini-1.5-flash (快速，多模态)",
        ],
        "recommended_model": "gemini-2.0-flash-exp",
        "api_key_pattern": r"^AIza[A-Za-z0-9_-]{35}$",
        "api_key_example": "AIzaSyC5...（以 AIza 开头，长度 39）"
    },
    "2": {
        "name": "OpenAI",
        "api_key_url": "https://platform.openai.com/api-keys",
        "base_url": "https://api.openai.com/v1/",
        "models": [
            "gpt-4o (最新，多模态)",
            "gpt-4o-mini (快速，多模态)",
            "gpt-4-turbo (稳定，多模态)",
        ],
        "recommended_model": "gpt-4o",
        "api_key_pattern": r"^sk-[A-Za-z0-9]{48}$",
        "api_key_example": "sk-proj-...（以 sk-proj- 或 sk- 开头）"
    },
    "3": {
        "name": "DeepSeek",
        "api_key_url": "https://platform.deepseek.com/api_keys",
        "base_url": "https://api.deepseek.com/v1/",
        "models": [
            "deepseek-chat (不支持图片) ❌",
            "deepseek-reasoner (不支持图片) ❌",
        ],
        "recommended_model": "deepseek-chat",
        "api_key_pattern": r"^sk-[a-f0-9]{64}$",
        "api_key_example": "sk-...（以 sk- 开头，64位十六进制）",
        "warning": "注意：DeepSeek 模型不支持图片分析，只能分析文本数据"
    },
    "4": {
        "name": "豆包 (Doubao)",
        "api_key_url": "https://console.volcengine.com/ark",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3/",
        "models": [
            "doubao-pro-4k (文本)",
            "doubao-pro-32k (文本)",
            "doubao-vision (支持图片)",
        ],
        "recommended_model": "doubao-vision",
        "api_key_pattern": r"^[a-f0-9]{32}-[a-f0-9]{8}$",
        "api_key_example": "xxxx-xxxx（32位-8位）"
    },
}


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_menu():
    """打印 AI 提供商选择菜单"""
    print_section("选择 AI 提供商")
    for key, provider in AI_PROVIDERS.items():
        print(f"{key}. {provider['name']}")
        if 'warning' in provider:
            print(f"   ⚠️  {provider['warning']}")
    print("0. 退出")


def validate_api_key(api_key: str, pattern: str) -> tuple[bool, str]:
    """验证 API Key 格式"""
    if not api_key or api_key.strip() == "":
        return False, "API Key 不能为空"

    if not re.match(pattern, api_key):
        return False, f"API Key 格式不正确，应该是："

    return True, ""


def get_user_input(prompt: str, default: str = None, required: bool = True) -> str:
    """获取用户输入"""
    if default:
        prompt = f"{prompt} (默认: {default}): "
    else:
        prompt = f"{prompt}: "

    while True:
        value = input(prompt).strip()

        if not value:
            if default:
                return default
            if not required:
                return ""
            print("⚠️  此项不能为空，请重新输入")
            continue

        return value


def configure_provider(provider_id: str):
    """配置指定的 AI 提供商"""
    provider = AI_PROVIDERS[provider_id]

    print_section(f"配置 {provider['name']}")

    # 显示获取 API Key 的链接
    print(f"\n📖 如何获取 {provider['name']} API Key：")
    print(f"   访问：{provider['api_key_url']}")
    print(f"\n   API Key 格式：{provider['api_key_example']}")
    if 'warning' in provider:
        print(f"\n   ⚠️  {provider['warning']}")

    # 输入 API Key
    print("\n" + "-" * 60)
    api_key = get_user_input("请输入你的 API Key", required=True)

    # 验证 API Key
    is_valid, error_msg = validate_api_key(api_key, provider['api_key_pattern'])
    if not is_valid:
        print(f"\n❌ {error_msg}")
        print(f"   正确格式：{provider['api_key_example']}")
        choice = input("\n是否继续？(y/n): ").strip().lower()
        if choice != 'y':
            print("配置已取消")
            return False

    # 选择模型
    print("\n" + "-" * 60)
    print("可用的模型：")
    for idx, model in enumerate(provider['models'], 1):
        if idx == 1 and "★推荐" in model:
            print(f"  [{idx}] {model}")
        else:
            print(f"  [{idx}] {model}")

    default_idx = 1
    while True:
        model_choice = get_user_input(
            f"请选择模型编号",
            default=str(default_idx),
            required=False
        )

        if not model_choice:
            model_name = provider['models'][0].split()[0]
            break

        try:
            idx = int(model_choice) - 1
            if 0 <= idx < len(provider['models']):
                model_name = provider['models'][idx].split()[0]
                break
            else:
                print(f"⚠️  请输入 1-{len(provider['models'])'} 之间的数字")
        except ValueError:
            print("⚠️  请输入数字")

    # 可选：配置代理
    print("\n" + "-" * 60)
    proxy_url = get_user_input("代理地址 (可选，留空则不使用)", required=False)

    # 更新 .env 文件
    print("\n" + "-" * 60)
    print("正在更新 .env 文件...")

    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"❌ .env 文件不存在: {env_file}")
        return False

    try:
        # 更新配置
        set_key(env_file, "OPENAI_API_KEY", api_key)
        set_key(env_file, "OPENAI_BASE_URL", provider['base_url'])
        set_key(env_file, "OPENAI_MODEL_NAME", model_name)
        if proxy_url:
            set_key(env_file, "PROXY_URL", proxy_url)
        else:
            # 如果代理为空，则删除或注释掉
            lines = []
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("PROXY_URL=") and line.strip() == 'PROXY_URL=""':
                        continue
                    lines.append(line)
            with open(env_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        print(f"✅ .env 文件已更新")

        # 显示配置摘要
        print_section("配置摘要")
        print(f"提供商: {provider['name']}")
        print(f"API Key: {api_key[:20]}...")
        print(f"Base URL: {provider['base_url']}")
        print(f"模型: {model_name}")
        if proxy_url:
            print(f"代理: {proxy_url}")
        else:
            print(f"代理: 未配置")

        print("\n✅ 配置完成！")
        print("   请运行 'python diagnose_ai.py' 验证配置")
        return True

    except Exception as e:
        print(f"❌ 更新 .env 文件失败: {e}")
        return False


def main():
    """主函数"""
    print_section("AI 配置工具")
    print("此工具将帮助你配置 AI API Key")

    while True:
        print_menu()
        choice = input("\n请选择 (0-4): ").strip()

        if choice == "0":
            print("\n退出配置工具")
            return

        if choice in AI_PROVIDERS:
            success = configure_provider(choice)
            if success:
                print("\n是否继续配置其他提供商？(y/n): ", end="")
                continue_choice = input().strip().lower()
                if continue_choice != 'y':
                    break
            else:
                print("\n按回车键继续...")
                input()
        else:
            print("⚠️  无效的选择，请重新输入")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n配置已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 配置过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
