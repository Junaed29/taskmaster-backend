# TaskMaster Pro API Backend

A complete production-ready Django REST API backend for the TaskMaster Pro iOS app.

## Features Included
- **Python/Django Backend**: Django 5.0+ and Django REST Framework
- **JWT Authentication**: Secure stateless token pair base
- **Custom User Model**: Authenticate natively using `email` as the `username` field.
- **RESTful Tasks API**: CRUD operations, filtering, ordering, pagination, toggle completions.
- **Ready for Deployment**: Configured with gunicorn, `Procfile`, Railway/Render configurations, and environment variables handling.

## Initial Setup Instructions

### 1. Prerequisites
- Python 3.10+
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
You can seed demo data utilizing the custom management command we built.
```bash
# Seed the backend with the `demo@taskmaster.com` user and 5 sample tasks
python manage.py create_demo_data
```

To create a Django superuser (admin pane is at `/admin/`):
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

## Testing Endpoints with `curl`

### 1. Login (Obtain Tokens)
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@taskmaster.com", "password":"password123"}'
```
*Note: Copy the `access` token returned inside the JSON payload.*

### 2. Get All Tasks
Replace `<YOUR_ACCESS_TOKEN>` below with the token you copied above.
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

### 3. Create a New Task
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
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
Replace `<TASK_ID>` with the actual UUID string returned from GET endpoints.
```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/<TASK_ID>/toggle/ \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json"
```

## API Documentation
The API views adhere to DRF API design. Because `DEBUG=True` by default locally, opening `http://127.0.0.1:8000/api/tasks/` in a browser will allow you to see the DRF Browsable API.

## Deployment Details
- **Render Deployment**: Add your GitHub repository to Render and use `render.yaml`. Render automatically uses `postgres` or defaults to `sqlite` based on how you override environment URLs.
- **Railway Deployment**: Connect GitHub repo. `railway.json` dictates using Nixpacks. Ensure you add variables in Railway dashboard matching `.env.example`.
