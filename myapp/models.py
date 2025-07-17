import sqlite3, os
from werkzeug.security import generate_password_hash

DB_PATH = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    name TEXT,
                    password TEXT,
                    is_admin INTEGER DEFAULT 0
                )''')
    conn.commit()
    try:
        c.execute('INSERT INTO users (username, name, password, is_admin) VALUES (?,?,?,?)',
                  ('root', '관리자', generate_password_hash('jyj18nom79@gusalswns070124!'), 1))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

init_db()
