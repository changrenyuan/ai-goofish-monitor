# 数据爬取与 AI 分析指南

## 一、爬取的数据保存在哪里？

### 1. 原始数据文件（JSONL 格式）

爬取的所有商品数据都会保存到 `jsonl/` 目录下的 `.jsonl` 文件中：

```
jsonl/
├── iphone_15_2026-01-12.jsonl          # iPhone 15 任务的数据
├── macbook_m1_2026-01-12.jsonl         # MacBook 任务的数据
└── watch_s10_2026-01-12.jsonl          # Watch 任务的数据
```

每个文件按日期命名，格式为：`{关键词}_{日期}.jsonl`

### 2. 商品图片

商品图片会下载到 `images/task_images_{任务名称}/` 目录：

```
images/
└── task_images_iPhone 15 监控/
    ├── product_123456_1_800x800.jpg
    ├── product_123456_2_800x800.jpg
    └── product_123456_3_800x800.jpg
```

### 3. AI 分析日志

AI 分析的日志保存在 `logs/ai/` 目录：

```
logs/ai/
├── 20260112_143025.log
├── 20260112_143032.log
└── ...
```

## 二、如何查看爬取的数据？

### 方法 1：Web 界面查看（推荐）

1. **访问结果页面**
   - 登录后，点击顶部菜单的 **"结果"** 标签

2. **选择数据文件**
   - 在结果页面，选择对应的 `.jsonl` 文件
   - 文件名格式：`{关键词}_{日期}.jsonl`

3. **查看数据**
   - 系统会以表格形式展示所有爬取的商品
   - 包含：商品标题、价格、发布时间、AI 分析结果等

4. **筛选和排序**
   - 可以勾选 **"仅显示推荐"** 只看 AI 推荐的商品
   - 可以按价格、发布时间、爬取时间排序
   - 支持分页浏览（默认每页 20 条）

5. **查看详情**
   - 点击某条记录可以查看完整的商品数据
   - 包含：商品信息、卖家信息、AI 分析结果

### 方法 2：直接查看 JSONL 文件

使用文本编辑器打开 `jsonl/` 目录下的 `.jsonl` 文件：

```bash
# 在 Linux/Mac 上
cat jsonl/iphone_15_2026-01-12.jsonl

# 在 Windows 上
type jsonl\iphone_15_2026-01-12.jsonl
```

每行是一个 JSON 对象，代表一个商品：

```json
{
  "任务名称": "iPhone 15 监控",
  "爬取时间": "2026-01-12 14:30:25",
  "商品信息": {
    "商品ID": "123456",
    "商品标题": "iPhone 15 128G 粉色 9新",
    "当前售价": "¥4,200",
    "发布时间": "2026-01-12 10:00",
    "商品描述": "自用机，无拆无修，电池健康95%...",
    "商品主图链接": "https://...",
    "商品图片列表": ["https://...", "https://..."],
    "商品链接": "https://2.taobao.com/item.htm?id=..."
  },
  "卖家信息": {
    "卖家昵称": "张三",
    "卖家信用等级": "卖家信用极好",
    "注册天数": "365",
    "交易记录": [
      {"商品": "iPhone 14", "时间": "2025-06"},
      {"商品": "AirPods", "时间": "2024-12"}
    ]
  },
  "ai_analysis": {
    "prompt_version": "V6.4",
    "is_recommended": true,
    "reason": "成色新，电池健康95%，卖家信用极好，交易记录显示为个人玩家",
    "risk_tags": [],
    "criteria_analysis": {
      "model_chip": "通过 - iPhone 15 128G",
      "battery_health": "通过 - 95%",
      "condition": "通过 - 9新",
      "history": "通过 - 无拆无修",
      "seller_type": "个人玩家 - 交易记录显示长期发烧友"
    }
  }
}
```

### 方法 3：使用命令行工具

```bash
# 统计爬取的商品数量
wc -l jsonl/*.jsonl

# 查看最新的商品
tail -1 jsonl/iphone_15_2026-01-12.jsonl | jq

# 过滤推荐的商品
grep '"is_recommended": true' jsonl/*.jsonl | jq
```

## 三、AI 分析是如何触发的？

### 完整的 AI 分析流程

```
1. 爬虫启动
   ↓
2. 访问闲鱼搜索页面
   ↓
3. 获取商品列表（HTML/JSON）
   ↓
4. 解析商品数据
   - 商品标题、价格、描述
   - 卖家信息、信用等级
   - 商品图片链接
   ↓
5. 下载商品图片
   - 保存到 images/task_images_{任务名称}/
   ↓
6. 【关键】调用 AI 分析
   ↓
7. AI 分析商品和图片
   - 商品信息（JSON 格式）
   - 商品图片（Base64 编码）
   - 分析标准（Prompt 文件）
   ↓
8. 接收 AI 响应
   - is_recommended: 是否推荐
   - reason: 推荐理由
   - risk_tags: 风险标签
   - criteria_analysis: 详细分析
   ↓
9. 保存完整数据
   - 附加 AI 分析结果
   - 保存到 .jsonl 文件
   ↓
10. 发送通知（如果推荐）
    - ntfy / 微信 / Telegram 等
```

### 关键代码位置

#### 1. AI 分析触发点
文件：`src/scraper.py`，约 600 行

```python
# 爬虫在爬取每个商品后会调用 AI 分析
ai_result = await get_ai_analysis(
    product_data=product_data,
    image_paths=image_paths,
    prompt_text=prompt_text
)
```

#### 2. AI 分析函数
文件：`src/ai_handler.py`，约 513 行

```python
async def get_ai_analysis(product_data, image_paths=None, prompt_text=""):
    """
    将完整的商品JSON数据和所有图片发送给 AI 进行分析
    
    Args:
        product_data: 商品数据（包含商品信息和卖家信息）
        image_paths: 下载的图片路径列表
        prompt_text: 分析标准（从 prompts/*.txt 读取）
    
    Returns:
        AI 分析结果（JSON 格式）
    """
```

## 四、AI 分析的详细过程

### 1. 构建发送给 AI 的数据

#### 商品数据（JSON 格式）

AI 会收到完整的商品数据，包括：

```json
{
  "商品信息": {
    "商品ID": "123456",
    "商品标题": "iPhone 15 128G 粉色 9新",
    "当前售价": "¥4,200",
    "发布时间": "2026-01-12 10:00",
    "商品描述": "自用机，无拆无修，电池健康95%...",
    "商品主图链接": "https://...",
    "商品图片列表": ["https://...", "https://..."]
  },
  "卖家信息": {
    "卖家昵称": "张三",
    "卖家信用等级": "卖家信用极好",
    "注册天数": "365",
    "交易记录": [...]
  }
}
```

#### 商品图片

所有商品图片会转换为 Base64 格式发送给 AI：

```
data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBD...
```

#### 分析标准（Prompt）

从 `prompts/{任务名}_criteria.txt` 读取，例如：

```
### 第一部分：核心分析原则

1. 一票否决硬性原则：
   - 必须是 iPhone 15
   - 电池健康必须 ≥ 90%
   - 成色 9新以上
   ...

### 第二部分：详细分析指南

1. 型号检查：...
2. 成色评估：...
3. 卖家类型判断：...
...
```

### 2. AI 响应格式

AI 返回的 JSON 结构：

```json
{
  "prompt_version": "V6.4",
  "is_recommended": true,
  "reason": "成色新，电池健康95%，卖家信用极好，交易记录显示为个人玩家",
  "risk_tags": [],
  "criteria_analysis": {
    "model_chip": "通过 - iPhone 15 128G",
    "battery_health": "通过 - 95%",
    "condition": "通过 - 9新",
    "history": "通过 - 无拆无修",
    "seller_type": "个人玩家 - 交易记录显示长期发烧友",
    "shipping": "通过 - 支持邮寄",
    "seller_credit": "通过 - 卖家信用极好"
  }
}
```

### 3. AI 分析的判断逻辑

#### 示例 1：推荐的商品

```
✅ is_recommended: true

判断依据：
1. 商品符合所有硬性要求（型号、价格、成色）
2. 电池健康 95%（≥ 90%）
3. 无维修历史
4. 卖家信用极好
5. 交易记录显示为个人玩家（非商家）

结果：发送通知
```

#### 示例 2：不推荐的商品

```
❌ is_recommended: false

判断依据：
1. 卖家交易记录显示批量售卖（5个相同商品）
2. 卖家描述中有"工作室"、"拿货"等商家术语

结果：不发送通知
```

## 五、如何让 AI 进行分析？

### 方法 1：创建任务时自动分析（推荐）

当你使用 **"AI 生成任务"** 创建任务后，AI 分析会自动启用：

1. AI 根据你的描述生成分析标准
2. 保存到 `prompts/{任务名}_criteria.txt`
3. 启动任务时，自动对每个商品进行 AI 分析

### 方法 2：手动配置分析标准

如果你想手动控制 AI 分析，可以：

1. **编辑 Prompt 文件**

打开 `prompts/{任务名}_criteria.txt`，修改分析规则：

```text
### 第一部分：核心分析原则

1. 一票否决硬性原则：
   - 必须是 [你的产品名称]
   - 价格范围：[最低价格] - [最高价格]
   - 成色要求：[如 9新以上]
   ...

2. 卖家类型判断：
   - 排除商家
   - 优先个人玩家
   ...
```

2. **任务配置确保 AI 启用**

在 Web 界面编辑任务，确保：
- `ai_prompt_base_file`: `prompts/base_prompt.txt`
- `ai_prompt_criteria_file`: `prompts/{任务名}_criteria.txt`

### 方法 3：关闭 AI 分析

如果你不想使用 AI 分析，可以：

1. 在 `.env` 文件中设置：
   ```env
   SKIP_AI_ANALYSIS=true
   ```

2. 或者修改任务配置，删除 AI Prompt 文件路径

## 六、调试 AI 分析

### 1. 启用 AI 调试模式

在 `.env` 文件中设置：

```env
AI_DEBUG_MODE=true
```

这会在控制台打印：
- 发送给 AI 的完整数据
- AI 的原始响应
- 解析后的结果

### 2. 查看 AI 分析日志

```bash
# 查看最新的 AI 分析日志
ls -lt logs/ai/ | head -1

# 查看日志内容
cat logs/ai/20260112_143025.log | jq
```

### 3. 测试单个商品

创建测试脚本 `test_single_product.py`：

```python
import asyncio
from src.ai_handler import get_ai_analysis

async def test():
    product_data = {
        "商品信息": {
            "商品标题": "iPhone 15 128G",
            "当前售价": "¥4,200",
            "商品描述": "..."
        },
        "卖家信息": {
            "卖家信用等级": "卖家信用极好",
            ...
        }
    }
    
    result = await get_ai_analysis(
        product_data=product_data,
        image_paths=["images/xxx.jpg"],
        prompt_text=open("prompts/your_criteria.txt").read()
    )
    
    print(result)

asyncio.run(test())
```

## 七、常见问题

### Q1: AI 分析很慢，如何优化？

**A**: 
- 减少图片数量：在任务配置中设置只下载前 2-3 张图片
- 使用更快的模型：如 `gemini-1.5-flash` 而不是 `gemini-1.5-pro`
- 启用缓存：已经分析过的商品不会重复分析

### Q2: AI 分析不准确怎么办？

**A**:
- 启用调试模式查看 AI 的完整输入输出
- 优化 Prompt 文件，添加更详细的规则
- 调整分析标准的权重和判断逻辑
- 尝试不同的 AI 模型

### Q3: 如何只看推荐的商品？

**A**:
1. 在 Web 界面勾选 **"仅显示推荐"**
2. 或使用命令行过滤：
   ```bash
   grep '"is_recommended": true' jsonl/*.jsonl | jq
   ```

### Q4: AI 分析失败怎么处理？

**A**:
- 检查 AI API Key 是否配置正确
- 查看日志文件确认错误原因
- 运行 `python diagnose_ai.py` 诊断配置
- 确保网络可以访问 AI 服务

### Q5: 数据会重复分析吗？

**A**: 不会。系统会：
- 记录已分析的商品链接
- 去重后再分析
- 已分析的商品保存在 `.jsonl` 文件中

## 八、数据示例

### 完整的商品数据示例

```json
{
  "任务名称": "iPhone 15 监控",
  "爬取时间": "2026-01-12 14:30:25",
  "商品信息": {
    "商品ID": "123456789",
    "商品标题": "iPhone 15 128G 粉色 自用机 无拆无修",
    "当前售价": "¥4,200",
    "原价": "¥5,999",
    "发布时间": "2026-01-12 10:15",
    "商品描述": "自用iPhone 15，粉色128G，成色9新，无磕碰无划痕，电池健康95%，无拆无修无进水，原装配件齐全，支持验机，只接受同城面交",
    "商品主图链接": "https://gw.alicdn.com/tfscom...",
    "商品图片列表": [
      "https://gw.alicdn.com/tfscom/img1.jpg",
      "https://gw.alicdn.com/tfscom/img2.jpg",
      "https://gw.alicdn.com/tfscom/img3.jpg"
    ],
    "商品链接": "https://2.taobao.com/item.htm?id=123456789"
  },
  "卖家信息": {
    "卖家昵称": "数码发烧友小王",
    "卖家信用等级": "卖家信用极好",
    "卖家信用分数": "723",
    "注册天数": "730",
    "交易记录": [
      {"商品": "iPhone 14 Pro", "时间": "2025-08", "价格": "¥5,800"},
      {"商品": "AirPods Pro 2", "时间": "2025-05", "价格": "¥1,200"},
      {"商品": "MacBook Air", "时间": "2024-11", "价格": "¥6,500"}
    ],
    "卖家地址": "北京市朝阳区"
  },
  "ai_analysis": {
    "prompt_version": "V6.4",
    "is_recommended": true,
    "reason": "✅ 成色9新，电池健康95%符合要求\n✅ 无拆无修，无维修历史\n✅ 卖家信用极好（723分）\n✅ 交易记录显示长期数码发烧友（2年注册，多次升级换机）\n✅ 价格合理（¥4,200，原价¥5,999，约7折）\n✅ 图片清晰，包装齐全",
    "risk_tags": [],
    "criteria_analysis": {
      "model_chip": "✅ 通过 - iPhone 15 128G",
      "battery_health": "✅ 通过 - 95% (≥ 90%)",
      "condition": "✅ 通过 - 9新，无磕碰无划痕",
      "history": "✅ 通过 - 无拆无修无进水",
      "seller_type": "✅ 个人玩家 - 交易记录显示长期数码发烧友，从iPhone 14到MacBook的升级路径",
      "shipping": "⚠️ 注意 - 仅支持同城面交",
      "seller_credit": "✅ 通过 - 卖家信用极好（723分）",
      "price": "✅ 通过 - ¥4,200 在合理区间（3500-4500）"
    }
  }
}
```

这个商品会被标记为 **is_recommended: true**，系统会发送通知！
