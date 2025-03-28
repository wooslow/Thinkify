from fastapi import FastAPI, Request, Depends

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from auth import auth_router, AuthService, UserBaseSchema
from ai_engine import ai_router
from database import lifespan

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
    user: UserBaseSchema = Depends(AuthService.get_current_user_cookie),
):
    token = request.cookies.get("Authorization")
    if not token:
        return RedirectResponse(url="/login")

    return templates.TemplateResponse(
        request=request, name="main.html", context={"username": user.email}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
