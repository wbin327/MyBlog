# encoding=utf-8
from flask import Blueprint

'''
这个模块主要用于一些全局的路由定义,例如404、500等
通过实例化一个 Blueprint 类对象可以创建蓝本。这个构造函数有两个必须指定的参数：
蓝本的名字和蓝本所在的包或模块。 和程序一样，大多数情况下第二个参数使用 Python 的
__name__ 变量即可。
'''
main = Blueprint('main', __name__)
from . import views, errors
