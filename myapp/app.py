from flask import Flask
import os
from config import UPLOAD_FOLDER
from auth.routes import auth_bp
from files.routes import files_bp
from admin.routes import admin_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

# 블루프린트 등록
app.register_blueprint(auth_bp)
app.register_blueprint(files_bp)
app.register_blueprint(admin_bp)

# 업로드 폴더 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == "__main__":
    app.run(debug=True)
