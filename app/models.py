# encoding=utf-8
from . import login_manager


'''
LoginManager.user_loader 回调函数，它的作用是在用户登录并调用 login_user() 的时候, 根据 user_id 找到对应的 user, 
如果没有找到，返回None, 此时的 user_id 将会自动从 session 中移除, 若能找到 user ，则 user_id 会被继续保存.
'''
@login_manager.user_loader()
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))