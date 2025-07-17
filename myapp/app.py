import os
from flask import Flask
from flask_login import LoginManager
from models import db, User  # models.py에서 가져옴

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)

    # 경로 문제 해결: 절대 경로로 config.py 불러오기
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, 'config.py')
    app.config.from_pyfile(config_path)

    # DB, 로그인 매니저 초기화
    db.init_app(app)
    login_manager.init_app(app)

    # 블루프린트 등록
    from auth.routes import auth_bp
    from files.routes import files_bp
    from admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(admin_bp)

    return app

# Gunicorn이 인식할 수 있도록 app 인스턴스 생성
app = create_app()

# 로컬 테스트용
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
