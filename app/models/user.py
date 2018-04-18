# encoding=utf-8
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from app.models.permission import Permission
from flask_login import UserMixin


class User(UserMixin, db.Model):
    '__tablename__' == 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, index=True)
    password = db.Column(db.String(256))
    login_time = db.Column(db.Float)
    # 外键声明
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    # 一对多关系模型
    article = db.relationship('Article', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.password = self.password_to_hash(password)

    def can(self, permissions):
        return self.role.permissions & permissions == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return '<User %r>' % self.username

    def password_to_hash(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def serialize(self):
        data = {
            'username': self.username,
            'login_time': self.login_time,
            'role_id': self.role_id,
        }
        return data


def session_commit():
    try:
        db.session.commit()
        return 'success'
    except SQLAlchemyError as e:
        db.session.rollback()
        print e
        reason = str(e)
        return reason


if __name__ == '__main__':
    print generate_password_hash('123456')

