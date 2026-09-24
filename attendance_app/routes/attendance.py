from datetime import date, datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from extensions import db
from models import Student, Attendance
from forms import AttendanceEditForm

attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")


@attendance_bp.route("/mark", methods=["GET", "POST"])
@login_required
def mark_attendance():
    class_name = request.args.get("class_name", "").strip()
    date_str = request.args.get("date", "")
    selected_date = date.today()
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date, showing today instead.", "warning")

    students = []
    if class_name:
        students = (
            Student.query.filter_by(class_name=class_name)
            .order_by(Student.roll_no)
            .all()
        )

    if request.method == "POST":
        class_name = request.form.get("class_name", "").strip()
        date_str = request.form.get("date", "")
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        students = (
            Student.query.filter_by(class_name=class_name)
            .order_by(Student.roll_no)
            .all()
        )

        for student in students:
            status = request.form.get(f"status_{student.id}", "Absent")
            record = Attendance.query.filter_by(
                student_id=student.id, date=selected_date
            ).first()
            if record:
                record.status = status
                record.marked_by = current_user.id
            else:
                record = Attendance(
                    student_id=student.id,
                    date=selected_date,
                    status=status,
                    marked_by=current_user.id,
                )
                db.session.add(record)

        db.session.commit()
        flash(f"Attendance saved for {class_name} on {selected_date}.", "success")
        return redirect(
            url_for("attendance.mark_attendance", class_name=class_name, date=selected_date)
        )

    # Build a lookup of existing attendance for the selected date, so the
    # template can pre-select the correct radio button per student.
    existing = {}
    if students:
        records = Attendance.query.filter(
            Attendance.date == selected_date,
            Attendance.student_id.in_([s.id for s in students]),
        ).all()
        existing = {r.student_id: r.status for r in records}

    return render_template(
        "attendance/mark.html",
        students=students,
        class_name=class_name,
        selected_date=selected_date,
        existing=existing,
    )


@attendance_bp.route("/edit/<int:record_id>", methods=["GET", "POST"])
@login_required
def edit_attendance(record_id):
    record = Attendance.query.get_or_404(record_id)
    form = AttendanceEditForm(obj=record)

    if form.validate_on_submit():
        record.status = form.status.data
        record.date = form.date.data
        record.marked_by = current_user.id
        db.session.commit()
        flash("Attendance record updated.", "success")
        return redirect(url_for("report.student_report", student_id=record.student_id))

    if request.method == "GET":
        form.status.data = record.status
        form.date.data = record.date

    return render_template("attendance/edit.html", form=form, record=record)
