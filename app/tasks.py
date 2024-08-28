import asyncio
import random

from datetime import datetime
from sqlalchemy import select

from app.enum import TaskStatus
from app.models import Task
from app.session import DatabaseSession, async_sessionmaker


task_queue = asyncio.Queue()
semaphore = asyncio.Semaphore(value=2) 


async def process_tasks():
    while True:
        task_id = await task_queue.get()
        asyncio.create_task(run_task_with_semaphore(task_id))

async def run_task_with_semaphore(task_id):
    async with semaphore:
        async with async_sessionmaker() as session:
            await run_task(task_id, session)

async def request_unprocessed_tasks(session: DatabaseSession):
    unprocessed_tasks = (
        await session.execute(
            select(Task).where(Task.status == TaskStatus.IN_QUEUE)
        )
    ).scalars().all()
    for task in unprocessed_tasks:
        await task_queue.put(task.id)


async def run_task(task_id: int, session: DatabaseSession):
    async with session.begin():
        task = await session.get(Task, task_id)
        if task is None:
            return
        task.status = TaskStatus.RUN
        task.start_time = datetime.now()

    await asyncio.sleep(random.randint(0, 10))

    async with session.begin():
        task = await session.get(Task, task_id)
        if task is None:
            return
        task.status = TaskStatus.COMPLETED
        task.exec_time = datetime.now() - task.start_time
