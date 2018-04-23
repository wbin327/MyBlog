# encoding=utf-8
from dao import Dao
from app.util.public_method import PublicMethod
from app.models.blog_category import Category
import traceback
import os
from werkzeug.utils import secure_filename
import time
from flask import current_app
import json
from flask import render_template, redirect


class Service(object):
    """
    category表中存储所有的博客分类，分类有多个级别。一级栏目（也就是博客头部栏目）以father_id为0作为标识。
    father_id存储父节点的ID
    """
    def __init__(self):
        self.dao = Dao()

    def get_blog_header(self):
        try:
            return self.dao.get_blog_header()
        except Exception as e:
            traceback.print_exc()
            return []

    def delete_blog_header(self, header_id):
        try:
            blog_header = self.dao.getCategoryById(header_id)
            self.dao.delete_category(blog_header)
            return PublicMethod.true_return(data='删除成功', msg='success')
        except Exception as e:
            traceback.print_exc()
            return PublicMethod.false_return(data='删除异常，请修复', msg='error')

    def add_blog_header(self, name):
        try:
            header_obj = Category(name=name, father_id=0, father_name=0)
            self.dao.add_category(header_obj)
            return PublicMethod.true_return(data='新增成功', msg='success')
        except Exception as e:
            traceback.print_exc()
            return PublicMethod.false_return(data='新增异常，请修复', msg='error')

    def update_blog_header(self, id, name):
        try:
            header_obj = self.dao.getCategoryById(id)
            header_obj.name = name
            self.dao.update_category()
            return PublicMethod.true_return(data='更新成功', msg='success')
        except Exception as e:
            traceback.print_exc()
            return PublicMethod.false_return(data='更新异常，请修复', msg='error')

    def get_blog_siderbar(self):
        try:
            all_obj_list = self.dao.get_all_category()
            father_obj_list = self.dao.get_blog_header()
            son_list = []
            for father in father_obj_list:
                self.find_all_son(all_obj_list, father.id, son_list)
            return son_list, father_obj_list
        except Exception as e:
            traceback.print_exc()
            return [], []

    def find_all_son(self, category_list, id, result_list):
        """       
        :param category_list: 博客类别对象的列表(博客类别表中所有结果）
        :param id: 获取这个ID的所有儿子对象
        :param result_list: 所有的儿子对象保存在这个列表中
        :return: result_list
        """
        for category in category_list:
            if category.father_id == id:
                result_list.append(category)
                self.find_all_son(category_list, category.id, result_list)
        return result_list

    def add_sidebar(self, category_name, father_id, father_name):
        try:
            category_obj = Category(category_name, father_id, father_name)
            self.dao.add_category(category_obj)
            return PublicMethod.true_return(data='新增左侧边栏成功', msg='success')
        except Exception:
            traceback.print_exc()
            return PublicMethod.false_return(data='新增左侧边栏失败', msg='error')

    def update_sidebar(self, id, name, father_id, father_name):
        try:
            category_obj = self.dao.getCategoryById(id)
            category_obj.name = name
            category_obj.father_id = father_id
            category_obj.father_name = father_name
            self.dao.update_category()
            return PublicMethod.true_return(data='编辑左侧边栏成功', msg='success')
        except Exception:
            traceback.print_exc()
            return PublicMethod.false_return(data='编辑左侧边栏失败', msg='error')

    def delete_sidebar(self, id):
        try:
            category_obj = self.dao.getCategoryById(id)
            self.dao.delete_category(category_obj)
            return PublicMethod.true_return(data='删除左侧边栏成功', msg='success')
        except Exception:
            traceback.print_exc()
            return PublicMethod.false_return(data='删除左侧边栏失败', msg='error')

    def get_father_and_son(self, name):
        """
        通过传入的类别名，获取该类别所有儿子，返回所有父亲分类和该分类的所有儿子分类
        :param name: 父亲类别名称
        :return: 所有父亲分类以及该分类的所有儿子分类
        """
        try:
            father = self.dao.getCategoryByName(name)
            category_list = self.dao.get_all_category()
            son_list = []
            self.find_all_son(category_list, father.id, son_list)
            father_list = self.dao.get_blog_header()
            return father_list, son_list
        except Exception:
            traceback.print_exc()
            return [], []

    def upload_image(self, file, username):
        """
        上传文件，保存在static/upload_image/username文件夹下，
        首先判断是否支持上传的文件类型
        首先判断文件夹是否存在，如果没有该文件夹会自动创建。
        为了防止文件重名以及安全性问题，上传的文件统一以系统时间命名
        :param file: 文件流
        :param username: 用户名
        :return: json
        """
        try:
            if file and self.allowed_file(file.filename):
                if not os.path.isdir(current_app.config['UPLOAD_FOLDER']):
                    os.mkdir(current_app.config['UPLOAD_FOLDER'])
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], username)             
                if os.path.isdir(path):
                    image_path = self.save_image2(path, file, username)
                else:
                    os.mkdir(path)
                    image_path = self.save_image2(path, file, username)
                return PublicMethod.true_return(data=image_path, msg='上传图片成功')
            else:
                return PublicMethod.false_return(data='error', msg='该类型文件无法上传')
        except Exception:
            traceback.print_exc()
            return PublicMethod.false_return(data='error', msg='图片上传失败，请联系管理员')

    def save_image2(self, path, file, username):
        file_type = file.filename.rsplit('.', 1)[1]
        new_file_name = time.strftime("%Y-%m-%d_%H%M%S", time.localtime()) + '.' + file_type
        upload_path = os.path.join(path, new_file_name)
        file.save(upload_path)
        image_path = '/static/uploads/' + username + '/' + new_file_name
        return image_path

    def get_path_msg(self, path):
            """
            遍历该目录，获取目录的绝对路径，该目录下所有文件和文件夹
            :param path: 文件夹路径
            :return: 
            root:str,绝对路径。
            dirs:列表，该目录下所有文件夹名
            files:列表，该目录下所有文件名
            """
            for root, dirs, files in os.walk(path):
                '''
                print(root) #当前目录路径  
                print(dirs) #当前路径下所有子目录  
                print(files) #当前路径下所有非目录子文件 
                '''
                return root, dirs, files

    def save_image(self, path, file_name, file):
        # 获取该路径绝对地址,该路径下的目录名，该路径下的文件名
        root, dirs, files = self.get_path_msg(path)
        # 判断文件夹下是否存在重名文件，如果重名，将以当前系统时间为文件名
        if file_name not in files:
            upload_path = os.path.join(path, file_name)
            file.save(upload_path)
        else:
            file_type = file_name.rsplit('.', 1)[1]
            file_name = time.strftime("%Y-%m-%d %H%M%S", time.localtime()) + '.' + file_type
            upload_path = os.path.join(path, file_name)
            file.save(upload_path)

    def add_article(self, form, user):
        try:
            from app.models.article import Article
            article = Article(form=form)
            article.user_id = user.id
            article.read_count = 0
            category = self.dao.getCategoryById(form['category'])
            article.category = [category]
            self.dao.add_article(article)
            return PublicMethod.true_return(data='', msg=u'发布成功')
        except Exception,e:
            traceback.print_exc()
            return PublicMethod.false_return(data='', msg=u'后台报错，请联系管理员')

    def allowed_file(self, filename):
        # 这里需要注意的是windows系统里的文件后缀可能是大写或小写，需要先将其统一转化成小写再进行判断
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    def get_blog_by_header(self, son_list, page):
        """
        获取一级类别的所有博客
        :param son_list: 一级类别的所有子类别
        :param page:分页,每页五篇博客
        :return: 博客list
        """
        try:

            article_list = []
            for son in son_list:
                for article in son.article:
                    article_list.append(article)
            if not article_list:
                # 根据时间顺序排序, reverse=True升序排序，key根据关键字进行排序
                article_list.sort(key=lambda blog: blog.update_time, reverse=True)
            # 不知什么原因列表未能升序排序，这里将其反转
            article_list.reverse()
            start = (page-1)*5
            return article_list[start:start+5]
        except Exception:
            traceback.print_exc()

    def page_count(self, header):
        try:
            father = self.dao.getCategoryByName(header)
            father_list, son_list = self.get_father_and_son(header)
            article_list = []
            for son in son_list:
                article_list = article_list + son.article
            article_count = len(article_list)
            page_count = article_count/5
            if not article_count % 5 == 0:
                page_count += 1
            return 1, page_count
        except Exception:
            traceback.print_exc()

    def get_blog_by_sidebar(self, sidebar_obj, page):
        sidebar_obj.article.sort(key=lambda blog: blog.update_time)
        # 列表反转
        sidebar_obj.article.reverse()
        start = (page-1)*5
        return sidebar_obj.article[start:start+5]

    def get_blog_by_header_and_sidebar(self, header, sidebar, page):
        try:

            if not page:
                page = 1
            else:
                # str.isdigit()如果字符串只包含数字则返回 True 否则返回 False。
                # filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。
                page = int(filter(str.isdigit, page.encode("utf-8")))
            if header and not sidebar:
                father_list, son_list = self.get_father_and_son(header)
                article_list = self.get_blog_by_header(son_list, page=page)
                start_page, end_page = self.page_count(header=header)
                return render_template('/blog/content.html', father_list=father_list, son_list=son_list,
                                       start_page=start_page, end_page=end_page, article_list=article_list,
                                       header=header, page=int(page))
            elif header and sidebar:
                father_list, son_list = self.get_father_and_son(header)
                sidebar_obj = None
                for son in son_list:
                    if son.name == sidebar:
                        sidebar_obj = son
                article_list = self.get_blog_by_sidebar(sidebar_obj, page=page)
                article_count = len(sidebar_obj.article)
                page_count = article_count / 5
                if not article_count % 5 == 0:
                    page_count += 1
                return render_template('/blog/content.html', father_list=father_list, son_list=son_list,
                                       start_page=1, end_page=page_count, article_list=article_list,
                                       header=header, page=int(page), sidebar=sidebar)
        except Exception:
            traceback.print_exc()
            return redirect('/blog/error')

    def get_all_header(self):
        return self.dao.get_blog_header()

    def get_sidebar_by_blogID(self, blog_id):
        try:
            # 博客阅读量加一
            article = self.dao.get_article_by_id(blog_id)
            article.read_count += 1
            self.dao.update_article(article)

            father_list = self.get_blog_header()
            son_list = self.dao.get_second_category(article.category[0].father_id)
            return render_template('/blog/read_blog.html', father_list=father_list, son_list=son_list,
                                   article=article)
        except Exception:
            traceback.print_exc()
            return redirect('/blog/error')

    def get_article(self, blog_id):
        article = self.dao.get_article_by_id(blog_id)
        return article

    def download_content(self, blog_id):
        try:
            article = self.dao.get_article_by_id(blog_id)
            if article:
                return PublicMethod.true_return(data=article.content, msg='获取博客内容成功!')
            else:
                return PublicMethod.false_return(data='', msg='articl对象为空，具体原因请查看后台日志')
        except Exception:
            traceback.print_exc()
            return PublicMethod.false_return(data='', msg='后台抛出异常，请查看后台日志')
