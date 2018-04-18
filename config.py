# encoding=utf-8
import os
'''
os.path.abspath(path) ,返回path规范化的绝对路径。 
os.path.dirname(path) ,返回path的目录。
__file__ , 指本行语句所在源文件的文件名
basedir = 'E:\PythonWrokSpace\MyBlog'
'''
basedir = os.path.abspath(os.path.dirname(__file__))


'''
设定多个配置，分别是开发、测试和生产环境的配置
config类设置通用配置，子类分别定义专用的配置
为了让配置方式更灵活且更安全，某些配置可以从环境变量中导入。例如， SECRET_KEY 的值，
这是个敏感信息，可以在环境中设定，但系统也提供了一个默认值，以防环境中没有定义。
'''
class Config:
        # 设置文件上传路径
        UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
        # 设置允许文件上传的格式
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'bmp', 'gif'])
        # os.environ.get('key'),从环境变量中导入
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'haha'
        SQLALCHEMY_COMMIT_ON_TEARDOWN = True
        # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
        # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
        # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

        @staticmethod   # 静态方法声明
        def init_app(app):
            pass


class DevelopmentConfig(Config):
        DEBUG = True
        # MAIL_SERVER = 'smtp.googlemail.com'
        # MAIL_PORT = 587
        # MAIL_USE_TLS = True
        # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
        # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
        '''
        数据库url
        mysql的url:mysql://username:password@hostname/database
        '''

        SQLALCHEMY_DATABASE_URI = os.environ.get('MYBLOG_DATABASE_URL') or  'mysql://root:123456@localhost/test'
        # 禁用以下的设置，不关闭会增加很大开销
        SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = os.environ.get('MYBLOG_DATABASE_URL') or \
                                  'mysql://root:123456@localhost/test'
        # 设置每次请求结束后自动提交数据库中变动
        SQLALCHEMY_COMMIT_ON_TEARDOWN = True
        # 禁用以下的设置，不关闭会增加很大开销
        SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
        SQLALCHEMY_DATABASE_URI = os.environ.get('MYBLOG_DATABASE_URL') or  'mysql://root:123456@localhost/test'
        # 禁用以下的设置，不关闭会增加很大开销
        SQLALCHEMY_TRACK_MODIFICATIONS = False

   

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }

if __name__ == '__main__':
    print os.environ.get('MYBLOG_DATABASE_URL')

