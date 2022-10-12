from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render



def login_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get("has_login", False) == False or request.session.get("user_id", 0) == 0:
            # print("尚未登陆")
            msg = "尚未登陆，请先登陆再进行操作。"
            return render(request, "login.html", locals())
        else:
            pass
        # print(request.session.get("nickname") + "已登陆")
        return func(request, *args, **kwargs)

    return inner


def login_required_json(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get("has_login", False) == False or request.session.get("user_id", 0) == 0:
            # print("尚未登陆")
            if request.POST.get("operation") != "load_headerbar":
                msg = "尚未登陆，请先登陆再进行操作。"
                return JsonResponse({"code": 500, "msg": msg})
        else:
            pass
        # print(request.session.get("nickname") + "已登陆")
        return func(request, *args, **kwargs)

    return inner


def auth_superuser_required_json(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get("user_type", 2) != 0:
            msg = "权限不足，无法进行操作。"
            return JsonResponse({"code": 300, "msg": msg})
        else:
            pass
        # print(request.session.get("nickname") + "已登陆")
        return func(request, *args, **kwargs)

    return inner


def auth_administrator_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get("user_type", 2) == 2:
            msg = "权限不足，无法进行操作。"
            return render(request, "libEnd/wrongmsg.html", locals())
        else:
            pass
        # print(request.session.get("nickname") + "已登陆")
        return func(request, *args, **kwargs)

    return inner


def auth_administrator_required_json(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get("user_type", 2) == 2:
            msg = "权限不足，无法进行操作。"
            return JsonResponse({"code": 300, "msg": msg})
        else:
            pass
        # print(request.session.get("nickname") + "已登陆")
        return func(request, *args, **kwargs)

    return inner


def cache_is_open(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not settings.USE_MY_REDIS_CACHE:
            return None
        return func(request, *args, **kwargs)
    return inner
