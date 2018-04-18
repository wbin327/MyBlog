# encoding=utf-8
# from .ServiceInterface import ServiceInterface
import time

from werkzeug.security import check_password_hash, generate_password_hash

from app.auth.auth import identify, encode_auth_token
from app.util.public_method import PublicMethod
from dao import Dao
from flask_login import login_user
import traceback


class Service(object):
    def __init__(self):
        self.dao = Dao()

    def background_login_check(self, name, password,  remember=False):
        """
        后台登录认证，使用了flask_login插件
        :param name: 用户名
        :param password: 密码
        :param session: 会话
        :param remember:保持登录，boolean
        :return: dict
        """

        user = self.dao.query_user_by_name(name)

        if user:
            result = check_password_hash(user.password, password)
            if result:
                user.login_time = time.time()
                self.dao.add(user)
                login_user(user, remember=remember)
                return PublicMethod.true_return(data='', msg='login_success')
            else:
                return PublicMethod.false_return(data='', msg='password_error')
        else:
            return PublicMethod.false_return(data='', msg='none_user')

    def login_check(self, name, password):
        """
            token验证，登录成功返回token,并将登录时间写入数据库；登录失败则返回失败原因
            :param username: 用户名
            :param password: 密码
            :return: dict
            """
        user = self.dao.query_user_by_name(name)

        if user:
            result = check_password_hash(user.password, password)
            if result:
                user.login_time = time.time()
                self.dao.add(user)
                token = encode_auth_token(user_id=user.id, login_time=user.login_time)
                return PublicMethod.true_return(data=token, msg='登录成功')
            else:
                return PublicMethod.false_return(data='', msg='密码错误')
        else:
            return PublicMethod.false_return(data='', msg='用户名不存在')

    def register(self, username, password):
        user = self.dao.query_user_by_name(username)
        if user:
            result = PublicMethod.false_return(data='', msg='用户名已存在')
        else:
            hash_password = generate_password_hash(password)
            excute = self.dao.add_user(username, hash_password)
            if excute is True:
                result = PublicMethod.true_return(data='', msg='注册成功')
            else:
                result = PublicMethod.false_return(data='', msg='注册失败')
        return result

    def get_user(self, authorization):
        result = identify(authorization)
        if not isinstance(result, str):
            user = result
            return PublicMethod.true_return(data=user.serialize(), msg='success')
        else:
            return PublicMethod.false_return(data='', msg=result)

    def logout(self, authorization):
        result = identify
        if not isinstance(result, str):
            user = result
            user.login_time = 0
            self.dao.add(user)

            return PublicMethod.true_return(data=user.serialize(), msg='success')
        else:
            return PublicMethod.false_return(data='', msg=result)

    def get_all_user(self):
        try:
            user_list = self.dao.get_all_user()
            return user_list
        except Exception:
            traceback.print_exc()
            return []

    def delete_user(self, request):
        try:
            user = self.dao.get_user_by_id(request.values.get('user_id'))
            self.dao.delete_user(user)
            return PublicMethod.true_return(data='', msg='删除用户成功!')
        except Exception:
            traceback.print_exc()
            return PublicMethod.false_return(data='', msg='后台抛出异常，请查看日志')

    def update_user(self, request):
        try:
            user_id = request.values.get('user_id')
            user_name = request.values.get('user_name')
            user_password = request.values.get('user_password')
            user_obj = self.dao.get_user_by_id(user_id)
            user_obj.username = user_name
            user_obj.password = user_obj.password_to_hash(user_password)
            self.dao.update_user(user_obj)
            return PublicMethod.true_return(data='', msg='更新用户成功！')
        except Exception:
            traceback.print_exc()
            return PublicMethod.false_return(data='', msg='后台抛出异常，请查看日志')

    def add_user(self, request):
        try:
            username = request.values.get('user_name')
            password = request.values.get('user_password')
            self.dao.add_user(username=username, password=password)
            return PublicMethod.true_return(data='', msg='添加用户成功！')
        except Exception:
            return PublicMethod.false_return(data='', msg='后台抛出异常，请查看日志')




