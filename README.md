# 📁 Cloud Storage Mini Project

A simple personal cloud storage web application built using **Python Flask (Backend)** and **HTML + JavaScript (Frontend)**.  
This project allows users to register, login, upload files, download files, and delete files – all stored locally on the system.

---

## 🚀 Features

- User Registration  
- User Login  
- Individual storage folder for each user  
- File Upload (with drag & drop support)  
- File List Display  
- File Download  
- File Delete  
- Simple and clean dark mode UI  
- Local storage system  
- REST API based communication  

---

## 🛠 Technologies Used

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** JSON file (`users.json`)  
- **Storage:** Local File System  
- **API Communication:** Fetch API  

---

## 📂 Project Structure

project-folder/
│
├── app.py # Flask backend server
├── users.json # Stores registered users
├── uploads/ # Stores uploaded files
│
├── login.html # Login page
├── register.html # Registration page
└── upload.html # Main cloud dashboard


---

## ⚙ How to Run the Project

### 1. Install Python Dependencies

Make sure you have Python installed.

Install required packages:

pip install flask flask-cors


---

### 2. Run Backend Server

Open terminal in project folder and run:

python app.py


Backend will start at:

http://127.0.0.1:5000


---

### 3. Open Frontend

Open this file in browser:

login.html


From there you can:

- Register a new account  
- Login  
- Upload and manage files  

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|------|----------|-------------|
| POST | /register | Register new user |
| POST | /login | User login |
| POST | /upload/<username> | Upload file |
| GET  | /files/<username> | List user files |
| GET  | /download/<username>/<filename> | Download file |
| DELETE | /delete/<username>/<filename> | Delete file |

---

## 💡 How It Works

- Each user gets a personal folder inside `uploads/username/`
- Files are stored locally
- Frontend communicates with Flask API using Fetch
- User session is stored using browser `localStorage`

---

## 📌 Future Improvements

Possible features to add in future:

- File rename option  
- Multiple file upload  
- Upload progress bar  
- Image preview  
- Search filter  
- File size and date display  
- Better authentication system  

---

## 🧑‍💻 Author

Developed as a learning project in Computer Science Engineering.

---

## 📄 License

This project is free to use for educational purposes.
