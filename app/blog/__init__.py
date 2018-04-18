# encoding=utf-8
# 用户模块
from flask import Blueprint


blog = Blueprint('blog', __name__)
from . import views
