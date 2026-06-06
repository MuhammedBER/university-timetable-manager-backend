<h1 align="center">🎓 University Timetable Manager — Backend</h1>
<p align="center">
  REST API for a university timetable management system — professors, rooms, courses & fields.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white"/>
</p>

---

## 📌 Overview

The backend REST API for the University Timetable Manager platform. Built with **FastAPI** and **MySQL**, it powers the full timetable generation and management system for universities — handling professors, rooms, courses, fields and authentication.

---

## ✨ Features

- 📅 **Timetable Generation** — Create and manage university timetables
- 👨‍🏫 **Professor Management** — Add and manage professor records
- 🏫 **Room Management** — Manage classrooms and their availability
- 📚 **Course & Field Management** — Handle courses and academic fields
- 🔐 **Authentication** — Secure JWT-based authentication system
- 📡 **REST API** — Clean and documented API endpoints

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Language | Python |
| Database | MySQL |
| Auth | JWT |

---

## 🚀 Getting Started

### Prerequisites
- Python >= 3.9
- MySQL

### Setup

```bash
# Clone the repo
git clone https://github.com/MuhammedBER/university-timetable-manager-backend.git
cd university-timetable-manager-backend

# Install dependencies
pip install -r requirements.txt

# Configure your database in .env
cp .env.example .env

# Run the server
uvicorn main:app --reload
```

### API Docs
Once running, visit:
```
http://localhost:8000/docs
```

---

## 🔗 Related

- 🌐 Frontend: [university-timetable-manager-frontend](https://github.com/MuhammedBER/university-timetable-manager-frontend)

---

## 👨‍💻 Author

**Mohamed Berhaila**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/mohamed-berhaila)
[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=flat&logo=vercel&logoColor=white)](https://berhaila.com)
