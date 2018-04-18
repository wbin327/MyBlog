# encoding=utf-8
from mapper import MyType


class ServiceInterface(object):
    # 拦截ServiceInterface对象的实例化，实例化接口对象时，会通过字典映射到接口实现类
    __metaclass__ = MyType

    # 用户认证接口
    def login_check(self, name, password):
        pass

    # 用户注册接口
    def register(self, name, password):
        pass

    def get_user(self, authorization):
        pass

