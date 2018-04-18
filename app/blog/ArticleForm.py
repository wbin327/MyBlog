# encoding:utf-8
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, SelectField,TextAreaField
from wtforms.validators import DataRequired, Length
from app.models.blog_category import Category


class ArticleForm(FlaskForm):
    title = StringField(u"title", validators=[DataRequired(u'标题必填'), Length(min=2, max=20, message=u'标题必须介于2-20个字符')])
    category = SelectField(u"category", coerce=int)
    tags = StringField(u"tag", validators=[DataRequired(u'标签必填'),  Length(min=2, max=25, message=u'标签必须介于2-25个字符')])
    content = PageDownField(u"content", validators=[DataRequired()])
    submit = SubmitField(u"发布博客")
    type = SelectField(u'type', coerce=int, choices=[(1, u'原创'), (2, u'转载'), (3, u'翻译')])
    # 文章简介
    introduce = TextAreaField(u'introduce', validators=[DataRequired()])

    def __init__(self):
        super(ArticleForm, self).__init__()
        self.category.choices = [(category.id, category.name) for category in Category.query.filter(Category.father_id !=0)]


    def get_sidebar(self):
        father_list = Category.query.filter(father='!0')
        all_list = Category.query.all()



