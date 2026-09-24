from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    role = SelectField(
        "Role",
        choices=[("teacher", "Teacher"), ("admin", "Admin")],
        default="teacher",
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")


class StudentForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    roll_no = StringField("Roll Number", validators=[DataRequired(), Length(max=20)])
    class_name = StringField("Class / Section", validators=[DataRequired(), Length(max=50)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=120)])
    submit = SubmitField("Save")


class AttendanceEditForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[("Present", "Present"), ("Absent", "Absent"), ("Late", "Late")],
        validators=[DataRequired()],
    )
    date = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Update")


class AttendanceFilterForm(FlaskForm):
    """Used on the 'mark attendance' page to pick class + date before marking."""

    class_name = StringField("Class / Section", validators=[DataRequired(), Length(max=50)])
    date = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Load Students")
