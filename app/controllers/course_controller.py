from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..newmodels import Course, db

bp = Blueprint("courses", __name__)

@bp.route("/")
def home():
    courses = Course.query.all()
    return render_template("home.html", courses=courses)

@bp.route("/admin", methods=["GET", "POST"])
def admin():
    error = None
    if request.method == "POST":
        if not request.form["title"]:
            error = "Invalid title"
        elif not request.form["course_code"]:
            error = "Invalid course code"
        else:
            new = Course(request.form["title"], request.form["course_code"])
            db.session.add(new)
            db.session.commit()
            flash("Course successfully created")
            return redirect(url_for("courses.admin"))
    return render_template("admin.html", error=error)
