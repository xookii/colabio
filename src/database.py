from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///colabio.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with new_session() as session:
        yield session

class Model(DeclarativeBase):
    pass

from src.models.user import UserModel
from src.models.project import ProjectModel, ProjectMemberModel

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)