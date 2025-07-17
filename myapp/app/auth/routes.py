import os
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, '..', 'users.db')

@auth_bp.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('files.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # 입력 체크 (필수는 아니지만 권장)
        if not username or not password:
            flash('아이디와 비밀번호를 모두 입력하세요.', 'error')
            return render_template('login.html')

        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('SELECT name, password, is_admin FROM users WHERE username=?', (username,))
            user = c.fetchone()
            conn.close()
        except Exception as e:
            flash('서버 오류가 발생했습니다. 관리자에게 문의하세요.', 'error')
            # 실제 디버깅 시에는 print(e) 혹은 로깅 권장
            return render_template('login.html')

        if user:
            stored_hash = user[1]
            if check_password_hash(stored_hash, password):
                session['username'] = username
                session['name'] = user[0]
                session['is_admin'] = bool(user[2])
                return redirect(url_for('files.dashboard'))
            else:
                flash('비밀번호가 올바르지 않습니다.', 'error')
        else:
            flash('존재하지 않는 아이디입니다.', 'error')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        name = request.form.get('name', '').strip()
        password_raw = request.form.get('password', '')

        if not username or not name or not password_raw:
            flash('모든 항목을 입력하세요.', 'error')
            return render_template('register.html')

        password = generate_password_hash(password_raw)

        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute('INSERT INTO users (username, name, password) VALUES (?, ?, ?)', (username, name, password))
            conn.commit()
            conn.close()
            flash('회원가입 성공! 로그인하세요.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            # 중복된 아이디 시 IntegrityError 발생
            flash('이미 존재하는 아이디입니다.', 'error')
        except Exception as e:
            # 기타 예외처리 - 디버깅용 출력 혹은 로깅 추천
            flash('서버 오류가 발생했습니다. 관리자에게 문의하세요.', 'error')
            # print(e)

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/settings', methods=['GET','POST'])
def settings():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        try:
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            if 'new_name' in request.form:
                new_name = request.form['new_name'].strip()
                if new_name:
                    c.execute('UPDATE users SET name=? WHERE username=?', (new_name, session['username']))
                    session['name'] = new_name
                    flash('이름 변경 완료!', 'success')
            if 'new_password' in request.form:
                new_password = request.form['new_password'].strip()
                if new_password:
                    new_pass_hash = generate_password_hash(new_password)
                    c.execute('UPDATE users SET password=? WHERE username=?', (new_pass_hash, session['username']))
                    flash('비밀번호 변경 완료!', 'success')
            conn.commit()
            conn.close()
        except Exception as e:
            flash('서버 오류가 발생했습니다. 관리자에게 문의하세요.', 'error')
            # print(e)
    return render_template('settings.html', name=session.get('name'))
