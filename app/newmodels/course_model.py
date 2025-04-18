from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db

class Course(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
    course_code: Mapped[str] = mapped_column(String(30), unique=True)

    ratings: Mapped[list["Rating"]] = relationship("Rating", back_populates="course")

    def __init__(self, title, course_code):
        self.title = title
        self.course_code = course_code
