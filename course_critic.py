from datetime import datetime
from flask import Flask, flash, redirect, render_template, g, request, session, url_for
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy import Enum, Integer, String, Column, ForeignKey, func
import os

from model import Course, Rating, db


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


# @app.route("/customer", methods=["GET", "POST"])
# def customer():
#     """Customer home page."""
#     customer = db.session.execute(db.select(Customer).where(Customer.id == g.user.id)).scalar()

#     stmt = db.select(Event).where(Event.customer_id == customer.id)
#     requested_events = db.session.execute(stmt).scalars().all()

#     error = None
#     if request.method == "POST":
#         event_date_str = request.form["event-date"]
#         event_date = int(datetime.strptime(event_date_str, "%Y-%m-%d").timestamp())

#         busy = db.session.execute(db.select(Event).where(Event.date == event_date)).scalar()
#         if busy:
#             error = "An event is already scheduled for that day."
#         else:
#             event = Event(event_date, customer)
#             db.session.add(event)
#             db.session.commit()
#             flash("Event successfully requested")
#             return redirect(url_for("customer"))

        
#     return render_template("customer.html", error=error, requested_events=requested_events)


# @app.route("/cancel_event/<int:event_id>")
# def cancel_event(event_id):
#     """Cancels a customer's request for an event."""
#     cancel = db.session.execute(db.select(Event).where(Event.id == event_id)).scalar()
#     db.session.delete(cancel)

#     db.session.commit()
#     flash("Event successfully canceled.")
#     return redirect(url_for("customer"))


# @app.route("/signup_event/<int:event_id>")
# def signup_event(event_id):
#     """Signs a staff member up for an event."""
#     event = db.session.execute(db.select(Event).where(Event.id == event_id)).scalar()
#     staff = db.session.execute(db.select(Staff).where(Staff.id == g.user.id)).scalar()
#     event.workers.append(staff)

#     db.session.commit()
#     flash("Event successfully added to your schedule.")
#     return redirect(url_for("staff"))


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Logs the user in."""
#     if g.user:
#         return redirect(url_for("home"))
    
#     error = None
#     if request.method == "POST":
#         user = db.session.execute(db.select(User).where(User.username == request.form["username"])).scalar()
#         # Why not check both individually?
#         if user is None or not user.password == request.form["password"]:
#             error = "Invalid username/password combination"
#         else:
#             flash("You were logged in")
#             session["user_id"] = user.id
#             if user.role == 0:
#                 return redirect(url_for("owner"))
#             elif user.role == 1:
#                 return redirect(url_for("staff"))
#             elif user.role == 2:
#                 return redirect(url_for("customer"))
#             return redirect(url_for("home"))
        
#     return render_template("login.html", error=error)


# @app.route("/create_staff_account", methods=["GET", "POST"])
# def create_staff_account():
#     """Creates a staff account."""
#     error = None
#     if request.method == "POST":
#         if not request.form["username"]:
#             error = "You have to enter a username"
#         elif not request.form["password"]:
#             error = "You have to enter a password"
#         elif get_user_id(request.form["username"]) is not None:
#             error = "The username is already taken"
#         else:
#             new = User(
#                     request.form["username"],
#                     request.form["password"],
#                     1,
#                 )
#             db.session.add(new)
#             new = Staff(new)
#             db.session.add(new)

#             db.session.commit()
#             flash("Staff member successfully created")
#             return redirect(url_for("owner"))
#     return render_template("create_staff_account.html", error=error)