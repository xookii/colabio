from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.task import new_task, get_tasks, task_done
from src.schemas.task import NewTaskSchema
from src.models.user import UserModel
from src.dependencies import get_current_user
from src.database import get_db


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("/new")
async def add_task(
    task: NewTaskSchema,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await new_task(task, user, db)

@router.post("/complete")
async def complete_task(
    task_id: int,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await task_done(task_id, user, db)

@router.get("")
async def project_tasks(
    project_id: int = Query(),
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await get_tasks(project_id, user, db)

