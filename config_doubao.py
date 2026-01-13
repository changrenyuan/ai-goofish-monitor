#!/usr/bin/env python3
"""
豆包 (Doubao) 模型快速配置工具
"""
import os
import re
from dotenv import load_dotenv, set_key

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def validate_doubao_api_key(api_key: str) -> tuple[bool, str]:
    """验证豆包 API Key 格式"""
    if not api_key or api_key.strip() == "":
        return False, "API Key 不能为空"

    # 豆包 API Key 格式：32位十六进制-8位十六进制
    # 示例：a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6-1a2b3c4d
    pattern = r"^[a-f0-9]{32}-[a-f0-9]{8}$"
    if not re.match(pattern, api_key):
        return False, "格式不正确，应为：32位十六进制-8位十六进制（如：a1b2...6-1a2b3c4d）"

    return True, ""

def configure_doubao():
    """配置豆包模型"""

    print_section("豆包 (Doubao) 模型配置")

    print("\n📖 获取豆包 API Key 步骤：")
    print("  1. 访问火山引擎控制台：https://console.volcengine.com/ark")
    print("  2. 登录或注册账号（支持手机号/微信）")
    print("  3. 进入「API Key 管理」页面")
    print("  4. 点击「创建 API Key」")
    print("  5. 复制生成的 API Key（格式：32位-8位）")

    print("\n💡 豆包模型特点：")
    print("  ✅ 支持图片分析（多模态）")
    print("  ✅ 响应速度快")
    print("  ✅ 价格相对便宜")
    print("  ✅ 免费额度充裕（新用户）")

    print("\n" + "-" * 70)

    # 输入 API Key
    print("\n请输入你的豆包 API Key：")
    api_key = input("API Key: ").strip()

    # 验证 API Key
    is_valid, error_msg = validate_doubao_api_key(api_key)
    if not is_valid:
        print(f"\n❌ API Key {error_msg}")
        print("\n正确格式示例：a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6-1a2b3c4d")
        print("              （32位十六进制 - 8位十六进制）\n")

        choice = input("是否继续使用此 API Key？(y/n): ").strip().lower()
        if choice != 'y':
            print("配置已取消")
            return False

    # 选择模型
    print("\n" + "-" * 70)
    print("豆包可用模型：")
    print("\n  [1] doubao-vision (推荐) ★")
    print("      - 支持图片分析（多模态）")
    print("      - 适合商品图片识别和分析")
    print("      - 价格合理，速度快")
    print("\n  [2] doubao-pro-4k")
    print("      - 纯文本模型")
    print("      - 上下文长度 4k")
    print("      - ⚠️ 不支持图片分析")
    print("\n  [3] doubao-pro-32k")
    print("      - 纯文本模型")
    print("      - 上下文长度 32k")
    print("      - ⚠️ 不支持图片分析")

    model_choice = input("\n请选择模型编号 (默认: 1): ").strip() or "1"

    models = {
        "1": "doubao-vision",
        "2": "doubao-pro-4k",
        "3": "doubao-pro-32k",
    }

    model_name = models.get(model_choice, "doubao-vision")

    if model_choice == "1":
        print(f"\n✅ 已选择 doubao-vision（支持图片分析）")
    else:
        print(f"\n⚠️  已选择 {model_name}（不支持图片分析）")
        print("   提示：闲鱼监控建议使用支持图片的模型")

    # 可选：配置代理
    print("\n" + "-" * 70)
    print("\n🌐 代理配置（可选）")
    print("如果你的网络无法直接访问豆包 API，可以配置代理")
    print("例如：http://127.0.0.1:7890 或 socks5://127.0.0.1:1080")
    proxy_url = input("代理地址（留空则不使用）: ").strip()

    # 更新 .env 文件
    print("\n" + "-" * 70)
    print("正在更新 .env 文件...")

    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"❌ .env 文件不存在: {env_file}")
        print("   请确保在项目根目录下运行此脚本")
        return False

    try:
        # 更新配置
        set_key(env_file, "OPENAI_API_KEY", api_key)
        set_key(env_file, "OPENAI_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3/")
        set_key(env_file, "OPENAI_MODEL_NAME", model_name)

        if proxy_url:
            set_key(env_file, "PROXY_URL", proxy_url)
            print(f"✅ 代理已设置: {proxy_url}")

        # 配置豆包特殊设置
        # 豆包不支持 response_format=json_object
        set_key(env_file, "ENABLE_RESPONSE_FORMAT", "false")
        set_key(env_file, "ENABLE_THINKING", "false")

        print("\n" + "=" * 70)
        print("  ✅ 豆包模型配置成功！")
        print("=" * 70)
        print(f"\n配置信息：")
        print(f"  API Key: {api_key[:8]}...{api_key[-4:]}")
        print(f"  Base URL: https://ark.cn-beijing.volces.com/api/v3/")
        print(f"  模型: {model_name}")
        if proxy_url:
            print(f"  代理: {proxy_url}")

        print("\n📋 后续步骤：")
        print("  1. 运行诊断脚本验证配置：")
        print("     python diagnose_ai.py")
        print("\n  2. 测试单个商品分析：")
        print("     python analyze_single.py <商品链接>")

        print("\n" + "=" * 70)

        return True

    except Exception as e:
        print(f"❌ 更新 .env 文件失败: {e}")
        return False

if __name__ == "__main__":
    try:
        success = configure_doubao()
        if not success:
            exit(1)

        print("\n✨ 配置完成！")
        input("\n按回车键退出...")

    except KeyboardInterrupt:
        print("\n\n⚠️  用户取消配置")
        exit(0)
