import os

from flask import Flask, redirect, url_for

from config import Config
from extensions import db, login_manager
from models import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Make sure instance/ folder exists for the SQLite file.
    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.attendance import attendance_bp
    from routes.report import report_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(report_bp)

    @app.route("/")
    def index():
        return redirect(url_for("student.list_students"))

    with app.app_context():
        db.create_all()
        _create_default_admin()

    return app


def _create_default_admin():
    """Create a default admin/admin123 account on first run, for convenience."""
    if User.query.filter_by(username="admin").first() is None:
        admin = User(username="admin", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
