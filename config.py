"""InsightHub 配置"""

import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库
DATABASE_URL = os.path.join(BASE_DIR, "data", "insighthub.db")

# 服务端口
HOST = "0.0.0.0"
PORT = int(os.getenv("INSIGHTHUB_PORT", "8080"))

# InsightLens 配置
INSIGHTLENS_URL = os.getenv("INSIGHTLENS_URL", "http://localhost:9091")
INSIGHTLENS_TIMEOUT = 30

# InsightSee 配置
INSIGHTSEE_URL = os.getenv("INSIGHTSEE_URL", "http://localhost:9090")
INSIGHTSEE_TIMEOUT = 30

# 会话密钥（仅用于flash消息）
SECRET_KEY = os.getenv("INSIGHTHUB_SECRET", "insighthub-dev-secret-key")

# 可用数据源
SOURCES = [
    {
        "id": "meituan",
        "name": "美团外卖",
        "icon": "🍜",
        "type": "free",
        "description": "美团外卖用户评价分析，提取用户需求与痛点",
        "categories": ["餐饮", "外卖", "本地生活"],
    },
    {
        "id": "dianping",
        "name": "大众点评",
        "icon": "⭐",
        "type": "free",
        "description": "大众点评商家评论分析，了解用户真实反馈",
        "categories": ["餐饮", "本地生活", "休闲娱乐"],
    },
    {
        "id": "taobao",
        "name": "淘宝评价",
        "icon": "🛒",
        "type": "paid",
        "price": 99,
        "description": "淘宝商品评价洞察，分析好评率与退货原因",
        "categories": ["电商", "商品", "消费"],
    },
    {
        "id": "xiaohongshu",
        "name": "小红书",
        "icon": "📕",
        "type": "paid",
        "price": 199,
        "description": "小红书笔记与评论分析，挖掘用户深层需求",
        "categories": ["社交", "种草", "生活方式"],
    },
    {
        "id": "jd",
        "name": "京东",
        "icon": "📦",
        "type": "paid",
        "price": 99,
        "description": "京东商品评价数据分析，售后退款原因洞察",
        "categories": ["电商", "3C数码", "消费"],
    },
]

# 可用分析维度
ANALYSIS_DIMENSIONS = [
    {"id": "positive", "name": "好评分析", "description": "提取用户点赞的关键点"},
    {"id": "negative", "name": "差评分析", "description": "定位用户不满的核心原因"},
    {"id": "returns", "name": "退货原因", "description": "分析退换货的深层原因"},
    {"id": "needs", "name": "用户需求", "description": "挖掘用户未被满足的需求"},
    {"id": "persona", "name": "用户画像", "description": "构建典型用户画像"},
    {"id": "trends", "name": "趋势洞察", "description": "发现消费趋势变化"},
]

# 定价方案
PLANS = [
    {
        "id": "free",
        "name": "免费版",
        "price": "¥0",
        "period": "永久",
        "features": ["5次分析/月", "1个数据源", "基础报告", "社区支持"],
        "highlight": False,
    },
    {
        "id": "personal",
        "name": "个人版",
        "price": "¥29",
        "period": "月",
        "features": ["无限分析", "3个数据源", "完整报告", "邮件推送", "导出PDF"],
        "highlight": False,
    },
    {
        "id": "team",
        "name": "团队版",
        "price": "¥99",
        "period": "月",
        "features": [
            "无限分析",
            "全部数据源",
            "完整报告+图表",
            "定时分析",
            "多人协作",
            "优先支持",
        ],
        "highlight": True,
    },
    {
        "id": "enterprise",
        "name": "企业版",
        "price": "¥499",
        "period": "月",
        "features": [
            "所有团队版功能",
            "私有化部署",
            "专属API通道",
            "定制分析维度",
            "SLA保障",
            "专属客户经理",
        ],
        "highlight": False,
    },
]
