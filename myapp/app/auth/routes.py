from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('files.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT name, password, is_admin FROM users WHERE username=?',(username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[1], password):
            session['username'] = username
            session['name'] = user[0]
            session['is_admin'] = bool(user[2])
            return redirect(url_for('files.dashboard'))
        else:
            flash('로그인 실패!', 'error')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = generate_password_hash(request.form['password'])
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, name, password) VALUES (?,?,?)',(username, name, password))
            conn.commit()
            conn.close()
            flash('회원가입 성공! 로그인하세요.','success')
            return redirect(url_for('auth.login'))
        except:
            flash('이미 존재하는 아이디입니다.','error')
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
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        if 'new_name' in request.form:
            new_name = request.form['new_name']
            c.execute('UPDATE users SET name=? WHERE username=?',(new_name,session['username']))
            session['name'] = new_name
            flash('이름 변경 완료!','success')
        if 'new_password' in request.form:
            new_pass = generate_password_hash(request.form['new_password'])
            c.execute('UPDATE users SET password=? WHERE username=?',(new_pass,session['username']))
            flash('비밀번호 변경 완료!','success')
        conn.commit()
        conn.close()
    return render_template('settings.html', name=session.get('name'))
