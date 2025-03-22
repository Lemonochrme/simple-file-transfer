from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ultra_complexe'  # Changez cette clé pour plus de sécurité

# Répertoire pour stocker les fichiers uploadés
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

USERNAME = 'admin' # Bien penser à changer le login / mdp
PASSWORD_HASH = generate_password_hash('admin123')

@app.route('/')
def index():
    # Vérifier si l'utilisateur est authentifié
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
        # Vérification de l'identifiant et du mot de passe
        if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Identifiants invalides', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'):
        return "Non autorisé", 401
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné', 'warning')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('Nom de fichier vide', 'warning')
        return redirect(url_for('index'))
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash('Fichier uploadé avec succès', 'success')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    if not session.get('logged_in'):
        return "Non autorisé", 401
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    # L'application sera accessible sur le réseau local
    app.run(host='0.0.0.0', port=4242, debug=True)
