# encoding=utf-8

from functools import wraps
from flask import abort, session
from app.models.user import User
from app.models.permission import Permission
from flask_login import current_user


def root_decorators(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.is_administrator():
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(func):
    return root_decorators(Permission.ADMINISTER)(func)


def write_required(func):
    return root_decorators(Permission.WRITE_ARTICLES)(func)


def login_required(func):
    @wraps(func)
    def decorator_function(*args, **kwargs):
        try:
            userinfo = session['userinfo']
            return func(*args, **kwargs)
        except Exception,e:
            abort(403)
    return decorator_function


