from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
USER_DB = "users.json"

# Ensure required folders and files exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)


@app.route("/")
def home():
    return "Cloud Storage Mini Project Backend Running!"


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    with open(USER_DB, "r") as f:
        users = json.load(f)

    if username in users:
        return jsonify({"message": "User already exists"}), 400

    users[username] = password

    with open(USER_DB, "w") as f:
        json.dump(users, f)

    os.makedirs(os.path.join(UPLOAD_FOLDER, username), exist_ok=True)

    return jsonify({"message": "User registered successfully"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    with open(USER_DB, "r") as f:
        users = json.load(f)

    if users.get(username) == password:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@app.route("/upload/<username>", methods=["POST"])
def upload(username):

    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]

    user_folder = os.path.join(UPLOAD_FOLDER, username)
    os.makedirs(user_folder, exist_ok=True)

    file.save(os.path.join(user_folder, file.filename))

    return jsonify({"message": "File uploaded successfully"})


# 🔥 FIXED LIST FILES ENDPOINT
@app.route("/files/<username>")
def list_files(username):

    user_folder = os.path.join(UPLOAD_FOLDER, username)

    if not os.path.exists(user_folder):
        return jsonify([])

    files = os.listdir(user_folder)

    file_list = []

    for f in files:
        file_list.append({
            "name": f
        })

    return jsonify(file_list)


@app.route("/download/<username>/<filename>")
def download(username, filename):

    user_folder = os.path.join(UPLOAD_FOLDER, username)
    return send_from_directory(user_folder, filename)


# 🔥 FIXED DELETE ENDPOINT
@app.route("/delete/<username>/<filename>", methods=["DELETE"])
def delete_file(username, filename):

    user_folder = os.path.join(UPLOAD_FOLDER, username)
    file_path = os.path.join(user_folder, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": "File deleted successfully"})
    else:
        return jsonify({"message": "File not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
