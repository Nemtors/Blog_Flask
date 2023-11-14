from ..exts import db
# 做后台登录
class AdminUserModel(db.Model):
    __tablename__ = 'tb_admin'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(30),unique=True)
    passwd = db.Column(db.String(30))