from datetime import date

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(UserMixin, db.Model):
    """Teacher / admin account used to log into the app."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="teacher", nullable=False)  # teacher / admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Student(db.Model):
    """A student who can be marked present/absent."""

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    attendances = db.relationship(
        "Attendance", backref="student", lazy=True, cascade="all, delete-orphan"
    )

    def attendance_percentage(self):
        """Percentage of days marked 'Present' out of all recorded days."""
        total = len(self.attendances)
        if total == 0:
            return 0
        present = sum(1 for a in self.attendances if a.status == "Present")
        return round((present / total) * 100, 2)

    def __repr__(self):
        return f"<Student {self.roll_no} - {self.name}>"


class Attendance(db.Model):
    """One attendance record for one student on one date."""

    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.String(10), nullable=False, default="Present")  # Present / Absent / Late
    marked_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    __table_args__ = (
        db.UniqueConstraint("student_id", "date", name="uq_student_date"),
    )

    def __repr__(self):
        return f"<Attendance {self.student_id} {self.date} {self.status}>"
