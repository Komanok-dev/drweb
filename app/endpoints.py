from fastapi import APIRouter, HTTPException
from datetime import datetime
from sqlalchemy import select, insert

from app.models import Task
from app.schemas import TaskResponse
from app.session import DatabaseSession
from app.tasks import task_queue


router = APIRouter(prefix='/tasks', tags=['Tasks'])


@router.get('/status', response_model=TaskResponse)
async def get_task_status(id: int, session: DatabaseSession):
    task = (
        await session.execute(
            select(Task)
            .where(Task.id==id)
        )
    ).scalar_one_or_none()
    if not task :
        raise HTTPException(status_code=404, detail='Task not found')
    return TaskResponse(
            status=task.status,
            create_time=task.create_time,
            start_time=task.start_time,
            time_to_execute=task.exec_time
        )


@router.post('/create', response_model=int)
async def create_task(session: DatabaseSession):
    task_id = (
        await session.execute(
            insert(Task)
            .values(status='In Queue', create_time=datetime.now())
            .returning(Task.id)
        )
    ).scalar()
    await task_queue.put(task_id)
    return task_id
