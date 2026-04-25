"""用户系统路由"""

from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from fastapi import Query
from models import get_or_create_user, get_user_by_api_key, get_user_by_id
from utils import templates, set_user_cookie, clear_user_cookie, get_current_user_id
import uuid

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "user_id": get_current_user_id(request)},
    )


@router.post("/login")
async def login_action(request: Request, email: str = Form(...)):
    user = get_or_create_user(email)
    response = RedirectResponse(url="/", status_code=303)
    set_user_cookie(response, user["id"])
    return response


@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    clear_user_cookie(response)
    return response


@router.get("/api-key")
async def api_key_page(request: Request):
    """API Key 管理页"""
    user_id = get_current_user_id(request)
    user = get_user_by_id(user_id)
    return templates.TemplateResponse(
        "api_key.html",
        {"request": request, "user": user},
    )


@router.post("/api-key/regenerate")
async def regenerate_api_key(request: Request):
    user_id = get_current_user_id(request)
    from models import get_db
    new_key = str(uuid.uuid4())
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET api_key = ? WHERE id = ?", (new_key, user_id))
    conn.commit()
    conn.close()
    user = get_user_by_id(user_id)
    return templates.TemplateResponse(
        "api_key.html",
        {"request": request, "user": user, "message": "API Key 已重新生成"},
    )


@router.get("/api/auth/check")
async def api_check(api_key: str = Query(...)):
    """API 认证检查"""
    user = get_user_by_api_key(api_key)
    if user:
        return {"valid": True, "user_id": user["id"], "plan": user["plan"]}
    return {"valid": False}
