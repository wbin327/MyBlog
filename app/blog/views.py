# encoding=utf-8
from flask import render_template, request, jsonify, session, redirect, url_for, flash
from . import blog
from service import Service
from app.util.root_decorators import admin_required, write_required
from flask_login import login_required, logout_user, current_user
from ArticleForm import ArticleForm
import traceback
from ..user.service import Service as UserService

service = Service()
user_service = UserService()


@blog.route('/background/blog_header')
@login_required
@admin_required
def blog_header():
    header_list = service.get_blog_header()
    return render_template('/background/blog_category/blog_header.html', header_list=header_list)


@blog.route('/background/delete_blog_header', methods=['post'])
@login_required
@admin_required
def delete_blog_header():
    header_id = request.values.get('header_id')
    json = service.delete_blog_header(header_id)
    return jsonify(json)


@blog.route('/background/add_blog_header', methods=['post'])
@login_required
@admin_required
def add_blog_header():
    header_name = request.values.get('header_name')
    json = service.add_blog_header(header_name)
    return jsonify(json)


@blog.route('/background/update_blog_header', methods=['post'])
@login_required
@admin_required
def update_blog_header():
    header_name = request.values.get('header_name')
    header_id = request.values.get('header_id')
    json = service.update_blog_header(header_id, header_name)
    return jsonify(json)


'''博客左边栏管理'''


@blog.route('/background/blog_sidebar')
@login_required
@admin_required
def blog_siderbar():
    sidebar_list, father_list = service.get_blog_siderbar()
    return render_template('/background/blog_category/blog_sidebar.html', sidebar_list=sidebar_list,
                           father_list=father_list)


@blog.route('/background/add_sidebar', methods=['post'])
@login_required
@admin_required
def add_sidebar():
    category_name = request.values.get('name')
    father_id = request.values.get('father_id')
    father_name = request.values.get('father_name')
    json_dict = service.add_sidebar(category_name, father_id, father_name)
    return jsonify(json_dict)


@blog.route('/background/update_sidebar', methods=['post'])
@login_required
@admin_required
def update_sidebar():
    id = request.values.get('id')
    name = request.values.get('name')
    father_id = request.values.get('father_id')
    father_name = request.values.get('father_name')
    json_dict = service.update_sidebar(id, name, father_id, father_name)
    return jsonify(json_dict)


@blog.route('/background/delete_sidebar', methods=['post'])
@login_required
@admin_required
def delete_sidebar():
    id = request.values.get('id')
    json_dict = service.delete_sidebar(id)
    return jsonify(json_dict)


'''博客首页'''
@blog.route('/index')
def blog_index():
    header_list = service.get_blog_header()
    return render_template('/blog/index.html', header_list=header_list)


@blog.route('/get_blog')
def get_blog_by_category():
    # 获取url, ?后的值
    header = request.args.get('header')
    page = request.args.get('page')
    sidebar = request.args.get('sidebar')
    return service.get_blog_by_header_and_sidebar(header=header, page=page, sidebar=sidebar)


def get_blog_by_sidebar():
    sidebar_id = request.values.get('sidebar_id')
    data = service.get_blog_by_sidebar(sidebar_id)
    return jsonify(data)


@blog.route('/to_write_blog')
def to_write_blog():
    if current_user.is_authenticated:
        return redirect('/blog/write_blog')
    else:
        return render_template('/blog/login.html')


@blog.route('/login')
def login():
    return render_template('/blog/login.html')


@blog.route('/login_check')
def login_check():
    username = request.values.get('username')
    password = request.values.get('password')
    remember = request.values.get('remember')
    if remember == 'true':
        remember = True
    else:
        remember = False
    result = user_service.background_login_check(username, password, remember=remember, session=session)
    return jsonify(result)


@blog.route('/logout')
@login_required
def logout():
    logout_user()
    session['userinfo'] = None
    flash('您已退出系统！')
    return redirect('/blog/index')


@blog.route('/write_blog', methods=['get', 'post'])
@login_required
@write_required
def write_blog():
    form = ArticleForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = current_user
        json = service.add_article(request.form, user)
        if json['status']:
            return render_template('/blog/write_blog.html', form=form, json=json, article=None)
        else:
            return render_template('/blog/write_blog.html', form=form, json=json, article=None)
    else:
        return render_template('/blog/write_blog.html', form=form, json=None, article=None)


@blog.route('/edit_blog/<int:blog_id>', methods=['get', 'post'])
@login_required
@write_required
def edit_blog(blog_id):
    try:
        form = ArticleForm()
        article = service.get_article(blog_id)
        if article:
            form.title.data = article.title
            form.tags.data = article.tags
            form.introduce.data = article.introduce
            form.type.data = article.type
        if form.validate_on_submit() and request.method == 'POST':
            user = current_user
            json = service.add_article(request.form, user)
            if json['status']:
                return render_template('/blog/edit_blot.html', form=form, json=json, blog_id=article.id)
            else:
                return render_template('/blog/edit_blog.html', form=form, json=json, blog_id=article.id)
        else:
            return render_template('/blog/edit_blog.html', form=form, json=None, blog_id=article.id)
    except Exception:
        traceback.print_exc()
        return redirect('/blog/error')


@blog.route('/download_content', methods=['get'])
def download_content():
    blog_id = request.values.get('blog_id')
    json = service.download_content(blog_id)
    return jsonify(json)


@blog.route('/upload_image', methods=['post'])
@login_required
@write_required
def upload_image():
    try:
        f = request.files['file']
        result = service.upload_image(f, current_user.username)
        return jsonify(result)
    except Exception:
        traceback.print_exc()


@blog.route('/read_blog/<int:blog_id>', methods=['get'])
def read_blog(blog_id):
    return service.get_sidebar_by_blogID(blog_id)


@blog.route('/error', methods=['get'])
def blog_error():
    return render_template('/blog/blog_error.html')

