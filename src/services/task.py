from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.services.user import get_user_by_email
from src.models.user import UserModel
from src.models.project import ProjectMemberModel
from src.models.task import TaskModel
from src.schemas.task import NewTaskSchema

async def new_task(
    task: NewTaskSchema,
    user: UserModel,
    db: AsyncSession
):
    query = await db.execute(
        select(ProjectMemberModel)
        .where(
            ProjectMemberModel.user_id == user.id,
            ProjectMemberModel.project_id == task.project_id
        )
    )
    if not query.scalar_one_or_none():
        raise HTTPException(
            status_code=403,
            detail="Only team members can add task"
        )

    assignee = await get_user_by_email(task.assignee_email, db)

    query = await db.execute(
        select(ProjectMemberModel)
        .where(
            ProjectMemberModel.user_id == assignee.id,
            ProjectMemberModel.project_id == task.project_id
        )
    )
    if not query.scalar_one_or_none():
        raise HTTPException(
            status_code=404,
            detail="Assignee not found"
        )

    task = TaskModel(
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        assignee_id=assignee.id
    )
    db.add(task)
    await db.commit()
    return "Task successfully added"


async def get_tasks(
    project_id: int,
    user: UserModel,
    db: AsyncSession
):
    query = await db.execute(
        select(ProjectMemberModel)
        .where(
            ProjectMemberModel.user_id == user.id,
            ProjectMemberModel.project_id == project_id
        )
    )
    if not query.scalar_one_or_none():
        raise HTTPException(
            status_code=403,
            detail="Only team members can see tasks"
        )

    query = await db.execute(
        select(TaskModel)
        .where(TaskModel.project_id == project_id)
    )
    tasks = query.scalars().all()
    if not tasks:
        return "There is not tasks yet"
    return tasks

async def task_done(
    task_id: int,
    user: UserModel,
    db: AsyncSession
):
    query = await db.execute(
        select(TaskModel)
        .where(TaskModel.id == task_id)
    )
    task = query.scalar_one_or_none()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    query = await db.execute(
        select(ProjectMemberModel)
        .where(
            ProjectMemberModel.user_id == user.id,
            ProjectMemberModel.project_id == task.project_id
        )
    )
    member = query.scalar_one_or_none()
    if not member or not task.assignee_id == user.id:
        raise HTTPException(
            status_code=403,
            detail="Only assignee can complete tasks"
        )

    task.status = "completed"
    db.add(task)
    await db.commit()
    return "Task completed"