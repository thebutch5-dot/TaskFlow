from flask import Flask
from flask_login import LoginManager
from app.database import db
from config import Config

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    with app.app_context():
        from app import models
        db.create_all()

    return app

