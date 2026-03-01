# TaskMaster Pro API Backend

A complete production-ready Django REST API backend for the TaskMaster Pro iOS app.

## 🌐 Live Deployment

The API is hosted on **PythonAnywhere** (free tier):

| | |
|---|---|
| **Live API Base URL** | `https://junaedcrack.pythonanywhere.com` |
| **Admin Panel** | `https://junaedcrack.pythonanywhere.com/admin/` |
| **DRF Browsable API** | `https://junaedcrack.pythonanywhere.com/api/tasks/` |

### Accounts

| Account | Email | Password | Purpose |
|---|---|---|---|
| **Admin** | `admin@taskmaster.com` | `Admin@2529` | Django admin panel access |
| **Demo User** | `demo@taskmaster.com` | `password123` | API testing (has 5 sample tasks) |

## Features Included
- **Python/Django Backend**: Django 6.0+ and Django REST Framework
- **JWT Authentication**: Secure stateless token pair (access + refresh)
- **Custom User Model**: Authenticate using `email` as the username field
- **RESTful Tasks API**: CRUD operations, filtering, ordering, pagination, toggle completions
- **WhiteNoise Static Files**: Self-serve static files in production
- **Deployed on PythonAnywhere**: Free hosting with persistent SQLite database

---

## Local Development Setup

### 1. Prerequisites
- Python 3.12+
- `pip` package manager

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill the variables:
```bash
cp .env.example .env
```
Ensure you generate a strong secure `SECRET_KEY`.

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Admin User and Demo Data
Seed demo data:
```bash
# Creates `demo@taskmaster.com` user with 5 sample tasks
python manage.py create_demo_data
```

Create a Django superuser:
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/auth/login/` | Get JWT tokens (access + refresh) | ❌ |
| `POST` | `/api/auth/refresh/` | Refresh access token | ❌ |
| `POST` | `/api/auth/logout/` | Blacklist refresh token | ✅ |
| `GET` | `/api/tasks/` | List all tasks (paginated) | ✅ |
| `POST` | `/api/tasks/` | Create a new task | ✅ |
| `GET` | `/api/tasks/{id}/` | Get a single task | ✅ |
| `PUT` | `/api/tasks/{id}/` | Full update a task | ✅ |
| `PATCH` | `/api/tasks/{id}/` | Partial update a task | ✅ |
| `DELETE` | `/api/tasks/{id}/` | Delete a task | ✅ |
| `PATCH` | `/api/tasks/{id}/toggle/` | Toggle task completion | ✅ |

### Filters & Ordering
- **Filter by priority**: `?priority=high`
- **Filter by completion**: `?is_completed=true`
- **Search**: `?search=design`
- **Order**: `?ordering=-created_at`

---

## Testing with `curl` (Live API)

### 1. Login (Obtain Tokens)
```bash
curl -X POST https://junaedcrack.pythonanywhere.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@taskmaster.com", "password":"password123"}'
```
*Copy the `access` token from the response.*

### 2. Get All Tasks
```bash
curl -X GET https://junaedcrack.pythonanywhere.com/api/tasks/ \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

### 3. Create a New Task
```bash
curl -X POST https://junaedcrack.pythonanywhere.com/api/tasks/ \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Django REST Framework",
    "description": "Read documentation and build an API",
    "priority": "high",
    "due_date": "2026-03-01T10:00:00Z"
  }'
```

### 4. Toggle Task Completion Status
```bash
curl -X PATCH https://junaedcrack.pythonanywhere.com/api/tasks/<TASK_ID>/toggle/ \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

### 5. Delete a Task
```bash
curl -X DELETE https://junaedcrack.pythonanywhere.com/api/tasks/<TASK_ID>/ \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

---

## Testing with Postman

A ready-to-use Postman collection is included: `TaskMaster_Pro_API.postman_collection.json`

1. **Import** the collection into Postman
2. The `base_url` variable is pre-set to `https://junaedcrack.pythonanywhere.com`
3. **Run Login** first — the post-request script auto-saves tokens to environment variables
4. All other requests automatically use the saved token

> **Tip**: To test locally instead, change the `base_url` variable to `http://127.0.0.1:8000`

---

## PythonAnywhere Deployment Guide

### Initial Deployment

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com) (free Beginner account)
2. **Open Bash Console** → Clone the repo:
   ```bash
   git clone https://github.com/Junaed29/taskmaster-backend.git
   cd taskmaster-backend/taskmaster_backend
   ```
3. **Create virtual environment**:
   ```bash
   mkvirtualenv taskmaster-env --python=/usr/bin/python3.12
   pip install -r requirements.txt
   ```
4. **Set up database & static files**:
   ```bash
   python manage.py migrate
   python manage.py create_demo_data
   python manage.py collectstatic --noinput
   ```
5. **Create Web App** (Web tab → Add new web app):
   - Choose **Manual configuration** (NOT "Django")
   - Select **Python 3.12**
6. **Set paths** on the Web tab:
   - Source code: `/home/junaedcrack/taskmaster-backend/taskmaster_backend`
   - Virtualenv: `/home/junaedcrack/.virtualenvs/taskmaster-env`
7. **Edit WSGI file** — delete everything, paste:
   ```python
   import os
   import sys

   path = '/home/junaedcrack/taskmaster-backend/taskmaster_backend'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'taskmaster.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
8. **Set static files** mapping:
   - URL: `/static/` → Directory: `/home/junaedcrack/taskmaster-backend/taskmaster_backend/static/`
9. Click **Reload**

### Updating the Deployment

After pushing changes to GitHub, update the live server:

```bash
# Open a Bash console on PythonAnywhere
cd ~/taskmaster-backend/taskmaster_backend
workon taskmaster-env

# Pull latest changes
git pull origin main

# Apply any new migrations
python manage.py migrate

# Collect static files (if any changed)
python manage.py collectstatic --noinput
```

Then go to the **Web** tab and click **Reload**.

### Keeping It Alive

PythonAnywhere disables free web apps after **1 month of inactivity**. To prevent this:
- Log into PythonAnywhere once a month
- Click **Reload** on the Web tab
- Your SQLite data persists forever — even if the app gets temporarily disabled

---

## Project Structure

```
taskmaster_backend/
├── api/                    # Main app
│   ├── models.py           # CustomUser + Task models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # ViewSets and auth views
│   ├── urls.py             # API URL routing
│   ├── filters.py          # Task filtering
│   ├── tests.py            # API test suite (5 tests)
│   └── management/
│       └── commands/
│           └── create_demo_data.py
├── taskmaster/             # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── Procfile
├── render.yaml
├── railway.json
└── TaskMaster_Pro_API.postman_collection.json
```
