# encoding=utf-8
from app import db
from datetime import datetime
import bleach
from markdown import markdown


class Article(db.Model):
    '__tablename__' == 'article'
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(30))
    # 正文
    content = db.Column(db.Text)
    # 类型（原创/转载/翻译)
    type = db.Column(db.String(10))
    # 标签
    tags = db.Column(db.String(30))
    publish_time = db.Column(db.DateTime, index=True)
    update_time = db.Column(db.DateTime)
    # 文章简介
    introduce = db.Column(db.String(200))
    # 点击量
    read_count = db.Column(db.Integer)
    # 外键声明
    # role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # 用于缓存处理后的markdown文本
    body_html = db.Column(db.Text)

    # 多对多
    from app.models.blog_category import category_article
    category = db.relationship("Category", secondary=category_article)

    def __repr__(self):
        return '<Article %r>' % self.title

    def __init__(self, form=None):
        super(Article, self).__init__()
        if form:
            self.title = form['title']
            self.content = form['content']
            self.type = form['type']
            self.tags = form['tags']
            self.introduce = form['introduce']
            if not self.publish_time:
                self.publish_time = datetime.now()
            self.update_time = datetime.now()
            if str(form['type']) == str(1):
                self.type = '原创'
            elif str(form['type']) == str(2):
                self.type = '转载'
            else:
                self.type = '翻译'

    @staticmethod
    def on_changed_body(target, value, oldvalue, inittiator):
        # markdown() 函数初步把Markdown 文本转换成HTML
        # clean() 函数删除所有不在白名单中的标签
        # linkify() 函数, 把纯文本中的URL 转换成适当的<a> 链接
        allowed_tags = ['a', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img']
        # target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags,strip=True))
        # 这里没有使用clean()函数，因为pagedown的图片被过滤了
        target.body_html = bleach.linkify(markdown(value, output_format='html'))

    def serialize(self):
        '''
        将对象序列化为字典
        :param obj: 对象实例
        :return:字典 
        '''
        d = {
            "title": self.title,
            "type": self.type,
            "introduce": self.introduce,
            "publish_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "tags": self.tags,
        }
        # vars(obj),返回对象实例的所有属性的字典
        return d

# on_changed_body 函数注册在body 字段上，是SQLAlchemy“set”事件的监听程序，这意
# 味着只要这个类实例的body 字段设了新值，函数就会自动被调用。
db.event.listen(Article.content, 'set', Article.on_changed_body)
