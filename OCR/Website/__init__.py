from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
db_name = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='ABC'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    

    from .models import user, Doc
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        if id is not None:
            return user.query.get(int(id))
        else:
            return None

    return app

    

def create_database(app):
    with app.app_context():
        if not path.exists('website/'+db_name):
            db.create_all()
            print('Database Created')
