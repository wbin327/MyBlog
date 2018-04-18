# encoding=utf-8
from app import db
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError



class Dao(object):
    def query_all_user(self):
        return User.query.all()

    def query_user_by_name(self, name):
        return User.query.filter_by(username=name).first()

    def add_user(self, username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        return session_commit()

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def get_user_by_id(self, id):
        return User.query.filter_by(id=id).first()

    def get_all_user(self):
        return User.query.all()

    def delete_user(self, user):
        db.session.delete(user)
        return session_commit()

    def update_user(self, user):
        return session_commit()


def session_commit():
    try:
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason