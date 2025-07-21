from flask import Flask, request, render_template
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    fb_url = request.form['fb_url']
    email = request.form['email']
    phone = request.form['phone']
    file = request.files['gov_id']

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    with open('submissions.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, fb_url, email, phone, filename])

    return f"""
    <h2>Thank you, {name}!</h2>
    <p>Your submission has been saved successfully.</p>
    """

if __name__ == '__main__':
    app.run(debug=True)
