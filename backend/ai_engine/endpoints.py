import logging

from fastapi import APIRouter, Depends

from .schemas import NewCourseSchema, CourseSmallSchema, CourseTaskSchema, CourseTestSchema
from .service import AIService
from auth import AuthService, UserBaseSchema
from database import DatabaseSession

log = logging.getLogger(__name__)

ai_router = APIRouter(tags=["ai"])


@ai_router.post("/course", response_model=CourseSmallSchema)
async def new_course(
    course: NewCourseSchema,
    database: DatabaseSession,
    user: UserBaseSchema = Depends(AuthService.get_current_user),
):
    ai_service = AIService(database)
    answer = await ai_service.create_course_gpt(user, course)

    return answer


@ai_router.get("/courses", response_model=list[CourseSmallSchema])
async def get_courses(
    database: DatabaseSession,
    user: UserBaseSchema = Depends(AuthService.get_current_user),
):
    ai_service = AIService(database)
    answer = await ai_service.get_courses(user)

    return answer


@ai_router.get("/course/{course_id}/task/{task_number}", response_model=CourseTaskSchema)
async def get_course(
    course_id: int,
    task_number: int,
    database: DatabaseSession,
    user: UserBaseSchema = Depends(AuthService.get_current_user),
):
    ai_service = AIService(database)
    answer = await ai_service.get_task(course_id, task_number)

    return answer


@ai_router.get("/course/tests/{task_id}", response_model=CourseTestSchema)
async def get_course(
    task_id: int,
    database: DatabaseSession,
    user: UserBaseSchema = Depends(AuthService.get_current_user),
):
    ai_service = AIService(database)
    answer = await ai_service.get_all_test_for_task(task_id)

    return answer
