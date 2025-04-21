from datetime import datetime
from flask import Flask, flash, redirect, render_template, g, request, session, url_for
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
    prof_Snape = Professor("Snape")
    course_Potions = Course("Introduction to Potions", "POT 0600")
    profs = [Professor("Jonathan Misurda"), Professor("Nadine von Frankenberg"), Professor("Nicholas Farnan"),
             Professor("William Garrison"), Professor("Jarett Billingsley"), prof_Snape, Professor("Dumbledore")]
    for prof in profs:
        db.session.add(prof)
    courses = [course_Potions, Course("Intermediate Programming", "CS 0401"),
               Course("Defense Against the Dark Arts 2", "DADA 0220"),  Course("Introduction to Flying", "BRM 0747"),
               Course("Software Engineering", "CS 1530")]
    for course in courses:
        db.session.add(course)
    db.session.commit()
    i = 0
    for prof in profs:
        prof.courses.append(courses[i % len(courses)])
        i+=1
    db.session.commit()
    print("Initialized the database.")




def get_course_id(coursename):
    rv = db.session.execute(db.select(Course).where(Course.title == coursename)).scalar()
    return rv.id if rv else None

def displayResult(num, ress):
    for res in ress:
        print(f"\nQ{num}:\n{str(res)}\n{repr(res)}\n{type(res)}\n\n")

@app.cli.command("check")
def check():
    stmt = db.select(Course)
    displayResult(1, db.session.execute(stmt).scalars().all())
    print("done")

@app.route("/")
def home():
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
    course = db.session.execute(db.select(Course).where(Course.id == course_id)).scalar()
    stmt = db.select(Rating).where(Rating.course_id == course.id)
    ratings = db.session.execute(stmt).scalars().all()
    
    #get profs
    professors = course.professors
    
    diffAvg = sum([rating.difficulty for rating in ratings]) / len(ratings) if ratings else 0
    workAvg = sum([rating.workload for rating in ratings]) / len(ratings) if ratings else 0
    # calculate average rating

    return render_template("course.html", course=course, ratings=ratings, diff=diffAvg, work=workAvg, profs=professors)

@app.route("/submit", methods=["GET", "POST"])
def submit():
    courses = Course.query.all()
    professors = Professor.query.all()
    error = None

    if request.method == "POST":
        course_id = request.form.get("course_id")
        prof_id = request.form.get("professor_id")
        rating = request.form.get("rating")
        difficulty = request.form.get("difficulty")
        description = request.form.get("description")

        if not course_id or not prof_id or not rating or not difficulty or not description:
            error = "All fields are required."
        else:
            selected_course = Course.query.get(int(course_id))
            selected_prof = Professor.query.get(int(prof_id))

            new_rating = Rating(
                int(rating),
                int(difficulty),
                selected_course,
                selected_prof,
                description
            )
            db.session.add(new_rating)
            db.session.commit()
            flash("Your review has been submitted!")
            return redirect(url_for("home"))

    return render_template("submit.html", courses=courses, professors=professors, error=error)
