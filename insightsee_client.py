"""InsightSee API 客户端（需求解码分析）"""

import httpx
from config import INSIGHTSEE_URL, INSIGHTSEE_TIMEOUT

# 模拟分析结果
MOCK_RESULTS = {
    "positive": {
        "summary": "用户对产品品质和服务的满意度较高",
        "top_insights": [
            {"rank": 1, "content": "产品品质好、做工精细是用户最常提到的优点", "percentage": 35},
            {"rank": 2, "content": "配送/物流速度快，用户体验良好", "percentage": 28},
            {"rank": 3, "content": "客服服务态度好，解决问题及时", "percentage": 22},
        ],
        "details": [
            {"item": "品质认可", "count": 68, "ratio": "35%"},
            {"item": "物流体验", "count": 54, "ratio": "28%"},
            {"item": "服务态度", "count": 43, "ratio": "22%"},
            {"item": "包装精美", "count": 21, "ratio": "11%"},
            {"item": "性价比高", "count": 8, "ratio": "4%"},
        ],
    },
    "negative": {
        "summary": "用户不满主要集中在价格、质量和等待时间",
        "top_insights": [
            {"rank": 1, "content": "价格偏高或性价比不足是核心痛点", "percentage": 32},
            {"rank": 2, "content": "产品质量不稳定，部分批次出现瑕疵", "percentage": 28},
            {"rank": 3, "content": "等待/排队时间过长影响体验", "percentage": 18},
        ],
        "details": [
            {"item": "价格偏高", "count": 42, "ratio": "32%"},
            {"item": "质量瑕疵", "count": 37, "ratio": "28%"},
            {"item": "等待时间长", "count": 24, "ratio": "18%"},
            {"item": "售后体验差", "count": 18, "ratio": "14%"},
            {"item": "功能缺失", "count": 11, "ratio": "8%"},
        ],
    },
    "returns": {
        "summary": "退货的主要原因集中在质量问题和描述不符",
        "top_insights": [
            {"rank": 1, "content": "商品存在质量问题（破损/故障）是首要退货原因", "percentage": 40},
            {"rank": 2, "content": "实物与描述不符/色差问题", "percentage": 28},
            {"rank": 3, "content": "尺码/规格不合适", "percentage": 18},
        ],
        "details": [
            {"item": "质量问题", "count": 45, "ratio": "40%"},
            {"item": "描述不符", "count": 32, "ratio": "28%"},
            {"item": "尺码不合", "count": 20, "ratio": "18%"},
            {"item": "迟发漏发", "count": 10, "ratio": "9%"},
            {"item": "其他原因", "count": 6, "ratio": "5%"},
        ],
    },
    "needs": {
        "summary": "用户需求主要集中在功能完善和体验优化",
        "top_insights": [
            {"rank": 1, "content": "用户希望增加更多个性化定制选项", "percentage": 35},
            {"rank": 2, "content": "期待更低的价格或更多优惠活动", "percentage": 25},
            {"rank": 3, "content": "希望改善产品耐用性和长期稳定性", "percentage": 20},
        ],
        "details": [
            {"item": "个性化定制", "count": 55, "ratio": "35%"},
            {"item": "价格优惠", "count": 40, "ratio": "25%"},
            {"item": "品质提升", "count": 32, "ratio": "20%"},
            {"item": "功能扩展", "count": 22, "ratio": "14%"},
            {"item": "售后优化", "count": 10, "ratio": "6%"},
        ],
    },
    "persona": {
        "summary": "主要用户群体画像分析",
        "top_insights": [
            {"rank": 1, "content": "主力用户为25-35岁都市白领，注重品质和效率", "percentage": 40},
            {"rank": 2, "content": "女性用户占比略高，对细节和服务更敏感", "percentage": 35},
            {"rank": 3, "content": "价格敏感型用户占比约25%，对性价比要求高", "percentage": 25},
        ],
        "details": [
            {"item": "25-35岁白领", "count": 120, "ratio": "40%"},
            {"item": "女性用户", "count": 105, "ratio": "35%"},
            {"item": "价格敏感型", "count": 75, "ratio": "25%"},
            {"item": "学生群体", "count": 30, "ratio": "10%"},
            {"item": "企业采购", "count": 20, "ratio": "7%"},
        ],
    },
    "trends": {
        "summary": "消费趋势洞察",
        "top_insights": [
            {"rank": 1, "content": "用户对绿色环保、可持续产品的关注度上升", "percentage": 30},
            {"rank": 2, "content": "AI智能化功能成为新的需求增长点", "percentage": 28},
            {"rank": 3, "content": "社交电商内容对消费决策的影响持续增强", "percentage": 22},
        ],
        "details": [
            {"item": "环保可持续", "count": 65, "ratio": "30%"},
            {"item": "AI智能化", "count": 60, "ratio": "28%"},
            {"item": "社交电商影响", "count": 48, "ratio": "22%"},
            {"item": "国货品牌偏好", "count": 28, "ratio": "13%"},
            {"item": "订阅制消费", "count": 15, "ratio": "7%"},
        ],
    },
}


async def analyze(extracted_data: dict, dimensions: list) -> dict:
    """调用 InsightSee 分析提取的数据"""
    try:
        async with httpx.AsyncClient(timeout=INSIGHTSEE_TIMEOUT) as client:
            payload = {
                "data": extracted_data,
                "dimensions": dimensions,
            }
            resp = await client.post(f"{INSIGHTSEE_URL}/analyze", json=payload)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass

    # 降级：返回模拟分析结果
    results = {}
    for dim in dimensions:
        results[dim] = MOCK_RESULTS.get(dim, MOCK_RESULTS["positive"])
    return {
        "source": extracted_data.get("source", "unknown"),
        "total_reviews": extracted_data.get("total_reviews", 100),
        "results": results,
        "generated_at": "模拟模式（InsightSee 服务不可用）",
    }
