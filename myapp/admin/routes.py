from flask import Blueprint, render_template, session, flash, redirect, url_for, send_from_directory
import os, sqlite3
from app import app

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def get_db_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username, name FROM users')
    users = c.fetchall()
    conn.close()
    return users

@admin_bp.route('/')
def admin_dashboard():
    # 관리자만 접근
    if 'username' not in session or session.get('is_admin') != True:
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect(url_for('auth.login'))

    users = get_db_users()
    # selected_user, files 기본값을 넘겨서 템플릿이 오류 나지 않게 함
    return render_template('admin.html', users=users, selected_user=None, files=[])

@admin_bp.route('/view/<username>')
def view_user_files(username):
    if 'username' not in session or session.get('is_admin') != True:
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect(url_for('auth.login'))

    users = get_db_users()
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    files = []
    if os.path.exists(user_folder):
        files = os.listdir(user_folder)

    return render_template('admin.html', users=users, selected_user=username, files=files)

@admin_bp.route('/download/<username>/<filename>')
def admin_download(username, filename):
    if 'username' not in session or session.get('is_admin') != True:
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect(url_for('auth.login'))

    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], username), filename, as_attachment=True)

@admin_bp.route('/delete/<username>/<filename>')
def admin_delete_file(username, filename):
    if 'username' not in session or session.get('is_admin') != True:
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect(url_for('auth.login'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], username, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'{filename} 파일 삭제 완료.', 'success')
    else:
        flash('파일을 찾을 수 없습니다.', 'error')

    return redirect(url_for('admin.view_user_files', username=username))

@admin_bp.route('/delete_user/<username>')
def delete_user(username):
    if 'username' not in session or session.get('is_admin') != True:
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect(url_for('auth.login'))

    # root 계정은 삭제 불가
    if username == 'root':
        flash('root 계정은 삭제할 수 없습니다.', 'error')
        return redirect(url_for('admin.admin_dashboard'))

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE username=?', (username,))
    conn.commit()
    conn.close()

    # 업로드 폴더 삭제
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    if os.path.exists(user_folder):
        for f in os.listdir(user_folder):
            os.remove(os.path.join(user_folder, f))
        os.rmdir(user_folder)

    flash(f'{username} 계정을 삭제했습니다.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
