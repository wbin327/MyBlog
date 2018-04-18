# encoding=utf-8
'''
这个类拦截了ServiceInterface类的实例化，并为其实例化对应的实现类（ServiceInterfaceImpl）
'''
from .ServiceInterfaceImpl import ServiceInterfaceImpl

# 自定义映射字典,key为接口类名称,value为实现类对象
mapper = {'ServiceInterface': ServiceInterfaceImpl}


class MyType(type):

    def __call__(cls, *args, **kwargs):
        try:
            if cls.__name__ in mapper:
                # 实例化类对象(实例化类对象会为该实例开辟内存空间)
                obj = mapper[cls.__name__].__new__(mapper[cls.__name__])
                # 初始化实例
                obj.__init__()
                return obj
        except Exception, e:
            raise e
            return 'mapper errors'
