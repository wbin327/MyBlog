# encoding=utf-8
'''
在单个文件中开发程序很方便，但却有个很大的缺点，因为程序在全局作用域中创建，所
以无法动态修改配置。 运行脚本时，程序实例已经创建，再修改配置为时已晚。这一点对
单元测试尤其重要，因为有时为了提高测试覆盖度，必须在不同的配置环境中运行程序。

这个问题的解决方法是延迟创建程序实例， 把创建过程移到可显式调用的工厂函数中。这
种方法不仅可以给脚本留出配置程序的时间， 还能够创建多个程序实例，这些实例有时在
测试中非常有用。

构造文件导入了大多数正在使用的 Flask 扩展。由于尚未初始化所需的程序实例，所以没
有初始化扩展， 创建扩展类时没有向构造函数传入参数。 create_app() 函数就是程序的工
厂函数，接受一个参数，是程序使用的配置名。配置类在 config.py 文件中定义，其中保存
的配置可以使用 Flask app.config 配置对象提供的 from_object() 方法直接导入程序。至
于配置对象， 则可以通过名字从 config 字典中选择。程序创建并配置好后，就能初始化
扩展了。在之前创建的扩展对象上调用 init_app() 可以完成初始化过程。
'''

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown
import os

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

# 初始化Flask_Login
login_manager = LoginManager()
'''
LoginManager 对象的session_protection 属性可以设为None、'basic' 或'strong'，以提
供不同的安全等级防止用户会话遭篡改。设为'strong' 时，Flask-Login 会记录客户端IP
地址和浏览器的用户代理信息，如果发现异动就登出用户
'''
login_manager.session_protection = 'strong'
'''
login_view 属性设置登录页面
的端点。回忆一下，登录路由在蓝本中定义，因此要在前面加上蓝本的名字。
'''
login_manager.login_view = '/user/login'

# 初始化pagedown
pagedown = PageDown()

# 初始化根目录
basepath = os.path.dirname(__file__)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # 注册蓝本
    from main import main as main_blueprint
    from user import user as user_blueprint
    from blog import blog as blog_blueprint
    app.register_blueprint(main_blueprint)
    #  url_prefix 是可选参数,注册后蓝本中定义的所有路由都会加上指定的前缀
    #  例如该蓝本下定义了/login路由，则访问时的路径为/auth/login
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    # 附加路由和自定义的错误页面
    return app




'''
LoginManager.user_loader 回调函数，它的作用是在用户登录并调用 login_user() 的时候, 根据 user_id 找到对应的 user, 
如果没有找到，返回None, 此时的 user_id 将会自动从 session 中移除, 若能找到 user ，则 user_id 会被继续保存.
'''
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))
