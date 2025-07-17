import os
from flask import Flask
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# User 클래스 정의 (Flask-Login UserMixin 포함)
class User(UserMixin):
    def __init__(self, username, name, is_admin):
        self.id = username  # user_id로 username 사용
        self.name = name
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    import sqlite3
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT username, name, is_admin FROM users WHERE username=?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

def create_app():
    app = Flask(__name__)

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(base_dir, 'config.py')

    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)
    else:
        raise FileNotFoundError(f"Config file not found at {config_path}")

    # LoginManager 초기화
    login_manager.init_app(app)

    # 블루프린트 import 및 등록
    from app.auth.routes import auth_bp
    from app.files.routes import files_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(admin_bp)

    upload_folder = app.config.get('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    return app
