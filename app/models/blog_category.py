#encoding=utf-8
from app import db

# 用于联系多对多关系的中间表，存储两个表的主键
category_article = db.Table('category_article',
                            db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
                            db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True))


class Category(db.Model):
    '__tablename__' == 'category'
    id = db.Column(db.Integer, primary_key=True)
    father_id = db.Column(db.Integer)
    father_name = db.Column(db.String(20))
    name = db.Column(db.String(20))
    # 多对多关系
    # 在父表中的 relationship() 方法传入 secondary 参数，其值为关联表的表名
    # category_article = db.relationship('Article', secondary=category_article, lazy='dynamic',backref=db.backref('category', lazy='dynamic'))
    article = db.relationship("Article", secondary=category_article)

    def __init__(self, name, father_id, father_name):
        self.name = name
        self.father_id = father_id
        self.father_name = father_name



