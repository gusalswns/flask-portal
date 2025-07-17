from flask import Blueprint, render_template, session, redirect, url_for, flash, send_from_directory
import sqlite3
import os
from config import UPLOAD_FOLDER, DATABASE

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def check_admin():
    if not session.get('is_admin'):
        flash('관리자 권한 필요!', 'error')
        return redirect(url_for('auth.login'))

@admin_bp.route('/')
def admin_page():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT username, name FROM users')
    users = c.fetchall()
    conn.close()
    return render_template('admin.html', users=users)

@admin_bp.route('/files/<username>')
def view_user_files(username):
    folder = os.path.join(UPLOAD_FOLDER, username)
    files = []
    if os.path.exists(folder):
        files = os.listdir(folder)
    return render_template('admin.html', selected_user=username, files=files)

@admin_bp.route('/download/<username>/<filename>')
def admin_download(username, filename):
    folder = os.path.join(UPLOAD_FOLDER, username)
    return send_from_directory(folder, filename, as_attachment=True)

@admin_bp.route('/delete/<username>/<filename>')
def admin_delete_file(username, filename):
    folder = os.path.join(UPLOAD_FOLDER, username)
    fpath = os.path.join(folder, filename)
    if os.path.exists(fpath):
        os.remove(fpath)
        flash('파일 삭제 완료!', 'success')
    return redirect(url_for('admin.view_user_files', username=username))

@admin_bp.route('/delete_user/<username>')
def delete_user(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE username=?', (username,))
    conn.commit()
    conn.close()
    folder = os.path.join(UPLOAD_FOLDER, username)
    if os.path.exists(folder):
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
        os.rmdir(folder)
    flash('계정 삭제 완료!', 'success')
    return redirect(url_for('admin.admin_page'))
