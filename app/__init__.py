from flask import Flask
from .newmodels import db
from .controllers import course_controller  # Add other controllers as needed

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///course_critic.db"
    app.config["SECRET_KEY"] = "development key"

    db.init_app(app)

    # Register CLI commands
    from .cli import init_cli_commands
    init_cli_commands(app)

    # Register Blueprints
    app.register_blueprint(course_controller.bp)  # Add other controllers similarly

    return app