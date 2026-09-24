from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from extensions import db
from models import Student
from forms import StudentForm

student_bp = Blueprint("student", __name__, url_prefix="/students")


@student_bp.route("/")
@login_required
def list_students():
    page = request.args.get("page", 1, type=int)
    class_filter = request.args.get("class_name", "").strip()

    query = Student.query
    if class_filter:
        query = query.filter(Student.class_name.ilike(f"%{class_filter}%"))

    pagination = query.order_by(Student.class_name, Student.roll_no).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template(
        "students/list.html",
        students=pagination.items,
        pagination=pagination,
        class_filter=class_filter,
    )


@student_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        existing = Student.query.filter_by(roll_no=form.roll_no.data.strip()).first()
        if existing:
            flash("A student with this roll number already exists.", "danger")
        else:
            student = Student(
                name=form.name.data.strip(),
                roll_no=form.roll_no.data.strip(),
                class_name=form.class_name.data.strip(),
                email=form.email.data.strip() if form.email.data else None,
            )
            db.session.add(student)
            db.session.commit()
            flash("Student added successfully.", "success")
            return redirect(url_for("student.list_students"))

    return render_template("students/add.html", form=form)


@student_bp.route("/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)

    if form.validate_on_submit():
        student.name = form.name.data.strip()
        student.roll_no = form.roll_no.data.strip()
        student.class_name = form.class_name.data.strip()
        student.email = form.email.data.strip() if form.email.data else None
        db.session.commit()
        flash("Student updated successfully.", "success")
        return redirect(url_for("student.list_students"))

    if request.method == "GET":
        form.name.data = student.name
        form.roll_no.data = student.roll_no
        form.class_name.data = student.class_name
        form.email.data = student.email

    return render_template("students/edit.html", form=form, student=student)


@student_bp.route("/delete/<int:student_id>", methods=["POST"])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted.", "info")
    return redirect(url_for("student.list_students"))
