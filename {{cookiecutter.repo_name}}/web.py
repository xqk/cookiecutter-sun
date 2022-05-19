import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from conf import settings
from services.http.controllers import routers

app = FastAPI(
    title=settings.TITLE,
    docs_url="/{{cookiecutter.repo_name}}/docs",
    openapi_url="/{{cookiecutter.repo_name}}/openapi.json",
)

root_router = APIRouter(prefix="/{{cookiecutter.repo_name}}/api")
for i in routers:
    root_router.include_router(i)

app.include_router(root_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("web:app", host="0.0.0.0", port=8000, reload=True, access_log=True)
