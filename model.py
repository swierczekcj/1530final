from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Column, ForeignKey, CheckConstraint

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


prof_course_table = db.Table(
    "prof_course_table",
    Column("professor_id", Integer, ForeignKey("prof_table.id")),
    Column("course_id", Integer, ForeignKey("course_table.id"))
)

class Course(db.Model):
    __tablename__ = "course_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
    course_code: Mapped[str] = mapped_column(String(30), unique=True)
    
    professors: Mapped[list["Professor"]] = relationship(secondary=prof_course_table, back_populates="courses")
    ratings: Mapped[list["Rating"]] = relationship("Rating", back_populates="course")

    def __init__(self, title, course_code):
        self.title = title
        self.course_code = course_code
        


class Professor(db.Model):
    __tablename__ = "prof_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)

    courses: Mapped[list["Course"]] = relationship(secondary="prof_course_table", back_populates="professors")
    ratings: Mapped[list["Rating"]] = relationship("Rating", back_populates="professor")
    
    def __init__(self, name):
        self.name = name


class Rating(db.Model):
    __tablename__ = "ratings_table"
    __table_args__ = (
        CheckConstraint('difficulty <= 5 AND difficulty >= 0', name='difficulty_bounds_check'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    workload: Mapped[int]
    difficulty: Mapped[int]
    description: Mapped[str] = mapped_column(String(300))
    
    professor_id: Mapped[int] = mapped_column(ForeignKey("prof_table.id"))
    professor: Mapped["Professor"] = relationship("Professor", back_populates="ratings")

    course_id: Mapped[int] = mapped_column(ForeignKey("course_table.id"))
    course: Mapped["Course"] = relationship("Course", back_populates="ratings")

    def __init__(self, workload, difficulty, course:Course, professor, description):
        self.workload = workload
        self.difficulty = difficulty
        self.course = course
        self.professor = professor
        self.description = description