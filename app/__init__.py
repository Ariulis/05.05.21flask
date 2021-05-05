from flask import Flask
from flask_admin import Admin
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from loguru import logger

from config import config
from .admin import HomeAdminView, UserAdminView

logger.add('log/debug.log', format="{time} {level} {message}", level="DEBUG", rotation='10 KB', compression='zip')

db = SQLAlchemy()
mail = Mail()
ckeditor = CKEditor()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Admin

    from .models import User
    admin = Admin(app, 'FlaskyApp', url='/', index_view=HomeAdminView())
    admin.add_views(UserAdminView(User, db.session))

    # Blueprints

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
