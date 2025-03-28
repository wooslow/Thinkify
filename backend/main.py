from fastapi import FastAPI, Request, Depends

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from auth import auth_router, AuthService, UserBaseSchema
from ai_engine import ai_router, AIService, CourseTaskSchema, CourseTestSchema
from database import lifespan, DatabaseSession

load_dotenv()

app = FastAPI(
    title="Thinkfy API",
    description="Welcome to Thinkfy API documentation!",
    lifespan=lifespan
)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")
templates = Jinja2Templates(directory="../frontend")

app.include_router(auth_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def create_auth_header(request: Request, call_next):
    if "Authorization" not in request.headers:
        token = request.cookies.get("Authorization")
        if token:
            request.headers.__dict__["_list"].append(
                ("authorization".encode(), f"Bearer {token}".encode())
            )

    response = await call_next(request)
    return response


@app.get("/")
def read_root():
    return {"message": f"Hello, world!"}


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html"
    )


@app.get("/main", response_class=HTMLResponse)
async def main(
    request: Request,
    user: UserBaseSchema = Depends(AuthService.get_currect_user_by_cookie),
):
    return templates.TemplateResponse(
        request=request, name="main.html", context={"username": user.email}
    )


@app.get("/create", response_class=HTMLResponse)
async def create(
    request: Request,
    user: UserBaseSchema = Depends(AuthService.get_currect_user_by_cookie),
):
    return templates.TemplateResponse(
        request=request, name="newtopic.html", context={"username": user.email}
    )


@app.get("/learn/{course_id}/{task_id}", response_class=HTMLResponse)
async def learn(
    request: Request,
    course_id: int,
    task_id: int,
    database: DatabaseSession,
    user: UserBaseSchema = Depends(AuthService.get_currect_user_by_cookie)
):
    ai_service = AIService(database)
    task_dict = await ai_service.get_task(course_id, task_id)
    task = CourseTaskSchema(**task_dict)
    course = await ai_service.get_course(course_id)

    return templates.TemplateResponse(
        request=request,
        name="article.html",
        context={
            "name": task.name,
            "description": task.description,
            "username": user.email,
            'theme': course['name'],
            'test_id': task.id
        }
    )


@app.get("/test/{task_id}", response_class=HTMLResponse)
async def test(
    request: Request,
    task_id: int,
    database: DatabaseSession,
    user: UserBaseSchema = Depends(AuthService.get_currect_user_by_cookie)
):
    ai_service = AIService(database)
    test_dict = await ai_service.get_all_test_for_task(task_id)
    course_test = CourseTestSchema(**test_dict)

    return templates.TemplateResponse(
        request=request, name="test.html", context={
            "test": test_dict,
            "username": user.email
        }
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
