import os

SECRET_KEY = "supersecretkey"
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
DATABASE = os.path.join(os.getcwd(), 'users.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'pdf', 'txt', 'zip'}
