from datetime import datetime

from flask import Blueprint, render_template, request
from flask_login import login_required

from models import Student, Attendance

report_bp = Blueprint("report", __name__, url_prefix="/reports")


@report_bp.route("/student/<int:student_id>")
@login_required
def student_report(student_id):
    student = Student.query.get_or_404(student_id)
    records = (
        Attendance.query.filter_by(student_id=student.id)
        .order_by(Attendance.date.desc())
        .all()
    )
    return render_template(
        "reports/student_report.html", student=student, records=records
    )


@report_bp.route("/class", methods=["GET"])
@login_required
def class_report():
    class_name = request.args.get("class_name", "").strip()
    date_str = request.args.get("date", "")

    students = []
    summary = []
    selected_date = None

    if class_name:
        students = (
            Student.query.filter_by(class_name=class_name)
            .order_by(Student.roll_no)
            .all()
        )

        if date_str:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            records = {
                r.student_id: r.status
                for r in Attendance.query.filter_by(date=selected_date)
                .filter(Attendance.student_id.in_([s.id for s in students]))
                .all()
            }
            for s in students:
                summary.append(
                    {
                        "student": s,
                        "status": records.get(s.id, "Not Marked"),
                        "percentage": s.attendance_percentage(),
                    }
                )
        else:
            for s in students:
                summary.append(
                    {
                        "student": s,
                        "status": None,
                        "percentage": s.attendance_percentage(),
                    }
                )

    return render_template(
        "reports/class_report.html",
        class_name=class_name,
        selected_date=selected_date,
        summary=summary,
    )
