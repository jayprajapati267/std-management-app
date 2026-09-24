"""
Central place for Flask extension instances.

Keeping these here (instead of inside app.py) avoids circular imports:
models.py, forms.py and the route blueprints can all import `db` / `login_manager`
without needing to import the app factory itself.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"
