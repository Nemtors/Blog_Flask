import time
from flask import Blueprint, request, render_template, url_for, redirect, jsonify
from ..models.models_admin import *
from ..models.models import *
from ..exts import cache
admin = Blueprint('admin',__name__)
#后台首页
@admin.route('/admin/index/')
@admin.route('/admin/')
def index():
    #获取cookie,得到登录用户
    user_id = request.cookies.get('user_id',None)
    if user_id:
        #登录成功，有cookie内容
        user = AdminUserModel.query.get(user_id)#找到cookie的用户
        #传入分类 文章 相册的总数
        categorys = CategoryModels.query.filter()
        articles = ArticleModel.query.filter()
        photos = PhotoModel.query.filter()
        return render_template('admin/index.html',username=user.name,
                               categorys=categorys,
                               articles=articles,photos=photos)
    else:
        #没有登录过则跳转至login页面
        return render_template('admin/login.html')
#后台登录页面
@admin.route('/admin/login/',methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    elif request.method == 'POST':
        username = request.form.get('username') # 用户名
        userpwd = request.form.get('userpwd') # 密码
        # 登录验证,查到了有匹配的值，那么user是有值的
        user = AdminUserModel.query.filter_by(name=username,passwd=userpwd).first()
        if user: # 登录成功
            response = redirect('/admin/')#登录成功则跳转首页
            response.set_cookie('user_id',str(user.id),max_age=3*24*3600)#设置cookie 3天登录期限
            return response
        else:
            return 'Login Failed 密码或用户名错误'

#退出登录页面
@admin.route('/admin/logout/')
def admin_logout():
    response = redirect('/admin/login/')
    response.delete_cookie('user_id') #删除cookie
    return response

#分类管理页面
@admin.route('/admin/category/')
def admin_category():
    user_id = request.cookies.get('user_id',None)
    if user_id:
        username = AdminUserModel.query.get(user_id).name
        categorys = CategoryModels.query.all()
        return render_template('admin/category.html',username=username,categorys=categorys)
    else:
        return redirect('/admin/login/')

#添加分类功能
@admin.route('/admin/addcategory/',methods=['GET','POST'])
def admin_addcategory():
    user_id = request.cookies.get('user_id',None)
    if user_id:
        if request.method == 'POST':
            # 添加分类,获取前端传过来的数据
            name = request.form.get('name')
            describe = request.form.get('describe')
            category = CategoryModels()
            category.name = name
            category.describe = describe
            try:#做判断
                db.session.add(category)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
            return redirect('/admin/category/')
        else:
            return '请求方式错误'
    else:
        return redirect('/admin/login/')

#分类删除功能
@admin.route('/admin/delcategory/',methods=['GET','POST'])
def admin_delcategory():
    if request.method == 'POST':
        id = request.form.get('id')#得到前端提交的id数据
        category = CategoryModels.query.get(id)
        try:
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('e')
        return 'Success'
    else:
        return '请求出错'

#修改分类
@admin.route('/admin/updatecategory/<id>/',methods=['GET','POST'])
def admin_updatecategory(id):
    category = CategoryModels.query.get(id)
    if request.method == 'GET':
        user_id= request.cookies.get('user_id')
        username = AdminUserModel.query.get(user_id).name
        return render_template('admin/category_update.html', username=username, category=category)
    elif request.method == 'POST': #提交修改分类
        name = request.form.get('name')
        describe = request.form.get('describe')
        category.name = name
        category.describe = describe
        try:
            db.session.commit()
        except Exception as e:
            print('e')
        return redirect('/admin/category/')

    else:
        return '请求方式错误'

#文章管理
@admin.route('/admin/article/')
def admin_article():
    user_id = request.cookies.get('user_id',None)
    if user_id:
        username = AdminUserModel.query.get(user_id).name
        articles = ArticleModel.query.all()
        return render_template('admin/article.html',username=username,articles=articles)
    else:
        return redirect('/admin/login/')

#添加文章
@admin.route('/admin/addarticle/',methods=['GET','POST'])
def add_article():
    if request.method == 'GET':
        user_id = request.cookies.get('user_id', None)
        username = AdminUserModel.query.get(user_id).name
        articles = ArticleModel.query.all()
        categorys = CategoryModels.query.all()
        return render_template('admin/article_add.html',username=username,articles=articles,categorys=categorys)
    elif request.method == 'POST':
        name = request.form.get('name')
        keywords = request.form.get('keywords')
        content = request.form.get('content')
        category = request.form.get('category')
        img = request.files.get('img') #取图片数据
        #图片的存储路径
        img_name = img.filename
        img_url = f'/static/home/uploads/{img_name}'
        #添加文章
        try:
            article = ArticleModel()
            article.name = name
            article.keyword = keywords
            article.content = content
            article.img = img_url
            article.category_id = category
            db.session.add(article)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
        else:#如果try成功则手动将文件路径存入本地
            img_data = img.read() #将图片数据读出来
            with open(f'App{img_url}','wb',) as fp: #通过项目目录来找
                fp.write(img_data)
                fp.flush()
        return redirect('/admin/article/')

#修改文章
#修改其中一篇文章，更改路由
@admin.route('/admin/updatearticle/<id>/',methods=['GET','POST'])
def update_article(id):
    user_id = request.cookies.get('user_id', None)
    username = AdminUserModel.query.get(user_id).name
    article = ArticleModel.query.get(id)
    categorys = CategoryModels.query.all()
    #点击更新
    if request.method == 'GET':

        return render_template('admin/article_update.html',username=username,article=article,categorys=categorys)
    elif request.method == 'POST':
        name = request.form.get('name')
        keywords = request.form.get('keywords')
        content = request.form.get('content')
        category = request.form.get('category')
        img = request.files.get('img')  # 取图片数据
        # 修改图片的存储路径至uploads
        img_name = img.filename
        img_url = f'/static/home/uploads/{img_name}'
        # 修改文章
        try:
            article.name = name
            article.keyword = keywords
            article.content = content
            article.img = img_url
            article.category_id = category
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
        else:  # 如果try成功则手动将文件路径存入本地
            img_data = img.read()  # 将图片数据读出来
            with open(f'App{img_url}', 'wb', ) as fp:  # 通过项目目录来找
                fp.write(img_data)
                fp.flush()
        return redirect('/admin/article/')
#后台删除文章
@admin.route('/admin/delarticle/',methods=['GET','POST'])
def del_article():
    if request.method == "POST":
        id = request.form.get('id')
        article = ArticleModel.query.get(id)
        try:
            db.session.delete(article)
            db.session.commit()
        except Exception as e:
            print('e:',e)
        return '成功'