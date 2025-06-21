
# 🎬 Videoflix Backend API

A modular, scalable backend API built with Django and Django REST Framework for the Videoflix streaming platform. It handles user authentication, secure registration with email confirmation, password reset, video management, genre categorization, and streaming with adaptive quality and playback tracking.

---

## 🚀 Features

- ✅ Token-based authentication and login
- ✅ Secure registration with email confirmation (inactive by default)
- ✅ Password reset via email
- ✅ Full CRUD for videos with genre grouping
- ✅ Playback resume via timestamp tracking per user/video
- ✅ Video upload and auto-processing into 120p, 360p, 720p, 1080p and HLS format
- ✅ Auto thumbnail generation
- ✅ Background processing using Django RQ
- ✅ Redis caching layer
- ✅ PostgreSQL database (recommended)
- ✅ Clean, modular structure following PEP-8 and single-responsibility principles

---

## 🏗️ Tech Stack

- Python 3.12+
- Django 5.x
- Django REST Framework
- PostgreSQL
- Redis + Django RQ (background tasks)
- ffmpeg (video processing)

---

## 📦 Installation

## 🐧 macOS & Linux
```bash

git clone <your-repo-url>
cd videoflix_backend-main
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## 🪟 Windows (cmd)
cmd

git clone <your-repo-url>
cd videoflix_backend-main
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

---

## ⚙️ Configuration

Create a `.env` file in the root directory based on `.env.template`. Example:

```env
FRONTEND_URL=http://localhost:3000
DEFAULT_FROM_EMAIL=noreply@videoflix.com
```

Then run:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## ▶️ Run the Server

```bash
python manage.py runserver
```

Default: http://localhost:8000

---

## 🛠️ API Endpoints

### 🔐 Auth
| Method | Endpoint         | Description                    |
|--------|------------------|--------------------------------|
| POST   | /register/       | Register new user              |
| GET    | /activate/<uid>/<token>/ | Activate user via email  |
| POST   | /login/          | User login                     |
| POST   | /password-reset/ | Request password reset email   |

### 🎞️ Videos
| Method | Endpoint         | Description                       |
|--------|------------------|-----------------------------------|
| GET    | /videos/         | List all videos                   |
| POST   | /videos/         | Upload new video                  |
| PUT    | /videos/<id>/    | Update video metadata             |
| DELETE | /videos/<id>/    | Delete a video                    |

### 📺 Progress
| Method | Endpoint               | Description                             |
|--------|------------------------|-----------------------------------------|
| GET    | /progress/             | List watched progress for current user  |
| POST   | /progress/             | Submit or update progress               |

### 🎭 Genres
| Method | Endpoint       | Description             |
|--------|----------------|-------------------------|
| GET    | /genres/       | List all genres         |
| POST   | /genres/       | Create new genre        |

---

## 🧼 Code Style & Architecture

- ✅ PEP-8 compliant
- ✅ snake_case naming
- ✅ Functions ≤ 14 lines
- ✅ Single responsibility per method
- ✅ No commented or unused code
- ✅ Utility logic separated in `tasks.py` or `signals.py`

---

## 📽️ Background Jobs & Processing

- Video uploads are processed in background via **Django RQ**.
- Redis is used as the task queue.
- Output includes multi-resolution MP4s, thumbnails, and HLS playlist for streaming.

---