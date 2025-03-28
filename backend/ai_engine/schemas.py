from pydantic import BaseModel


class NewCourseSchema(BaseModel):
    topic: str
    destination: str
    knows_now: str


class CourseSmallSchema(BaseModel):
    id: int
    author: str
    name: str
    description: str
    passed_lessons: int


class CourseTaskSchema(BaseModel):
    id: int
    course_id: int
    name: str
    description: str
    tests: list[dict] = None
    input: str | None = None


class CourseTestSchema(BaseModel):
    id: int
    task_id: int
    question: str
    answers: str
    question_type: str
    correct_answer: str
