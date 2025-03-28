import json
import os
import re

from dotenv import load_dotenv
from openai import Client

from database import DatabaseSession
from auth import UserBaseSchema
from .repository import AIRepository
from .schemas import NewCourseSchema
from enums import PROMT_AI

load_dotenv()


class AIService:
    def __init__(self, database: DatabaseSession) -> None:
        self.ai_repository = AIRepository(database)
        self.client = Client(api_key=os.getenv("OPENAI_API_KEY"))

    async def create_course_gpt(self, user: UserBaseSchema, course: NewCourseSchema) -> dict:
        """Create course with GPT-4o"""

        prompt = (
            PROMT_AI.
                replace("польский язык", course.topic).
                replace("я хочу знать многие фрукты и овощи на польском языке", course.destination).
                replace("A1 немного знаю польский алфавит и некоторые слова", course.knows_now)
        )
        response = self.client.responses.create(
            model="gpt-4o",
            instructions=prompt,
            input=prompt
        )

        response = response.output_text

        try:
            response_text = re.sub(r"```json|```", "", response).strip()
            response_json = json.loads(response_text)
        except Exception as e:
            response_json = {"error": "Not Acsess"}

        answer = await self.ai_repository.create_course(user, response_json)
        return answer.model_dump()

    async def get_courses(self, user: UserBaseSchema) -> list[dict]:
        """ Fetch all courses from database """
        answer = await self.ai_repository.get_courses(user)
        return [course.model_dump() for course in answer]

    async def get_task(self, course_id: int, task_number: int) -> dict:
        """ Fetch task from course """
        answer = await self.ai_repository.get_course(course_id)

        answer = answer.tasks[task_number - 1]

        return answer.model_dump()

    async def get_test_for_task(self, task_id: int) -> dict:
        """ Fetch test for task """
        answer = await self.ai_repository.get_test(task_id)

        return answer.model_dump()
