"""分析配置向导路由"""

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from config import SOURCES, ANALYSIS_DIMENSIONS
from models import (
    create_analysis,
    update_analysis_result,
    can_analyze,
    increment_analysis_count,
)
from insightlens_client import extract
from insightsee_client import analyze
from utils import templates, get_current_user_id

router = APIRouter()


@router.get("/configure", response_class=HTMLResponse)
async def configure_page(request: Request):
    user_id = get_current_user_id(request)
    return templates.TemplateResponse(
        "configure.html",
        {
            "request": request,
            "sources": SOURCES,
            "dimensions": ANALYSIS_DIMENSIONS,
            "user_id": user_id,
        },
    )


@router.get("/configure/{source_id}", response_class=HTMLResponse)
async def configure_with_source(request: Request, source_id: str):
    user_id = get_current_user_id(request)
    source = None
    for s in SOURCES:
        if s["id"] == source_id:
            source = s
            break
    return templates.TemplateResponse(
        "configure.html",
        {
            "request": request,
            "sources": SOURCES,
            "dimensions": ANALYSIS_DIMENSIONS,
            "selected_source": source,
            "user_id": user_id,
        },
    )


@router.post("/configure/run")
async def run_analysis(
    request: Request,
    source_id: str = Form(...),
    url: Optional[str] = Form(""),
    keyword: Optional[str] = Form(""),
    dimensions: list[str] = Form(...),
    schedule: Optional[int] = Form(0),
):
    user_id = get_current_user_id(request)

    if not can_analyze(user_id):
        return templates.TemplateResponse(
            "configure.html",
            {
                "request": request,
                "sources": SOURCES,
                "dimensions": ANALYSIS_DIMENSIONS,
                "error": "本月分析次数已用完，请升级套餐",
            },
        )

    # 创建分析任务
    task_id = create_analysis(user_id, source_id, url, keyword, dimensions)

    # 执行分析链路：InsightLens → InsightSee
    extracted = await extract(source_id, url, keyword)
    analysis_result = await analyze(extracted, dimensions)

    # 保存结果
    update_analysis_result(task_id, "completed", analysis_result)
    increment_analysis_count(user_id)

    # 如果设置了定时分析
    if schedule > 0:
        from models import create_schedule
        create_schedule(user_id, task_id, schedule)

    # 跳转到报告页
    return RedirectResponse(url=f"/report/{task_id}", status_code=303)
