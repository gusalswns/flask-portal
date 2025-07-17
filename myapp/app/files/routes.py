from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

files_bp = Blueprint('files', __name__, url_prefix='/dashboard')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@files_bp.route('/', methods=['GET','POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    user_folder = os.path.join(UPLOAD_FOLDER, session['username'])
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(user_folder, filename))
            flash('업로드 성공!','success')
        else:
            flash('허용되지 않는 파일입니다.','error')

    files = os.listdir(user_folder)
    return render_template('dashboard.html', name=session.get('name'), files=files)

@files_bp.route('/download/<filename>')
def download_file(filename):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    user_folder = os.path.join(UPLOAD_FOLDER, session['username'])
    return send_from_directory(user_folder, filename, as_attachment=True)

@files_bp.route('/delete/<filename>')
def delete_file(filename):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    user_folder = os.path.join(UPLOAD_FOLDER, session['username'])
    file_path = os.path.join(user_folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('삭제 완료!','success')
    return redirect(url_for('files.dashboard'))
