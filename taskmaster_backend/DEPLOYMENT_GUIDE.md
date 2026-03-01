# TaskMaster Pro — Deployment & Update Guide

A complete reference for managing your TaskMaster Pro API on PythonAnywhere.

---

## Table of Contents

- [Making Changes Locally](#making-changes-locally)
- [Pushing Changes to GitHub](#pushing-changes-to-github)
- [Updating PythonAnywhere](#updating-pythonanywhere)
- [Adding New Models or Fields](#adding-new-models-or-fields)
- [Installing New Packages](#installing-new-packages)
- [Managing the Database](#managing-the-database)
- [Keeping the App Alive](#keeping-the-app-alive)
- [Troubleshooting](#troubleshooting)
- [Quick Reference](#quick-reference)

---

## Making Changes Locally

### 1. Activate Your Virtual Environment

```bash
cd /Users/junaed/Desktop/Django/taskmaster/taskmaster_backend
source venv/bin/activate
```

### 2. Make Your Code Changes

Edit any file — models, views, serializers, URLs, etc.

### 3. Run Tests Before Pushing

Always verify your changes work:

```bash
python manage.py test api
```

### 4. Run the Dev Server to Test Manually

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/api/tasks/` to test locally.

---

## Pushing Changes to GitHub

After making and testing changes locally:

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Your commit message here"

# Push to GitHub
git push origin main
```

---

## Updating PythonAnywhere

After pushing to GitHub, you need to pull the changes on PythonAnywhere and reload.

### Step 1 — Open a Bash Console

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and log in
   - **Username**: `junaedcrack`
2. Click **Consoles** tab
3. Open your existing Bash console, or start a new one

### Step 2 — Pull Latest Code

```bash
cd ~/taskmaster-backend/taskmaster_backend
workon taskmaster-env
git pull origin main
```

### Step 3 — Apply Migrations (if you changed models)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4 — Collect Static Files (if you changed static assets)

```bash
python manage.py collectstatic --noinput
```

### Step 5 — Reload the Web App

1. Go to the **Web** tab
2. Click the green **Reload** button

> **Important**: The app won't reflect your changes until you click Reload!

---

## Adding New Models or Fields

When you add a new model or modify an existing one:

### Locally

```bash
# 1. Make the model changes in api/models.py
# 2. Generate the migration
python manage.py makemigrations

# 3. Apply the migration
python manage.py migrate

# 4. Test
python manage.py test api

# 5. Push to GitHub
git add .
git commit -m "Add new model/field"
git push origin main
```

### On PythonAnywhere

```bash
cd ~/taskmaster-backend/taskmaster_backend
workon taskmaster-env
git pull origin main
python manage.py makemigrations
python manage.py migrate
```

Then **Reload** from the Web tab.

---

## Installing New Packages

When you need a new Python package:

### Locally

```bash
# 1. Install the package
pip install package-name

# 2. Update requirements.txt
pip freeze > requirements.txt

# 3. Push to GitHub
git add requirements.txt
git commit -m "Add package-name dependency"
git push origin main
```

### On PythonAnywhere

```bash
cd ~/taskmaster-backend/taskmaster_backend
workon taskmaster-env
git pull origin main
pip install -r requirements.txt
```

Then **Reload** from the Web tab.

---

## Managing the Database

### View Data via Admin Panel

- **URL**: https://junaedcrack.pythonanywhere.com/admin/
- **Email**: `admin@taskmaster.com`
- **Password**: `Admin@2529`

### Reset Demo Data

If you want fresh demo data on PythonAnywhere:

```bash
cd ~/taskmaster-backend/taskmaster_backend
workon taskmaster-env

# Delete existing database
rm db.sqlite3

# Recreate everything
python manage.py migrate
python manage.py create_demo_data
```

Then **Reload** from the Web tab.

### Create a New Admin User

```bash
cd ~/taskmaster-backend/taskmaster_backend
workon taskmaster-env
python manage.py createsuperuser
```

### Database Backup

Since SQLite is a single file, back it up by copying:

```bash
cp ~/taskmaster-backend/taskmaster_backend/db.sqlite3 ~/db_backup_$(date +%Y%m%d).sqlite3
```

---

## Keeping the App Alive

PythonAnywhere free tier disables your web app after **1 month of inactivity**.

### What "Inactivity" Means
- You haven't logged into PythonAnywhere for 30 days
- The app stops serving requests

### What Happens When It's Disabled
- Your app URL returns an error page
- **Your data is NOT deleted** — everything is safe
- Your files, database, virtualenv — all intact

### How to Keep It Running
1. Log in to [pythonanywhere.com](https://www.pythonanywhere.com) at least once a month
2. Go to the **Web** tab
3. Click **Reload** (or click the "Run until 3 months from today" link if it appears)

### If Your App Gets Disabled
1. Log in to PythonAnywhere
2. Go to the **Web** tab
3. Click the button to re-enable it
4. Click **Reload**
5. Done — your app is back with all its data

---

## Troubleshooting

### "Server Error (500)" on the live site

1. Check the **error log** on PythonAnywhere:
   - Web tab → click the **Error log** link
   - Look at the last few lines for the error
2. Common causes:
   - Missing migration → run `python manage.py migrate`
   - Missing package → run `pip install -r requirements.txt`
   - Typo in code → fix and redeploy

### "Module not found" error

```bash
cd ~/taskmaster-backend/taskmaster_backend
workon taskmaster-env
pip install -r requirements.txt
```

Then **Reload**.

### Changes not showing up

Make sure you:
1. Pushed to GitHub (`git push origin main`)
2. Pulled on PythonAnywhere (`git pull origin main`)
3. Clicked **Reload** on the Web tab

### WSGI file got messed up

The WSGI config file is at:
```
/var/www/junaedcrack_pythonanywhere_com_wsgi.py
```

It should contain exactly:
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

---

## Quick Reference

### Key URLs

| What | URL |
|---|---|
| **Live API** | `https://junaedcrack.pythonanywhere.com/api/` |
| **Admin Panel** | `https://junaedcrack.pythonanywhere.com/admin/` |
| **GitHub Repo** | `https://github.com/Junaed29/taskmaster-backend` |
| **PythonAnywhere Dashboard** | `https://www.pythonanywhere.com/user/junaedcrack/` |

### Accounts

| Account | Email | Password |
|---|---|---|
| **Admin** | `admin@taskmaster.com` | `Admin@2529` |
| **Demo User** | `demo@taskmaster.com` | `password123` |

### PythonAnywhere Paths

| What | Path |
|---|---|
| **Project Root** | `/home/junaedcrack/taskmaster-backend/taskmaster_backend` |
| **Virtualenv** | `/home/junaedcrack/.virtualenvs/taskmaster-env` |
| **SQLite Database** | `/home/junaedcrack/taskmaster-backend/taskmaster_backend/db.sqlite3` |
| **Static Files** | `/home/junaedcrack/taskmaster-backend/taskmaster_backend/static/` |
| **WSGI File** | `/var/www/junaedcrack_pythonanywhere_com_wsgi.py` |
| **Error Log** | Web tab → Error log link |

### The Update Workflow (Cheat Sheet)

```bash
# === LOCAL ===
cd /Users/junaed/Desktop/Django/taskmaster/taskmaster_backend
source venv/bin/activate
# ... make changes ...
python manage.py test api
git add .
git commit -m "description"
git push origin main

# === PYTHONANYWHERE (Bash Console) ===
cd ~/taskmaster-backend/taskmaster_backend
workon taskmaster-env
git pull origin main
python manage.py migrate          # if models changed
pip install -r requirements.txt   # if packages changed
python manage.py collectstatic --noinput  # if static files changed
# Then: Web tab → Reload
```
