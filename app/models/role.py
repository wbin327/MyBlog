# encoding=utf-8
from app import db
from app.models.permission import Permission


class Role(db.Model):
    '__tablename__' == 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    permissions = db.Column(db.Integer)

    '''
    一对多关系模型
    db.relationship() 中的 backref 参数向 User 模型中添加一个 role 属性，从而定义反向关系。
    这一属性可替代 role_id 访问 Role 模型，此时获取的是模型对象，而不是外键的值。
    对于一个 Role 类的实例，其 users 属性将返回与角色相关联的用户组成的列表。
    lazy = 'dynamic',禁止自动执行查询，如果不关闭自动查询，在执行user_role.users表达式时会调用all()返回一个用户列表。
    自动查询的话，无法指定更精确的查询过滤器
    '''
    # users = db.relationship('User', backref='role', lazy='dynamic')
    users = db.relationship('User', backref='role')

    def __init__(self, name, permissions=Permission.DEFAULT):
        self.name = name
        self.permissions = permissions

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        '''
        向数据库中填入角色
        :return: None
        '''
        roles = {
            'user': Permission.COMMENT | Permission.WRITE_ARTICLES,
            'administrator': Permission.ADMINISTER,
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = roles[r]
                db.session.add(role)
        db.session.commit()


