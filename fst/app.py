from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import sqlite3, os

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.permanent_session_lifetime = timedelta(minutes=30)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'pdf', 'txt', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# DB 초기화
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        is_admin INTEGER DEFAULT 0
    )''')
    conn.commit()
    # 관리자 계정 기본 생성
    try:
        c.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)',
                  ('admin', generate_password_hash('admin'), 1))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT password, is_admin FROM users WHERE username=?', (username,))
        result = c.fetchone()
        conn.close()
        if result and check_password_hash(result[0], password):
            session.permanent = True
            session['username'] = username
            session['is_admin'] = bool(result[1])
            flash('로그인 성공!', 'success')
            return redirect('/dashboard')
        else:
            flash('로그인 실패. 아이디와 비밀번호를 확인하세요.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
            conn.commit()
            flash('회원가입 성공! 로그인해주세요.', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('이미 존재하는 사용자입니다.', 'error')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            f.save(os.path.join(user_folder, f.filename))
            flash('파일 업로드 완료!', 'success')
        else:
            flash('업로드 불가한 파일 형식!', 'error')
    files = os.listdir(user_folder)
    return render_template('dashboard.html', files=files, username=session['username'], is_admin=session.get('is_admin', False))

@app.route('/uploads/<username>/<filename>')
def uploaded_file(username, filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], username), filename, as_attachment=True)

@app.route('/delete_file/<filename>', methods=['POST'])
def delete_file(filename):
    if 'username' not in session:
        return redirect('/login')
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])
    target = os.path.join(user_folder, filename)
    if os.path.exists(target):
        os.remove(target)
        flash('파일 삭제 완료.', 'success')
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash('로그아웃 되었습니다.', 'info')
    return redirect('/login')

@app.route('/admin')
def admin():
    if 'username' not in session or not session.get('is_admin'):
        flash('관리자 권한 필요!', 'error')
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, is_admin FROM users')
    users = c.fetchall()
    conn.close()
    return render_template('admin.html', users=users)

@app.route('/promote/<username>')
def promote(username):
    if 'username' not in session or not session.get('is_admin'):
        flash('관리자 권한 필요!', 'error')
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE users SET is_admin=1 WHERE username=?',(username,))
    conn.commit()
    conn.close()
    flash(f'{username} 관리자 승격 완료.', 'success')
    return redirect('/admin')

@app.route('/delete_user/<username>', methods=['POST'])
def delete_user(username):
    if 'username' not in session or not session.get('is_admin'):
        flash('관리자 권한 필요!', 'error')
        return redirect('/login')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE username=?',(username,))
    conn.commit()
    conn.close()
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    if os.path.exists(user_folder):
        for f in os.listdir(user_folder):
            os.remove(os.path.join(user_folder,f))
        os.rmdir(user_folder)
    flash(f'{username} 계정 삭제 완료.', 'success')
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
