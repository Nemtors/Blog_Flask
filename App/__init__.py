from flask import Flask
from .views.views import blue
from .exts import init_exts
from .views.views_admin import admin
def create_app():
    fn = Flask(__name__)
    fn.register_blueprint(blue)
    fn.register_blueprint(admin)
    db_uri = 'mysql+pymysql://root:123456@192.168.10.129:3306/blogdb'
    fn.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    init_exts(fn)
    return fn
