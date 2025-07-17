import sqlite3
import os

# DB 파일 경로 설정
db_path = os.path.join(os.path.dirname(__file__), 'users.db')

# DB 연결 및 테이블 생성
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# users 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0
)
''')

# 관리자 계정 기본 생성 (username: admin / password: admin123)
cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
if not cursor.fetchone():
    cursor.execute('''
        INSERT INTO users (username, password, name, is_admin)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin123', '관리자', 1))
    print("기본 관리자 계정을 생성했습니다. (ID: admin, PW: admin123)")
else:
    print("기본 관리자 계정이 이미 존재합니다.")

conn.commit()
conn.close()
print("✅ users.db 초기화 완료.")
