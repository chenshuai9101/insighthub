"""InsightHub 通用工具函数"""

from fastapi import Request
from fastapi.responses import RedirectResponse
from jinja2 import Environment, FileSystemLoader
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Jinja2 模板引擎
template_env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    autoescape=True,
)


class Templates:
    """简化模板渲染"""

    def TemplateResponse(self, name, context):
        template = template_env.get_template(name)
        html = template.render(**context)
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html)


templates = Templates()


# Cookie 名称
USER_COOKIE = "insighthub_user_id"


def get_current_user_id(request: Request) -> int:
    """从 Cookie 获取当前用户 ID，默认返回匿名用户"""
    user_id_str = request.cookies.get(USER_COOKIE)
    if user_id_str and user_id_str.isdigit():
        return int(user_id_str)
    return 1  # 匿名用户


def set_user_cookie(response: RedirectResponse, user_id: int):
    """设置用户 Cookie"""
    response.set_cookie(
        key=USER_COOKIE,
        value=str(user_id),
        max_age=30 * 24 * 3600,  # 30天
        httponly=True,
    )


def clear_user_cookie(response: RedirectResponse):
    """清除用户 Cookie"""
    response.delete_cookie(key=USER_COOKIE)
