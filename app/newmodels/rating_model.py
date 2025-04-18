from sqlalchemy import Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db
from .course_model import Course  # for type hinting in __init__

class Rating(db.Model):
    __table_args__ = (
        CheckConstraint('difficulty <= 5 AND difficulty >= 0', name='difficulty_bounds_check'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    workload: Mapped[int]
    difficulty: Mapped[int]

    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    course: Mapped["Course"] = relationship("Course", back_populates="ratings")

    def __init__(self, workload, difficulty, course: Course):
        self.workload = workload
        self.difficulty = difficulty
        self.course = course
