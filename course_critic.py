from datetime import datetime
from flask import Flask, flash, redirect, render_template, g, request, session, url_for
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy import Enum, Integer, String, Column, ForeignKey, func
import os

from model import Course, Rating, Professor, db


app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(app.root_path, "course_critic.db")
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

SECRET_KEY = "development key"
app.secret_key = SECRET_KEY

db.init_app(app)


@app.cli.command("initdb")
def initdb_command():
    """Reinitializes the database"""
    prof_Snape = Professor("Snape")
    course_Potions = Course("Introduction to Potions", "POT 0600")
    db.drop_all()
    db.create_all()
    db.session.add(Professor("Jonathan Misurda"))
    db.session.add(Professor("Nicholas Farnan"))
    db.session.add(Professor("Nadine von Frankenberg und Ludwigsdor"))
    db.session.add(Professor("William Garrison"))
    db.session.add(Professor("Jarrett Billingsley"))
    db.session.add(prof_Snape)
    db.session.add(Professor("Dumbledore"))
    db.session.add(Course("Intermediate Programming", "CS 0401"))
    db.session.add(Course("Defense Against the Dark Arts 2", "DADA 0220"))
    db.session.add(course_Potions)
    db.session.add(Course("Software Engineering", "CS 1530"))
    db.session.add(Rating(5, 5, course_Potions, prof_Snape))
    db.session.commit()
    print("Initialized the database.")


def get_course_id(coursename):
    """Convenience method to look up the id for a username."""
    rv = db.session.execute(db.select(Course).where(Course.title == coursename)).scalar()
    return rv.id if rv else None

def displayResult(num, ress):
    for res in ress:
        print(f"\nQ{num}:\n{str(res)}\n{repr(res)}\n{type(res)}\n\n")


@app.cli.command("check")
def check():
    stmt = db.select(Course)
    displayResult(
        1,
        db.session.execute(stmt).scalars().all()
    )
    print("done")


@app.route("/")
def home():
    """The home page of CourseCritic. Users can view the available classes and their ratings as well as create their own ratings.
    """
    courses = Course.query.all()
    return render_template("home.html", courses=courses)

@app.route("/search", methods=["GET"])
def search():
    """Returns searched courses"""
    error = None
    search = request.args.get('search', '')
    app.logger.debug(f"Search term: {search}")
    if search:
        searched_courses = Course.query.filter(Course.course_code.contains(search) | Course.title.contains(search)).all()
        app.logger.debug(f"Search results: {searched_courses}")
    else:
        searched_courses = []
    return render_template("home.html", courses=searched_courses, error=error)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    """Admin page where new courses can be added."""
    error = None
    if request.method == "POST":
        if not request.form["title"]:
            error = "Invalid title"
        elif not request.form["course_code"]:
            error = "Invalid course code"
        elif get_course_id(request.form["title"]):
            error = "Course titel taken already"
        else:
            new = Course(
                    request.form["title"],
                    request.form["course_code"],
                )
            db.session.add(new)

            db.session.commit()
            flash("Course successfully created")
            return redirect(url_for("admin"))
    return render_template("admin.html", error=error)
    
@app.route("/course/<int:course_id>")
def course(course_id):
    """Page where the course info is displayed."""
    # get course
    course = db.session.execute(db.select(Course).where(Course.id == course_id)).scalar()

    # get ratings
    stmt = db.select(Rating).where(Rating.course_id == course.id)
    ratings = db.session.execute(stmt).scalars().all()
    
    # calculate average rating

    return render_template("course.html", course=course, ratings=ratings)

