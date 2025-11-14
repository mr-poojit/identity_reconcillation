# 🚀 Identity Reconciliation Backend  
### 🔗 FastAPI • SQLModel • SQLite • Render Deployment • Production-Ready  

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Render](https://img.shields.io/badge/Render-Deploy%20Ready-46E3B7?style=for-the-badge&logo=render)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🧠 Project Overview

This project implements **identity reconciliation** for BiteSpeed — merging multiple contacts (emails/phone numbers) belonging to the same real user.  
It follows BiteSpeed’s rules:

✔ Same email → same user  
✔ Same phone → same user  
✔ Oldest record → primary  
✔ Others → secondary  
✔ New incoming data not found in group → create **secondary contact**  

🛠 Built with **FastAPI**, **SQLModel**, and **SQLite**.  
☁️ Fully deployable on **Render** (Free Tier).

GitHub Repo: **https://github.com/mr-poojit/identity-reconcillation**

---

## ✨ Features

- 🧩 Intelligent identity linking (email + phone graph)
- 🔗 Automatic grouping of related contacts
- 👑 Primary contact determination (oldest)
- 🆕 Auto-create missing secondary contacts
- 📦 SQLite lightweight DB
- ☁️ One-click deploy on Render
- ⚡ High-performance API with FastAPI
- 📘 Swagger docs built-in

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| 🐍 **Python 3.10+** | Backend |
| ⚡ **FastAPI** | API Framework |
| 🗄️ **SQLModel** | ORM/Database |
| 🪶 **SQLite** | Storage |
| 🔧 **Uvicorn** | ASGI Server |
| ☁️ **Render** | Deployment |

---

## 📁 Project Structure

```
identity-reconcillation/
│
├── app/
│   ├── main.py             # API logic
│   ├── crud.py             # DB operations
│   ├── models.py           # SQLModel models
│   ├── schemas.py          # Pydantic schemas
│   └── database.py         # DB initialization
│
├── requirements.txt
├── render.yaml             # Render deployment config
└── README.md
```

---

## 🚀 Running Locally

### 1️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Start Server
```bash
uvicorn app.main:app --reload
```

Visit Swagger:  
👉 http://127.0.0.1:8000/docs

---

## 🧪 Example API Request

### POST `/identify`

#### Request:
```json
{
  "email": "doc@hillvalley.com",
  "phoneNumber": "1234567890"
}
```

#### Response:
```json
{
  "contact": {
    "primaryContatctId": 1,
    "emails": ["doc@hillvalley.com"],
    "phoneNumbers": ["1234567890"],
    "secondaryContactIds": []
  }
}
```

---

## ☁️ Deploy to Render (Free Tier)

### 1️⃣ Push project to GitHub  
Repo: https://github.com/mr-poojit/identity-reconcillation

### 2️⃣ Create `render.yaml` (already included)

```yaml
services:
  - type: web
    name: bitespeed-identity
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

### 3️⃣ Deploy on Render
Go to: https://render.com  
➡️ New → Web Service  
➡️ Select Repo  
➡️ Deploy  

Render automatically:  
✔ installs requirements  
✔ creates sqlite DB  
✔ runs Uvicorn server  

---

## 📝 Important Notes

- Do NOT commit `contacts.db`
```
contacts.db
```

- Render will auto-create a fresh DB when deployed.

---

## 💡 Troubleshooting

### 🔥 1. SQLite “locked” error
Happens only on concurrent writes.  
Fix: Use a production DB (PostgreSQL).

### 🔥 2. CORS blocking frontend
Add to `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧑‍💻 Author
**Poojit Jagadeesh Nagaloti**  
Backend Developer • AI Integrations • Python/FastAPI  
GitHub: https://github.com/mr-poojit  

---

## ⭐ Support  
If you like this project, give it a **🌟 Star on GitHub**!

👉 https://github.com/mr-poojit/identity_reconcillation.git

