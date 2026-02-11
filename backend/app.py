from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

BASE_FOLDER = "uploads"
USERS_FILE = "users.json"


# ---------- INITIAL SETUP ----------

if not os.path.exists(BASE_FOLDER):
    os.makedirs(BASE_FOLDER)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)


# ---------- USER MANAGEMENT ----------

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)


# ---------- ROUTES ----------

@app.route("/")
def home():
    return "Cloud Storage Backend Running!"


@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    users = load_users()

    if username in users:
        return jsonify({"message": "User already exists"}), 400

    users[username] = password
    save_users(users)

    user_folder = os.path.join(BASE_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)

    return jsonify({"message": "User registered successfully"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    users = load_users()

    if username in users and users[username] == password:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# ---------- FILE UPLOAD ----------

@app.route("/upload/<username>", methods=["POST"])
def upload_file(username):

    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)

    if filename == "":
        return jsonify({"message": "Invalid filename"}), 400

    user_folder = os.path.join(BASE_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)

    file.save(os.path.join(user_folder, filename))

    return jsonify({"message": "File uploaded successfully"})


# ---------- LIST FILES AND FOLDERS ----------

@app.route("/files/<username>")
def list_files(username):

    user_folder = os.path.join(BASE_FOLDER, username)

    if not os.path.exists(user_folder):
        return jsonify([])

    items = []

    for item in os.listdir(user_folder):

        path = os.path.join(user_folder, item)

        if os.path.isdir(path):
            items.append({
                "type": "folder",
                "name": item
            })
        else:
            items.append({
                "type": "file",
                "name": item
            })

    return jsonify(items)


# ---------- DOWNLOAD FILE ----------

@app.route("/download/<username>/<filename>")
def download_file(username, filename):

    filename = secure_filename(filename)

    user_folder = os.path.join(BASE_FOLDER, username)

    file_path = os.path.join(user_folder, filename)

    if not os.path.exists(file_path):
        return jsonify({"message": "File not found"}), 404

    return send_from_directory(user_folder, filename)


# ---------- DELETE FILE ----------

@app.route("/delete/<username>/<filename>", methods=["DELETE"])
def delete_file(username, filename):

    filename = secure_filename(filename)

    user_folder = os.path.join(BASE_FOLDER, username)
    path = os.path.join(user_folder, filename)

    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        return jsonify({"message": "File deleted"})
    else:
        return jsonify({"message": "File not found"}), 404


# ---------- CREATE FOLDER ----------

@app.route("/create_folder/<username>", methods=["POST"])
def create_folder(username):

    data = request.json
    foldername = data.get("folder")

    if not foldername:
        return jsonify({"message": "Folder name required"}), 400

    foldername = secure_filename(foldername)

    user_folder = os.path.join(BASE_FOLDER, username)
    new_folder = os.path.join(user_folder, foldername)

    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        return jsonify({"message": "Folder created"})

    return jsonify({"message": "Folder already exists"}), 400


# ---------- DELETE FOLDER ----------

@app.route("/delete_folder/<username>/<foldername>", methods=["DELETE"])
def delete_folder(username, foldername):

    foldername = secure_filename(foldername)

    folder_path = os.path.join(BASE_FOLDER, username, foldername)

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        return jsonify({"message": "Folder deleted"})
    else:
        return jsonify({"message": "Folder not found"}), 404


# ---------- RUN SERVER ----------

if __name__ == "__main__":
    app.run(debug=True)
