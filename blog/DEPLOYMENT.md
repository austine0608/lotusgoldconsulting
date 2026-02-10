# Django Blog Deployment Guide

## Environment Variables

Create a `.env` file in the project root:

```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
```

## Option 1: Deploy to Render.com

### 1. Push to GitHub
```
git init
git add .
git commit -m "Initial commit"
git push to GitHub
```

### 2. Create Web Service on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn myblog.wsgi:application`
   - Environment Variables: Add `DJANGO_SECRET_KEY` and `DJANGO_DEBUG=False`

### 3. Create Database
1. Click "New +" → "PostgreSQL"
2. Note the connection string

### 4. Update Settings
Add `DATABASE_URL` to your web service environment variables:
```
DATABASE_URL=postgres://user:pass@host:5432/dbname
```

### 5. Update settings.py for PostgreSQL
```python
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
```

## Option 2: Deploy to Railway

### 1. Push to GitHub
Same as Render

### 2. Deploy on Railway
1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository

### 4. Add PostgreSQL
1. Click "New +" → "Database" → "PostgreSQL"
2. Note the connection string

### 5. Configure Environment Variables
In Railway dashboard, add:
- `DJANGO_SECRET_KEY`
- `DATABASE_URL`
- `DJANGO_DEBUG=False`

## Option 3: Deploy to PythonAnywhere

### 1. Upload Files
- Upload your project to PythonAnywhere using their file uploader or git clone

### 2. Create Virtual Environment
```bash
mkvirtualenv myblog --python=/usr/bin/python3.13
pip install -r requirements.txt
```

### 3. Configure WSGI File
Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import os
import sys
path = '/home/yourusername/yourproject'
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'myblog.settings'
os.environ['DJANGO_SECRET_KEY'] = 'your-secret-key'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 4. Configure Database
Use PythonAnywhere's MySQL or PostgreSQL addon

### 5. Run Migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

## Static Files

For production, run:
```bash
python manage.py collectstatic
```

## Common Issues & Fixes

### 1. TemplateDoesNotExist
- Check `TEMPLATES` DIRS setting
- Verify template paths are correct

### 2. Static files not loading
- Run `python manage.py collectstatic`
- Configure `STATIC_ROOT` correctly

### 3. Database connection errors
- Verify DATABASE_URL format
- Check firewall settings
- Ensure database is in same region as web service

### 4. CSRF errors
- Keep DEBUG=True in development
- Check ALLOWED_HOSTS configuration

### 5. Media files not serving
- Add to your web server config:
```nginx
location /media/ {
    alias /path/to/media/;
}
```

## Security Checklist

- [ ] Set DEBUG=False in production
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS (auto on most platforms)
- [ ] Keep dependencies updated
- [ ] Regular database backups
- [ ] Set ALLOWED_HOSTS appropriately
