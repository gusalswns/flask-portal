import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        name TEXT,
                        password_hash TEXT NOT NULL,
                        is_admin INTEGER DEFAULT 0
                    )''')
    conn.commit()
    conn.close()