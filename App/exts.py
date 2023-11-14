from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
cache = Cache(config={'CACHE_TYPE': 'simple'})

def init_exts(fn):
    db.init_app(app=fn)
    migrate.init_app(app=fn,db=db)
    cache.init_app(app=fn)



