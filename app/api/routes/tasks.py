from fastapi import APIRouter, Query, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: DbSession, user: CurrentUser):
    task = Task(**data.model_dump(), owner_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: DbSession,
    user: CurrentUser,
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = select(Task).where(Task.owner_id == user.id)
    if status_filter:
        query = query.where(Task.status == status_filter)
    query = query.order_by(Task.id.desc()).limit(limit).offset(offset)
    return db.scalars(query).all()