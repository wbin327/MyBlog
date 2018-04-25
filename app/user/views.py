# encoding=utf-8
from datetime import datetime

from flask import render_template, request, jsonify, session, redirect, flash
from flask_login import login_required, logout_user, current_user

from app.util.root_decorators import admin_required
from service import Service
from . import user

service = Service()


@user.route('/login')
def test():
    return render_template('/user/login.html')


@user.route('/register', methods=['post'])
def register():
    name = request.form['name']
    password = request.form['password']
    result = service.register(name, password)
    return jsonify(result)


@user.route('/api_login_check', methods=['post'])
def login_check():
    username = request.values.get('username')
    password = request.values.get('password')
    # username = request.form['name']
    # password = request.form['password']
    result = service.login_check(username, password)
    return jsonify(result)


@user.route('/get_user', methods=['GET'])
def get():
    authorization = request.headers.get('Authorization')
    result = service.get_user(authorization)
    return jsonify(result)


@user.route('/to_background', methods=['get'])
@login_required
@admin_required
def to_background():
    return render_template('/background/background.html', current_time=datetime.now())


@login_required
def logout():
    authorization = request.headers.get('Authorization')
    result = service.logout(authorization)
    return jsonify(result)


@user.route('/sign_out', methods=['get'])
@login_required
def sign_out():
    logout_user()
    session['userinfo'] = None
    flash('您已退出系统！')
    return redirect('/user/login')


@user.route('/background_login_check', methods=['post'])
def background_login_check():
    username = request.values.get('username')
    password = request.values.get('password')
    remember = request.values.get('remember')
    if remember == 'true':
        remember = True
    else:
        remember = False
    result = service.background_login_check(username, password, remember=remember)
    return jsonify(result)


@user.route('/background/user_manage', methods=['get'])
@login_required
@admin_required
def user_manage():
    user_list = service.get_all_user()
    return render_template('/background/user_manage/user_manage.html', user_list=user_list)


@user.route('/background/delete_user', methods=['post'])
@login_required
@admin_required
def delete_user():
    json = service.delete_user(request)
    return jsonify(json)


@user.route('/background/add_user', methods=['post'])
@login_required
@admin_required
def add_user():
    json = service.add_user(request)
    return jsonify(json)


@user.route('/background/update_user', methods=['post'])
@login_required
@admin_required
def update_user():
    json = service.update_user(request)
    return jsonify(json)


@user.route('/background/user_blog_manage', methods=['get'])
@login_required
@admin_required
def to_blog_manage():
    father_list = service.get_father_by_user()
    return render_template('background/user_manage/user_blog_manage.html', father_list=father_list)


@user.route('/background/get_son_list', methods=['post'])
@login_required
@admin_required
def get_son_list():
    return service.get_son_list(request)


@user.route('/background/get_blog_list', methods=['post'])
@login_required
@admin_required
def get_blog_list():
    return service.get_blog_list(request)


@user.route('/background/delete_blog', methods=['post'])
@login_required
@admin_required
def delete_blog():
    return service.delete_blog(request)


