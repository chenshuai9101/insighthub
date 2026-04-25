"""报告查看路由"""

from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from models import get_analysis, get_user_analyses
from utils import templates, get_current_user_id
from datetime import datetime

router = APIRouter()


@router.get("/reports", response_class=HTMLResponse)
async def reports_list(request: Request):
    user_id = get_current_user_id(request)
    analyses = get_user_analyses(user_id)
    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "analyses": analyses,
        },
    )


@router.get("/report/{task_id}", response_class=HTMLResponse)
async def report_detail(request: Request, task_id: int):
    analysis = get_analysis(task_id)
    if not analysis:
        return templates.TemplateResponse(
            "report.html",
            {"request": request, "error": "报告不存在"},
        )
    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "analysis": analysis,
            "result": analysis.get("result"),
        },
    )


@router.get("/api/report/{task_id}")
async def api_report(task_id: int):
    analysis = get_analysis(task_id)
    if not analysis:
        return {"error": "报告不存在"}, 404
    return analysis
