# app/__init__.py
from flask import Flask
import os
from config import UPLOAD_FOLDER
from app.auth.routes import auth_bp
from app.files.routes import files_bp
from app.admin.routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # 블루프린트 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(admin_bp)

    # 업로드 폴더 생성
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    return app
