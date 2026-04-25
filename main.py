"""InsightHub - FastAPI 应用入口"""

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from config import HOST, PORT, SOURCES
from routes import sources, analysis, reports, auth
from models import init_db, get_user_analyses
from utils import templates, get_current_user_id

# 初始化数据库
init_db()

app = FastAPI(
    title="InsightHub",
    description="洞察数据智能分析平台 - 点几下鼠标，拿到洞察报告",
    version="1.0.0",
)

# 挂载静态文件
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 挂载 assets（图片等）
assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# 注册路由
app.include_router(sources.router)
app.include_router(analysis.router)
app.include_router(reports.router)
app.include_router(auth.router)


# ---------- 页面路由 ----------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user_id = get_current_user_id(request)
    recent_analyses = get_user_analyses(user_id, limit=3)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "sources": SOURCES,
            "user_id": user_id,
            "recent_analyses": recent_analyses,
            "total_sources": len(SOURCES),
        },
    )


@app.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request):
    from config import PLANS
    return templates.TemplateResponse(
        "pricing.html",
        {"request": request, "plans": PLANS},
    )


@app.get("/pricing/{plan_id}")
async def pricing_checkout(request: Request, plan_id: str):
    """定价页 + 锚点到特定方案"""
    from config import PLANS
    return templates.TemplateResponse(
        "pricing.html",
        {"request": request, "plans": PLANS, "selected_plan": plan_id},
    )


# ---------- 启动 ----------

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 InsightHub 启动中... http://{HOST}:{PORT}")
    print(f"📊 首页: http://localhost:{PORT}")
    print(f"📋 数据源市场: http://localhost:{PORT}/sources")
    print(f"⚙️  配置向导: http://localhost:{PORT}/configure")
    print(f"💰 定价页: http://localhost:{PORT}/pricing")
    print(f"  模拟模式已启用（无需外部服务）")
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
