from flask.cli import with_appcontext
import click
from .newmodels import db, Course

def display_result(num, results):
    for res in results:
        print(f"\nQ{num}:\n{str(res)}\n{repr(res)}\n{type(res)}\n\n")

@click.command("initdb")
@with_appcontext
def initdb_command():
    """Reinitializes the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Initialized the database.")

@click.command("check")
@with_appcontext
def check_command():
    """Checks the Course table."""
    from .controllers.course_model import Course
    display_result(1, db.session.execute(db.select(Course)).scalars().all())
    print("done")

def init_cli_commands(app):
    app.cli.add_command(initdb_command)
    app.cli.add_command(check_command)
