from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr 

from src.services.project import (
    create_project, 
    about_project, 
    my_projects, 
    add_member, 
    project_members, 
    delete_member
)
from src.schemas.project import (
    NewProjectSchema, 
    NewProjectMemberSchema, 
    RemoveMemberSchema
)
from src.dependencies import get_current_user
from src.models.user import UserModel
from src.database import get_db

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.post("/new")
async def new_project(
    new_project: NewProjectSchema, 
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await create_project(new_project, user, db)


@router.get("")
async def user_projects(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await my_projects(limit, offset, user, db)
    

@router.post("/members/add")
async def new_member(
    member: NewProjectMemberSchema,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await add_member(member, user, db)


@router.get("/members")
async def get_project_members(
    project_id: int = Query(),
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await project_members(project_id, user, db)


@router.delete("/members")
async def remove_member(
    member: RemoveMemberSchema,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await delete_member(member, user, db)


@router.get("/{project_id}")
async def get_project(
    project_id:int, 
    db: AsyncSession = Depends(get_db)
):
    return await about_project(project_id, db)

