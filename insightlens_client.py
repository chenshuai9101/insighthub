"""InsightLens API 客户端（网页提取）"""

import httpx
from config import INSIGHTLENS_URL, INSIGHTLENS_TIMEOUT

# 模拟数据：当 InsightLens 不可用时的降级数据
MOCK_EXTRACT_DATA = {
    "meituan": {
        "title": "美团外卖 - XX奶茶店评价",
        "content": "用户评价汇总：\n- '奶茶很好喝，珍珠很Q弹，推荐！'\n- '配送速度很快，包装也很好'\n- '味道一般，糖度不能调整有点遗憾'\n- '价格偏贵，分量有点少'\n- '店员态度很好，还送了小礼品'\n总计108条评价，好评率82%",
        "source": "meituan",
        "url": "https://www.meituan.com/example",
        "total_reviews": 108,
    },
    "dianping": {
        "title": "大众点评 - XX火锅店",
        "content": "用户评价汇总：\n- '锅底很正宗，牛油味浓郁，料很足'\n- '服务很好，等位还有零食吃'\n- '排队时间太长了，建议提前预约'\n- '价格适中，性价比不错'\n- '环境一般，有点嘈杂'\n总计245条评价，好评率75%",
        "source": "dianping",
        "url": "https://www.dianping.com/example",
        "total_reviews": 245,
    },
    "taobao": {
        "title": "淘宝 - XX商品评价",
        "content": "用户评价汇总：\n- '质量很好，做工精细，推荐购买'\n- '和描述一致，物流很快'\n- '颜色有点偏差，但总体满意'\n- '用了一个月就坏了，质量堪忧'\n- '退货流程很麻烦，客服态度差'\n总计560条评价，好评率68%，退货率12%",
        "source": "taobao",
        "url": "https://www.taobao.com/example",
        "total_reviews": 560,
    },
    "xiaohongshu": {
        "title": "小红书 - XX美妆产品笔记",
        "content": "笔记评论汇总：\n- '上脸效果很好，不卡粉！'\n- '成分安全吗？敏感肌可以用吗？'\n- '用了两周皮肤真的变好了'\n- '价格有点贵，但效果值得'\n- '求推荐不同色号的选择'\n总计320条评论，好评率88%",
        "source": "xiaohongshu",
        "url": "https://www.xiaohongshu.com/example",
        "total_reviews": 320,
    },
    "jd": {
        "title": "京东 - XX电子产品评价",
        "content": "用户评价汇总：\n- '性能强劲，运行流畅，物超所值'\n- '电池续航一般，一天一充'\n- '收到了瑕疵品，换货处理很快'\n- '性价比很高，适合学生党'\n- '系统偶尔卡顿，希望优化'\n总计890条评价，好评率72%，退货率8%",
        "source": "jd",
        "url": "https://www.jd.com/example",
        "total_reviews": 890,
    },
}

MOCK_DEFAULT = {
    "title": "数据源分析",
    "content": "从目标页面提取的用户评价数据，包含正负面反馈、使用体验描述等丰富信息。",
    "source": "unknown",
    "url": "https://example.com",
    "total_reviews": 100,
}


async def extract(source_id: str, url: str = "", keyword: str = "") -> dict:
    """调用 InsightLens 提取网页数据"""
    if not url and not keyword:
        keyword = source_id

    try:
        async with httpx.AsyncClient(timeout=INSIGHTLENS_TIMEOUT) as client:
            payload = {"url": url} if url else {"keyword": keyword}
            payload["source"] = source_id
            resp = await client.post(f"{INSIGHTLENS_URL}/extract", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data
    except Exception:
        pass

    # 降级：返回模拟数据
    mock = MOCK_EXTRACT_DATA.get(source_id, MOCK_DEFAULT)
    if url:
        mock["url"] = url
    if keyword:
        mock["keyword"] = keyword
    return mock
