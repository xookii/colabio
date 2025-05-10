from fastapi import FastAPI

import uvicorn

from src.api import main_router
from src.database import create_tables

app = FastAPI()
app.include_router(main_router)

@app.on_event("startup")
async def setup():
    await create_tables()

if __name__ == '__main__':
    uvicorn.run("src.main:app")