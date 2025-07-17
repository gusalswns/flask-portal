# app/__init__.py
import os
from flask import Flask
from app.auth.routes import auth_bp
from app.files.routes import files_bp
from app.admin.routes import admin_bp

def create_app():
    app = Flask(__name__)

    # 현재 파일 기준 상위 폴더(myapp/) 경로 구하기
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(base_dir, 'config.py')

    # config.py 파일 존재 여부 확인 후 로드
    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)
    else:
        raise FileNotFoundError(f"Config file not found at {config_path}")

    # 블루프린트 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(admin_bp)

    # 업로드 폴더 생성 (config에서 경로 읽기)
    upload_folder = app.config.get('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    return app
