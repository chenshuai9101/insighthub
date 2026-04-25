# 🔍 InsightHub - 洞察数据智能分析平台

> 面向传统企业用户的 SaaS 管理后台。点几下鼠标，拿到洞察报告。
> 底层能力由 **InsightSee**（用户需求解码）+ **InsightLens**（网页提取）提供。
> 用户不需要知道 Agent 是什么，零门槛使用。

---

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 📡 **数据源市场** | 美团外卖、大众点评、淘宝、小红书、京东等多平台数据源 |
| ⚙️ **一键配置向导** | 4 步完成分析配置：选数据源 → 输入URL/关键词 → 选维度 → 开始分析 |
| 📊 **报告查看器** | 洞察TOP3、维度占比柱状图、用户画像、CSS 柱状图（零JS库） |
| 🔑 **API Key 管理** | 程序化调用接口 |
| 💰 **定价方案** | 免费版(5次/月) / 个人版(¥29/月) / 团队版(¥99/月) / 企业版(¥499/月) |

## 🚀 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动
python3 main.py
```

访问 http://localhost:8080

### 启动脚本

```bash
bash scripts/start.sh
```

## 🏗️ 项目结构

```
insighthub/
├── main.py                 # FastAPI 入口
├── config.py               # 配置（数据源、定价方案、分析维度）
├── models.py               # SQLite 数据模型
├── utils.py                # 模板引擎、Cookie 工具
├── insightlens_client.py   # InsightLens API 客户端（带模拟降级）
├── insightsee_client.py    # InsightSee API 客户端（带模拟降级）
├── routes/                 # 路由
│   ├── sources.py          # 数据源市场
│   ├── analysis.py         # 分析配置
│   ├── reports.py          # 报告查看
│   └── auth.py             # 用户系统
├── templates/              # Jinja2 模板
├── static/style.css        # 纯 CSS 样式（零前端框架）
├── assets/                 # 收款码图片
├── scripts/                # 启动/打包脚本
└── data/                   # SQLite 数据库
```

## 🔗 API 对接

InsightLens: `localhost:9091`（网页提取）
InsightSee: `localhost:9090`（需求分析）
如果服务未启动，自动降级为模拟模式（内置演示数据）。

## 💳 定价方案

| 方案 | 价格 | 分析次数 | 数据源 |
|------|------|---------|--------|
| 免费版 | ¥0 | 5次/月 | 仅限免费数据源 |
| 个人版 | ¥29/月 | 无限 | 3个数据源 |
| 团队版 | ¥99/月 | 无限 | 全部数据源 |
| 企业版 | ¥499/月 | 无限 | 全部 + 私有化 |

**扫码付款开通：**

| 微信支付 | 支付宝 |
|---------|--------|
| ![微信支付](assets/wechat_pay.jpg) | ![支付宝](assets/alipay.jpg) |

## 📝 License

InsightLabs © 2026
