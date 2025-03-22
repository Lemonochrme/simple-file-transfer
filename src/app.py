from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, send_file
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import io
import qrcode

app = Flask(__name__)
app.secret_key = 'your_very_complex_secret_key'

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Single user for demonstration (username: admin / password: admin123)
USERNAME = 'admin'
PASSWORD_HASH = generate_password_hash('admin123')

@app.route('/')
def index():
    if session.get('logged_in'):
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('index.html', files=files)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'):
        return "Unauthorized", 401
    if 'file' not in request.files:
        flash('No file selected', 'warning')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('Empty filename', 'warning')
        return redirect(url_for('index'))
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash('File uploaded successfully', 'success')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    if not session.get('logged_in'):
        return "Unauthorized", 401
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    if not session.get('logged_in'):
        return "Unauthorized", 401
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('File deleted successfully', 'success')
    else:
        flash('File not found', 'warning')
    return redirect(url_for('index'))

@app.route('/qrcode/<filename>')
def qrcode_route(filename):
    if not session.get('logged_in'):
        return "Unauthorized", 401
    # Build the download URL for the file
    download_url = request.url_root.rstrip('/') + url_for('download', filename=filename)
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(download_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # Serve the image from an in-memory stream
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
