from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete

from src.schemas.project import (
    NewProjectSchema, 
    NewProjectMemberSchema, 
    RemoveMemberSchema,
    GetMemberSchema
)
from src.models.project import ProjectModel, ProjectMemberModel
from src.models.user import UserModel

from .user import get_user_by_email


async def create_project(
    new_project: NewProjectSchema, 
    user: UserModel,
    db: AsyncSession
):
    project = ProjectModel(
        name=new_project.name,
        description=new_project.description
    )
    db.add(project)
    try:
        await db.flush()
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Project name is already in use"
        )

    owner_link = ProjectMemberModel(
        user_id=user.id,
        project_id=project.id,
        role="owner"
    )
    db.add(owner_link)
    await db.commit()
    return project


async def about_project(
    project_id: int, 
    db: AsyncSession
):
    query = await db.execute(
        select(ProjectModel).
        where(ProjectModel.id == project_id)
    )
    project = query.scalar_one_or_none()
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project with this id not found"
        )
    return project


async def my_projects(
    limit: int,
    offset: int,
    user: UserModel,
    db: AsyncSession
):
    query = await db.execute(
        select(ProjectModel)
        .join(ProjectMemberModel, ProjectMemberModel.project_id == ProjectModel.id)
        .where(ProjectMemberModel.user_id == user.id)
        .limit(limit)
        .offset(offset)
    )
    projects = query.scalars().all()
    if not projects:
        raise HTTPException(
            status_code=404,
            detail="Projects not found"
        )
    return projects

async def add_member(
    member: NewProjectMemberSchema,
    user: UserModel,
    db: AsyncSession
):
    query = await db.execute(
        select(ProjectMemberModel)
        .where(
            ProjectMemberModel.user_id == user.id, 
            ProjectMemberModel.project_id == member.project_id
        )
    )
    project_member = query.scalar_one_or_none()
    if not project_member:
        raise HTTPException(
            status_code=403,
            detail="Something went wrong"
        )

    if not project_member.role == "owner":
        raise HTTPException(
            status_code=400,
            detail="Only owner can add new member"
        )

    user = await get_user_by_email(member.email, db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User with this email not found"
        )

    query = await db.execute(
        select(ProjectMemberModel)
        .where(
            ProjectMemberModel.user_id == user.id,
            ProjectMemberModel.project_id == member.project_id
        )
    )
    project_member = query.scalar_one_or_none()
    if project_member:
        raise HTTPException(
            status_code=400,
            detail="User already in project"
        )
    
    new_member = ProjectMemberModel(
        user_id=user.id,
        project_id=member.project_id,
        role="member"
    )
    db.add(new_member)
    await db.commit()
    
    return f"User {member.email} added to project"

async def project_members(
    project_id: int, 
    user: UserModel,
    db: AsyncSession
):
    query = await db.execute(
        select(ProjectMemberModel)
        .where(
            ProjectMemberModel.project_id == project_id,
            ProjectMemberModel.user_id == user.id
        )
    )
    member = query.scalar_one_or_none()
    if not member:
        raise HTTPException(
            status_code=403,
            detail="Only team members can see other members"
        )

    query = await db.execute(
        select(
            UserModel.username, 
            UserModel.email,
            ProjectMemberModel.role
        )
        .join(
            ProjectMemberModel, 
            ProjectMemberModel.user_id == UserModel.id
        )
        .where(
            ProjectMemberModel.project_id == project_id
        )
    )
    members = query.all()

    members_out = [
        GetMemberSchema(
            username=username,
            email=email,
            role=role
        ) for username, email, role in members
    ]
    
    return members_out

async def delete_member(
    member: RemoveMemberSchema,  
    user: UserModel,
    db: AsyncSession
):
    query = await db.execute(
        select(ProjectMemberModel)
        .where(
            ProjectMemberModel.user_id == user.id,
            ProjectMemberModel.project_id == member.project_id
        )
    )
    project_member = query.scalar_one_or_none()

    if not project_member:
        raise HTTPException(
            status_code=403,
            detail="You are not a participant in the project"
        )
    
    if project_member.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owner can remove participants"
        )

    member_for = await get_user_by_email(member.email, db)
    if user.id == member_for.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot remove yourself"
        )
    
    query = await db.execute(
        select(ProjectMemberModel)
        .where(
            ProjectMemberModel.user_id == member_for.id,
            ProjectMemberModel.project_id == member.project_id
        )
    )
    project_member = query.scalar_one_or_none()
    if not project_member:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    query = await db.execute(
        delete(ProjectMemberModel)
        .where(
            ProjectMemberModel.user_id == member_for.id,
            ProjectMemberModel.project_id == member.project_id
        )
    )
    await db.commit()
    return f"User {member.email} removed from project"