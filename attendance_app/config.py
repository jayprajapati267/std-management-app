import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration for the Attendance App."""

    # Secret key used for session signing / CSRF protection.
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key-in-production")

    # SQLite database stored inside the instance/ folder.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "instance", "attendance.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-WTF CSRF
    WTF_CSRF_ENABLED = True

    # Pagination default
    STUDENTS_PER_PAGE = 10
