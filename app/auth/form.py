# encoding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    name = StringField(u'用户名', validators=[DataRequired(message=u'用户名不能为空'), Length(1,10)])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'密码不能为空')])
    submit = SubmitField(u'登录')