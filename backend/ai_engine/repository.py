"""
Repository for AI

All methods that interact with the database should be here
Only database models or nothing should be returned from this class
"""

import json

from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from database import DatabaseSession
from auth import UserBaseSchema
from .models import CourseBaseModel, CourseTaskModel, CourseTestModel


class AIRepository:
    def __init__(self, database: DatabaseSession) -> None:
        self.database: DatabaseSession = database

    async def create_course(
        self,
        user: UserBaseSchema,
        course_ai_answer: dict
    ) -> CourseBaseModel:
        async with self.database as session:
            course = CourseBaseModel(
                name=course_ai_answer["course_name"],
                description=course_ai_answer["course_short_description"],
                author=user.email
            )
            session.add(course)

            await session.flush()

            for task_data in course_ai_answer["course_tasks"]:
                task = CourseTaskModel(
                    course_id=course.id,
                    name=task_data["task_name"],
                    description=task_data["task_description"]
                )
                session.add(task)

                await session.flush()

                for test_data in task_data.get("test_after_task", []):
                    test = CourseTestModel(
                        task_id=task.id,
                        question=test_data["question"],
                        answers=json.dumps(test_data["answers"]),
                        question_type=test_data["type"],
                        correct_answer=str(test_data["correct_answer"])
                    )
                    session.add(test)

            await session.commit()

            return course

    async def get_courses(self, user: UserBaseSchema) -> list[CourseBaseModel]:
        async with self.database as session:
            query = select(CourseBaseModel).where(CourseBaseModel.author == user.email)
            courses = await session.execute(query)
            return courses.scalars().all()

    async def get_course(self, course_id: int) -> CourseBaseModel:
        async with self.database as session:
            query = select(CourseBaseModel).where(CourseBaseModel.id == course_id).options(
                joinedload(CourseBaseModel.tasks)
            )
            course = await session.execute(query)
            return course.scalar()

    async def get_task(self, task_id: int) -> CourseTaskModel:
        async with self.database as session:
            query = select(CourseTaskModel).where(CourseTaskModel.id == task_id)
            task = await session.execute(query)
            return task.scalar()

    async def get_test(self, task_id: int) -> CourseTestModel:
        async with self.database as session:
            query = select(CourseTestModel).where(CourseTestModel.task_id == task_id)
            test = await session.execute(query)
            return test.scalar()

    async def get_tests(self, task_id: int) -> CourseTestModel:
        async with self.database as session:
            query = select(CourseTestModel).where(CourseTestModel.task_id == task_id and CourseTestModel.question_type == "radio")
            test = await session.execute(query)
            return test.scalar()
