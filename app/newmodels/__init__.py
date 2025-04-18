from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Step 1: Define Base class
class Base(DeclarativeBase):
    pass

# Step 2: Create db object using that base
db = SQLAlchemy(model_class=Base)

# Step 3: Import models to register with SQLAlchemy
from .course_model import Course
from .rating_model import Rating