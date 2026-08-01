from flask import Flask
from flask_login import LoginManager
from app.database import db, get_user_by_id
from config import Config

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.tasks.routes import tasks_bp
    from app.auth import auth_bp

    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)

    @app.before_request
    def before_request():
        if db.is_closed():
            db.connect()

    @app.teardown_request
    def teardown_request(exc):
        if not db.is_closed():
            db.close()

    with db:
        from app.models import User, Task
        db.create_tables([User, Task])

    return app

