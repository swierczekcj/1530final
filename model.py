from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Column, ForeignKey, CheckConstraint

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Course(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
    course_code: Mapped[str] = mapped_column(String(30), unique=True)

    ratings: Mapped[list["Rating"]] = relationship("Rating", back_populates="course")

    def __init__(self, title, course_code):
        self.title = title
        self.course_code = course_code


class Rating(db.Model):
    __table_args__ = (
        CheckConstraint('difficulty <= 5 AND difficulty >= 0', name='difficulty_bounds_check'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    workload: Mapped[int]
    difficulty: Mapped[int]

    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    course: Mapped["Course"] = relationship("Course", back_populates="ratings")

    def __init__(self, workload, difficulty, course:Course):
        self.workload = workload
        self.difficulty = difficulty
        self.course = course