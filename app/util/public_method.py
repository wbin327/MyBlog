# encoding=utf-8
'''
工具类
'''
import datetime
from config import DevelopmentConfig


class PublicMethod(object):

    @staticmethod
    def true_return(data, msg):
       return {
           "status": True,
           "data": data,
           "msg": msg
       }

    @staticmethod
    def false_return(data, msg):
       return {
           "status": False,
           "data": data,
           "msg": msg
       }

    @staticmethod
    def serialize_instance(obj):
        '''
        将对象序列化为字典
        :param obj: 对象实例
        :return:字典 
        '''
        # d = {'classname': type(obj).__name__}
        d = {}
        # vars(obj),返回对象实例的所有属性的字典
        d.update(vars(obj))
        return d


if __name__ == '__main__':
    print PublicMethod.verify_password('wbin')
