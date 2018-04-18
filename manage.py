# encoding=utf-8
'''
顶级文件夹中的 manage.py 文件用于启动程序。
'''


import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models.article import Article
from app.models.role import Role
from app.models.user import User
from app.models.permission import Permission
from app.models.blog_category import Category, category_article

app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)


# 用于给python shell添加上下文，打开python shell时会自动声明以下变量
def make_shell_context():
    return dict(
        app=app,
        db=db,
        Article=Article,
        User=User,
        Role=Role,
        category_article=category_article,
        Category=Category,
        user_wbin=User(username='wbin', password='pbkdf2:sha256:50000$NwxAD0HW$5d00de6484b6c9483526b3f840464fd77b28be85'+
'f67c86ac429f2ee09a88dc40'),
        role_admin=Role(name='admin', permissions=Permission.ADMINISTER),
    )
manager.add_command("shell", Shell(make_context=make_shell_context))
# 添加db命令
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # manager.run()
