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
    db.drop_all()
    db.create_all()
    db.session.add(Professor("Jonathan Misurda"))
    db.session.add(Professor("Nicholas Farnan"))
    db.session.add(Professor("Nadine von Frankenberg und Ludwigsdor"))
    db.session.add(Professor("William Garrison"))
    db.session.add(Professor("Jarrett Billingsley"))
    db.session.add(Professor("Snape"))
    db.session.add(Professor("Dumbledore"))
    db.session.add(Course("Intermediate Programming", "CS 0401"))
    db.session.add(Course("Defense Against the Dark Arts 2", "DADA 0220"))
    db.session.add(Course("Introduction to Potions", "POT 0600"))
    db.session.add(Course("Software Engineering", "CS 1530"))
    db.session.commit()
    print("Initialized the database.")


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


@app.route("/admin", methods=["GET", "POST"])
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
            return redirect(url_for("admin"))
    return render_template("admin.html", error=error)
    
@app.route("/course/<int:course_id>")
def course(course_id):
    """Page where the course info is displayed."""
    course = db.session.execute(db.select(Course).where(Course.id == course_id)).scalar()

    return render_template("course.html", course=course)

