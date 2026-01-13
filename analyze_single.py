#!/usr/bin/env python
"""
单个闲鱼商品链接快速分析工具
使用方法: python analyze_single.py <商品链接> <分析标准文件(可选)>
示例: python analyze_single.py https://www.goofish.com/item/xxx prompts/macbook_criteria.txt
"""
import asyncio
import sys
import os
import json
import argparse
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

from src.config import (
    STATE_FILE,
    DETAIL_API_URL_PATTERN,
    RUN_HEADLESS,
    LOGIN_IS_EDGE,
    IMAGE_SAVE_DIR,
    AI_DEBUG_MODE,
)
from src.utils import (
    safe_get,
    random_sleep,
    log_time,
    get_link_unique_key,
)
from src.ai_handler import (
    download_all_images,
    get_ai_analysis,
    cleanup_task_images,
)
from src.scraper import scrape_user_profile
from src.parsers import (
    parse_user_head_data,
    _parse_user_items_data,
    parse_ratings_data,
    calculate_reputation_from_ratings,
)
from src.infrastructure.external.ai_client import AIClient


def print_section(title):
    """打印分隔线"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


async def analyze_single_link(product_url: str, criteria_file: str = "prompts/macbook_criteria.txt"):
    """分析单个商品链接"""

    # 1. 验证URL格式
    print_section("步骤 1: 验证URL并提取商品ID")
    if "goofish.com" not in product_url:
        print("❌ 错误: 请提供有效的闲鱼商品链接")
        print("   格式示例: https://www.goofish.com/item/i123456789")
        return

    # 提取商品ID
    try:
        item_id = product_url.split("/")[-1].split("?")[0]
        print(f"✅ 商品ID: {item_id}")
    except Exception as e:
        print(f"❌ 错误: 无法从URL提取商品ID: {e}")
        return

    # 2. 检查登录状态文件
    print_section("步骤 2: 检查登录状态")
    if not os.path.exists(STATE_FILE):
        print(f"❌ 错误: 未找到登录状态文件: {STATE_FILE}")
        print(f"   请确保 state/ 目录下有登录状态JSON文件")
        return
    print(f"✅ 登录状态文件: {STATE_FILE}")

    # 3. 加载AI分析标准
    print_section("步骤 3: 加载AI分析标准")
    if not os.path.exists(criteria_file):
        print(f"❌ 错误: 分析标准文件不存在: {criteria_file}")
        print(f"   使用默认: prompts/macbook_criteria.txt")
        criteria_file = "prompts/macbook_criteria.txt"
        if not os.path.exists(criteria_file):
            print(f"❌ 错误: 默认分析标准文件也不存在")
            return

    try:
        with open("prompts/base_prompt.txt", 'r', encoding='utf-8') as f:
            base_prompt = f.read()
        with open(criteria_file, 'r', encoding='utf-8') as f:
            criteria_text = f.read()
        ai_prompt_text = base_prompt.replace("{{CRITERIA_SECTION}}", criteria_text)
        print(f"✅ 分析标准加载成功: {criteria_file}")
        print(f"   Prompt长度: {len(ai_prompt_text)} 字符")
    except Exception as e:
        print(f"❌ 错误: 加载分析标准失败: {e}")
        return

    # 4. 初始化AI客户端
    print_section("步骤 4: 初始化AI客户端")
    ai_client = AIClient()
    if not ai_client.is_available():
        ai_client.refresh()
    if not ai_client.is_available():
        print("❌ 错误: AI客户端未初始化")
        print("   请检查 .env 文件中的 OPENAI_API_KEY 配置")
        return
    print(f"✅ AI客户端已就绪")
    print(f"   模型: {ai_client.settings.model_name}")
    print(f"   API地址: {ai_client.settings.base_url}")

    # 5. 启动浏览器并访问商品页
    print_section("步骤 5: 启动浏览器并获取商品数据")

    launch_args = [
        '--disable-blink-features=AutomationControlled',
        '--disable-dev-shm-usage',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process'
    ]

    launch_kwargs = {"headless": RUN_HEADLESS, "args": launch_args}
    if LOGIN_IS_EDGE:
        launch_kwargs["channel"] = "msedge"
    else:
        launch_kwargs["channel"] = "chrome"

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(**launch_kwargs)

            # 移动端上下文
            context = await browser.new_context(
                storage_state=STATE_FILE,
                user_agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
                viewport={'width': 412, 'height': 915},
                device_scale_factor=2.625,
                is_mobile=True,
                has_touch=True,
                locale='zh-CN',
                timezone_id='Asia/Shanghai',
            )

            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en-US', 'en']});
                window.chrome = {runtime: {}, loadTimes: function() {}, csi: function() {}};
                Object.defineProperty(navigator, 'maxTouchPoints', {get: () => 5});
            """)

            page = await context.new_page()

            # 访问商品页
            print(f"📱 正在访问商品页面: {product_url}")
            try:
                async with page.expect_response(
                    lambda r: DETAIL_API_URL_PATTERN in r.url,
                    timeout=30000
                ) as response_info:
                    await page.goto(product_url, wait_until="domcontentloaded", timeout=60000)
                detail_response = await response_info.value

                if not detail_response.ok:
                    print(f"❌ 错误: 获取商品详情失败，状态码: {detail_response.status}")
                    return

                print(f"✅ 成功获取商品详情API响应")

            except PlaywrightTimeoutError:
                print(f"❌ 错误: 访问商品页面超时")
                return

            # 解析商品详情
            detail_json = await detail_response.json()
            item_do = await safe_get(detail_json, 'data', 'itemDO', default={})
            seller_do = await safe_get(detail_json, 'data', 'sellerDO', default={})

            # 构建商品基础信息
            print_section("步骤 6: 解析商品信息")

            item_data = {
                "商品ID": await safe_get(item_do, 'id', default=item_id),
                "商品标题": await safe_get(item_do, 'title', default="未知标题"),
                "当前售价": await safe_get(item_do, 'priceInfo', 'price', default="未知价格"),
                "商品原价": await safe_get(item_do, 'priceInfo', 'originalPrice', default="未知"),
                ""想要"人数": await safe_get(item_do, 'wantCnt', default='0'),
                "浏览量": await safe_get(item_do, 'browseCnt', default='0'),
                "发货地区": await safe_get(item_do, 'deliveryInfo', 'area', default="未知"),
                "商品链接": product_url,
            }

            # 提取图片列表
            image_infos = await safe_get(item_do, 'imageInfos', default=[])
            if image_infos:
                all_image_urls = [img.get('url') for img in image_infos if img.get('url')]
                item_data['商品图片列表'] = all_image_urls
                item_data['商品主图链接'] = all_image_urls[0] if all_image_urls else ""
                print(f"✅ 商品图片: {len(all_image_urls)} 张")
            else:
                print(f"⚠️  警告: 未找到商品图片")

            # 打印商品基础信息
            print(f"📦 商品标题: {item_data['商品标题']}")
            print(f"💰 当前售价: {item_data['当前售价']}")
            print(f"🎯 想要人数: {item_data['"想要"人数']}")
            print(f"👀 浏览量: {item_data['浏览量']}")
            print(f"📍 发货地区: {item_data['发货地区']}")

            # 采集卖家信息
            print_section("步骤 7: 采集卖家信息")

            seller_id = await safe_get(seller_do, 'sellerId')
            if seller_id:
                print(f"👤 卖家ID: {seller_id}")
                print("🔄 正在采集卖家完整信息...")
                user_profile_data = await scrape_user_profile(context, str(seller_id))

                # 添加额外的卖家信息
                zhima_credit_text = await safe_get(seller_do, 'zhimaLevelInfo', 'levelName')
                user_profile_data['卖家芝麻信用'] = zhima_credit_text

                print(f"✅ 卖家信息采集完成")
                print(f"   卖家昵称: {user_profile_data.get('卖家昵称', '未知')}")
                print(f"   卖家信用: {user_profile_data.get('卖家信用等级', '未知')}")
                print(f"   在售商品: {user_profile_data.get('卖家在售/已售商品数', '未知')}")

                # 统计卖家评价
                rating_list = user_profile_data.get('卖家收到的评价列表', [])
                print(f"   评价数量: {len(rating_list)} 条")
            else:
                print("❌ 错误: 无法获取卖家ID")
                user_profile_data = {}

            # 下载商品图片
            print_section("步骤 8: 下载商品图片")

            image_urls = item_data.get('商品图片列表', [])
            if not image_urls:
                print("⚠️  警告: 无图片可下载，跳过图片下载")
                downloaded_image_paths = []
            else:
                downloaded_image_paths = await download_all_images(
                    item_data['商品ID'],
                    image_urls,
                    task_name="single_analysis"
                )
                print(f"✅ 成功下载 {len(downloaded_image_paths)} 张图片")

            # 构建完整数据
            final_record = {
                "爬取时间": datetime.now().isoformat(),
                "商品信息": item_data,
                "卖家信息": user_profile_data
            }

            # AI分析
            print_section("步骤 9: AI深度分析")

            print("🤖 正在调用AI分析商品...")
            print("   (这可能需要30-60秒，请耐心等待...)")

            ai_analysis_result = await get_ai_analysis(
                final_record,
                downloaded_image_paths,
                prompt_text=ai_prompt_text
            )

            if ai_analysis_result:
                print("✅ AI分析完成!")
                final_record['ai_analysis'] = ai_analysis_result

                # 显示分析结果
                print("\n" + "="*80)
                print("  📊 AI分析结果")
                print("="*80 + "\n")

                is_recommended = ai_analysis_result.get('is_recommended', False)
                reason = ai_analysis_result.get('reason', '无')
                risk_tags = ai_analysis_result.get('risk_tags', [])
                criteria = ai_analysis_result.get('criteria_analysis', {})
                seller_analysis = criteria.get('seller_type', {})

                # 推荐状态
                if is_recommended:
                    print("✅ 是否推荐: 是 ✅")
                else:
                    print("❌ 是否推荐: 否 ❌")

                # 推荐理由
                print(f"\n💬 推荐理由:")
                print(f"   {reason}")

                # 风险标签
                if risk_tags:
                    print(f"\n⚠️  风险标签: {', '.join(risk_tags)}")

                # 卖家画像
                if seller_analysis:
                    print(f"\n👤 卖家画像:")
                    print(f"   类型: {seller_analysis.get('status', '未知')}")
                    persona = seller_analysis.get('persona', '未知')
                    if persona:
                        print(f"   详细: {persona}")

                    comment = seller_analysis.get('comment', '')
                    if comment:
                        print(f"\n   综合评价:")
                        for line in comment.split('。'):
                            if line.strip():
                                print(f"   • {line.strip()}")

                    # 行为逻辑链总结
                    details = seller_analysis.get('analysis_details', {})
                    summary = details.get('behavioral_summary', {})
                    if summary:
                        print(f"\n   行为逻辑链:")
                        print(f"   {summary.get('comment', '')}")
                        evidence = summary.get('evidence', '')
                        if evidence:
                            print(f"   证据: {evidence}")

                # 详细分析
                print(f"\n📋 详细分析:")
                for key, value in criteria.items():
                    if key != 'seller_type':
                        status = value.get('status', '未知')
                        comment = value.get('comment', '')
                        if comment and status != 'PASS':
                            print(f"\n   {key}:")
                            print(f"     状态: {status}")
                            print(f"     说明: {comment}")

                # 决策建议
                print("\n" + "="*80)
                if is_recommended:
                    print("  🎉 决策建议: 推荐购买!")
                else:
                    print("  ⚠️  决策建议: 不建议购买，请谨慎!")
                print("="*80 + "\n")

            else:
                print("❌ AI分析失败")
                final_record['ai_analysis'] = {'error': 'AI analysis failed'}

            # 保存结果
            print_section("步骤 10: 保存分析结果")

            output_dir = "single_analysis_results"
            os.makedirs(output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_dir, f"analysis_{timestamp}.json")

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(final_record, f, ensure_ascii=False, indent=2)

            print(f"✅ 分析结果已保存到: {output_file}")

            # 清理图片
            print_section("步骤 11: 清理临时文件")
            cleanup_task_images("single_analysis")
            print("✅ 临时图片已清理")

            print_section("分析完成!")
            print(f"完整数据已保存至: {output_file}")
            print("您可以用任何JSON查看器查看详细数据\n")

            await browser.close()

    except Exception as e:
        print(f"\n❌ 分析过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


async def main():
    parser = argparse.ArgumentParser(
        description="单个闲鱼商品链接快速分析工具",
        epilog="""
示例:
  # 分析MacBook商品
  python analyze_single.py https://www.goofish.com/item/i123456 prompts/macbook_criteria.txt

  # 分析其他商品（使用MacBook标准）
  python analyze_single.py https://www.goofish.com/item/i789012
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("url", help="闲鱼商品链接")
    parser.add_argument("criteria", nargs='?', default="prompts/macbook_criteria.txt",
                       help="分析标准文件路径（默认: prompts/macbook_criteria.txt）")
    args = parser.parse_args()

    await analyze_single_link(args.url, args.criteria)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        sys.exit(0)
