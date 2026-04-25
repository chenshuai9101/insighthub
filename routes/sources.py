"""数据源市场路由"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from config import SOURCES
from utils import templates

router = APIRouter()


@router.get("/sources", response_class=HTMLResponse)
async def sources_page(request: Request):
    return templates.TemplateResponse(
        "sources.html",
        {
            "request": request,
            "sources": SOURCES,
        },
    )


@router.get("/api/sources")
async def api_sources():
    """返回数据源列表（JSON API）"""
    return {"sources": SOURCES}


@router.get("/api/sources/{source_id}")
async def api_source_detail(source_id: str):
    """返回单个数据源详情"""
    for s in SOURCES:
        if s["id"] == source_id:
            return s
    return {"error": "数据源不存在"}, 404
