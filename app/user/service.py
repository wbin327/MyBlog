# encoding=utf-8
# from .ServiceInterface import ServiceInterface
import time
from flask import jsonify
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

    def get_father_by_user(self):
        try:
            father_list = self.dao.get_blog_header()
            return father_list
        except Exception:
            traceback.print_exc()
            return PublicMethod.false_return(data='', msg='后台抛出异常，请查看日志')

    def get_son_list(self, request):
        try:
            father_id = request.values.get('father_id')
            if father_id:
                category_list = self.dao.get_son_by_father(father_id)
                son_list = []
                func = lambda id, name: {'id': id, 'name': name}
                for category in category_list:
                    son_list.append(func(category.id, category.name))
                return jsonify(PublicMethod.true_return(data=son_list, msg='请求成功'))
            else:
                return jsonify(PublicMethod.false_return(data='', msg='请求参数有误，请求失败'))
        except Exception:
            traceback.print_exc()
            return jsonify(PublicMethod.false_return(data='', msg='后台报错，请查看日志'))

    def get_blog_list(self, request):
        try:
            son_id = request.values.get('son_id')
            # 要将字符型转整型，负责sql查询结果为空
            son_id = int(filter(str.isdigit, son_id.encode("utf-8")))
            if son_id:
                category = self.dao.get_category_by_id(son_id)
                blog_list = []
                func = lambda id, title: {'id': id, 'title': title}
                for article in category.article:
                    blog_list.append(func(article.id, article.title))
                return jsonify(PublicMethod.true_return(data=blog_list, msg='请求成功'))
            else:
                return jsonify(PublicMethod.false_return(data='', msg='请求的参数有误，请求失败'))
        except Exception:
            traceback.print_exc()
            return jsonify(PublicMethod.false_return(data='', msg='后台报错，请查看日志'))

    def delete_blog(self, request):
        try:
            blog_id = request.values.get('blog_id')
            # 要将字符型转整型，负责sql查询结果为空
            blog_id = int(filter(str.isdigit, blog_id.encode("utf-8")))
            if blog_id:
                article = self.dao.get_article_by_id(blog_id)
                excute = self.dao.delete_article(article)
                if excute:
                    return jsonify(PublicMethod.true_return(data='', msg='删除成功'))
                else:
                    return jsonify(PublicMethod.flase_return(data='', msg='删除失败'))
        except Exception:
            traceback.print_exc()
            return jsonify(PublicMethod.false_return(data='', msg='后台报错，请查看日志'))





