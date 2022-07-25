from sqlalchemy.orm import Session

from app.database import models
from app.schemas.processing import ProcessingTask


class TaskExistsError(Exception):
    pass


class TaskDoesNotExistError(Exception):
    pass


def get_task_by_uuid(db: Session, uuid: str) -> models.Task:
    return db.query(models.Task).filter_by(uuid=uuid).first()


def create_new_task(db: Session, task: ProcessingTask) -> models.Task:
    if get_task_by_uuid(db, task.uuid):
        raise TaskExistsError

    task_entry = models.Task(**task.dict())
    db.add(task_entry)
    db.commit()
    return task_entry


def update_task(db: Session, task: ProcessingTask) -> models.Task:
    existing_task = get_task_by_uuid(db, task.uuid)

    if existing_task is None:
        raise TaskDoesNotExistError

    for k, v in task.dict().items():
        if v is not None and hasattr(existing_task, k):
            setattr(existing_task, k, v)

    db.commit()

    return existing_task