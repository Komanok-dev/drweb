import asyncio

from fastapi import FastAPI

from app.database import create_tables
from app.endpoints import router
from app.session import async_sessionmaker
from app.tasks import process_tasks, request_unprocessed_tasks


async def lifespan(app: FastAPI):
    await create_tables()
    async with async_sessionmaker() as session:
        await request_unprocessed_tasks(session)
    app.state.task_processor = asyncio.create_task(process_tasks())
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)
