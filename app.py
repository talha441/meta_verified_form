from flask import Flask, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

SAVE_FOLDER = "submissions"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    nid = request.files.get("nid")

    # Save uploaded NID file
    if nid:
        nid_filename = os.path.join(SAVE_FOLDER, nid.filename)
        nid.save(nid_filename)

    # Save form data to a .txt file
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(SAVE_FOLDER, f"{name}_{now}.txt")
    with open(filename, "w") as f:
        f.write(f"Name: {name}\nEmail: {email}\nPhone: {phone}\nNID File: {nid.filename if nid else 'None'}\n")

    return f"Thanks {name}, your form has been submitted!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
