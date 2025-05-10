from fastapi import APIRouter

from .auth import router as auth_router
from .project import router as project_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(project_router)