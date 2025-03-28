from sqlalchemy import String, BigInteger, Integer, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import CustomBase


class CourseBaseModel(CustomBase):
    __tablename__ = "courses_base"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    author: Mapped[str] = mapped_column(String, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)
    passed_lessons: Mapped[int] = mapped_column(Integer, default=0)

    tasks: Mapped[list["CourseTaskModel"]] = relationship("CourseTaskModel", back_populates="course", cascade="all, delete")


class CourseTaskModel(CustomBase):
    __tablename__ = "courses_tasks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("courses_base.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text)

    course: Mapped["CourseBaseModel"] = relationship("CourseBaseModel", back_populates="tasks")
    tests: Mapped[list["CourseTestModel"]] = relationship("CourseTestModel", back_populates="task", cascade="all, delete")


class CourseTestModel(CustomBase):
    __tablename__ = "courses_tests"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("courses_tasks.id", ondelete="CASCADE"))
    question: Mapped[str] = mapped_column(Text)
    answers: Mapped[str] = mapped_column(Text)
    question_type: Mapped[str] = mapped_column(String)
    correct_answer: Mapped[str] = mapped_column(Text)
    task: Mapped["CourseTaskModel"] = relationship("CourseTaskModel", back_populates="tests")
