import os

# 현재 파일 위치를 기준으로 절대 경로 계산
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "supersecretkey"
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
DATABASE = os.path.join(BASE_DIR, 'users.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'pdf', 'txt', 'zip'}
