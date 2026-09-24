# Attendance App

A simple Flask-based student attendance management system.

## Features
- Login (Flask-Login) — default account `admin` / `admin123`
- Student CRUD (add / edit / delete / list with filter + pagination)
- Mark daily attendance per class (Present / Absent / Late)
- Edit individual attendance records
- Per-student and per-class attendance reports with percentages

## Setup

```bash
cd attendance_app
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

The app runs at http://127.0.0.1:5000/ and creates `instance/attendance.db`
(SQLite) automatically on first run, along with the default admin account.

## Project structure

```
attendance_app/
├── app.py              # Application factory + entry point
├── config.py            # Config class (secret key, DB URI)
├── models.py            # User, Student, Attendance (SQLAlchemy)
├── forms.py              # WTForms: Login, Student, Attendance
├── extensions.py          # db, login_manager instances
├── requirements.txt
├── routes/
│   ├── auth.py           # /auth/login, /auth/logout
│   ├── student.py         # /students CRUD
│   ├── attendance.py       # /attendance/mark, /attendance/edit/<id>
│   └── report.py          # /reports/student/<id>, /reports/class
├── templates/            # Jinja2 templates (Bootstrap 5 styled)
└── static/
    ├── css/style.css
    └── js/main.js
```

## Notes / next steps
- Change `SECRET_KEY` in `config.py` (or via env var) before deploying.
- Swap SQLite for Postgres/MySQL by changing `DATABASE_URL`.
- Add role-based restrictions (e.g. only admins can delete students) if needed.
