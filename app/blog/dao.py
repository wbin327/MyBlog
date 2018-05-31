# encoding=utf-8
from app import db
from app.models.blog_category import Category
from app.models.article import Article
from app.util.public_method import PublicMethod
from sqlalchemy.exc import SQLAlchemyError


class Dao(object):
    def __init__(self):
        pass

    def get_blog_header(self):
        return Category.query.filter_by(father_id=0)

    def getCategoryById(self, id):
        return Category.query.filter_by(id=id).first()

    def delete_category(self, category_obj):
        db.session.delete(category_obj)
        return session_commit()

    def add_category(self, category_obj):
        db.session.add(category_obj)
        return session_commit()

    def update_category(self):
        return session_commit()

    def get_all_category(self):
        return Category.query.all()

    def get_article_orderby_time(self, blog_id, startnum, endnum):
        return Article.query.filter_by(id=blog_id).order_by(Article.publish_time)[startnum: endnum]

    def getCategoryByName(self, name):
        return Category.query.filter_by(name=name).first()

    def add_article(self, article):
        db.session.add(article)
        return session_commit()

    def get_article_by_id(self, blog_id):
        return Article.query.filter_by(id=blog_id).first()

    def get_second_category(self, father_id):
        return Category.query.filter_by(father_id=father_id)

    def update_article(self, article):
        db.session.add(article)
        return session_commit()

    def session_commit(self):
        session_commit()

    def search_blog(self, condition):

        return Article.query.filter(Article.title.like('%'+condition+'%')).all()



def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e