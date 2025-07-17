import os
from flask import Flask
from flask_login import LoginManager
from models import db  # models.py에서 SQLAlchemy db 객체 임포트
from app.auth.routes import auth_bp
from app.files.routes import files_bp
from app.admin.routes import admin_bp

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(base_dir, 'config.py')

    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)
    else:
        raise FileNotFoundError(f"Config file not found at {config_path}")

    # SQLAlchemy 및 LoginManager 초기화
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(admin_bp)

    upload_folder = app.config.get('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User  # 순환 임포트 방지 위해 내부 임포트
    return User.query.get(int(user_id))
