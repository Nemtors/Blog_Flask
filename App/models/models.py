
from ..exts import db
# 一对多，一个分类可以有多个文章
# 分类模型
class CategoryModels(db.Model):
    __tablename__ = 'tb_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    describe = db.Column(db.Text(), default='describe')
    #获取分类下所有文章
    articles = db.relationship('ArticleModel',backref='category',lazy='dynamic')
# 文章
class ArticleModel(db.Model):
    __tablename__ = 'tb_article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    keyword = db.Column(db.String(255), default='keyword')
    content = db.Column(db.Text(), default='content')
    img = db.Column(db.Text(), default='img')
    # 所属分类,外键
    category_id = db.Column(db.Integer,db.ForeignKey(CategoryModels.id))
# 相册
class PhotoModel(db.Model):
    __tablename__ = 'tb_photo'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    url = db.Column(db.Text())
    name = db.Column(db.String(30),unique=True)
    describe = db.Column(db.Text(),default='describe')