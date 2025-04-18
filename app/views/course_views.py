from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Course

course_bp = Blueprint('course', __name__)

@course_bp.route("/")
def home():
    """The home page of CourseCritic. Users can view the available classes and their ratings as well as create their own ratings."""
    courses = Course.query.all()
    return render_template("home.html", courses=courses)

@course_bp.route("/admin", methods=["GET", "POST"])
def admin():
    """Admin page where new courses can be added."""
    error = None
    if request.method == "POST":
        if not request.form["title"]:
            error = "Invalid title"
        elif not request.form["course_code"]:
            error = "Invalid course code"
        else:
            new = Course(
                    request.form["title"],
                    request.form["course_code"],
                )
            db.session.add(new)
            db.session.commit()
            flash("Course successfully created")
            return redirect(url_for("course.admin"))
    return render_template("admin.html", error=error)
