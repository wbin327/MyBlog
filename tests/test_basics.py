# encoding=utf-8
import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    # setUp方法会在测试前执行
    def setUp(self):
        # 以测试设置创建程序
        self.app = create_app('testing')
        # 创建程序上下文
        self.app_context = self.app.app_context()
        self.app_context.push()
        # 创建数据库
        db.create_all()

    # tearDown方法会在测试后执行
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    '''
    下面的是需要测试的内容
    '''
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
