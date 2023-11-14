import time
from flask import Blueprint, request, render_template, url_for
from ..models.models_admin import *
from ..models.models import *
from ..exts import cache
blue = Blueprint('usr',__name__)

@blue.route('/')
@blue.route('/index/')
def blog_index():
    #photos = PhotoModel.query.limit(6)# 传图片
    categorys = CategoryModels.query.all() # 传递分类
    articles = ArticleModel.query.limit(4) #取出文章内容
    return render_template('home/index.html',categorys=categorys
                           ,articles=articles)
# 相册页面
@blue.route('/photos/')
def blog_photos():
    photos = PhotoModel.query.all()
    return render_template('home/photos.html',photos=photos)
# 日记
@blue.route('/article/')
def blog_article():
    categorys = CategoryModels.query.all()
    articles = ArticleModel.query.all()
    return render_template('home/article.html',categorys=categorys,articles=articles)
# 个人简介
@blue.route('/about/')
def blog_about():
    photos = PhotoModel.query.limit(6)
    categorys = CategoryModels.query.all()
    return render_template('home/about.html',categorys=categorys,photos=photos)

