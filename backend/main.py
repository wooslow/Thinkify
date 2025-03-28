from fastapi import FastAPI

from dotenv import load_dotenv
from auth import auth_router
from ai_engine import ai_router
from database import lifespan

load_dotenv()

app = FastAPI(
    title="Thinkfy API",
    description="Welcome to Thinkfy API documentation!",
    lifespan=lifespan
)
app.include_router(auth_router, prefix="/api")
app.include_router(ai_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": f"Hello, world!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
