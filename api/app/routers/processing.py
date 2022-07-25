import uuid
import json

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from pika_utils import Producer

from app.database import models
from app.database.db_admin import get_db
from app.database.crud import create_new_task, get_task_by_uuid, update_task
from app.schemas.processing import ProcessingRequest, ProcessingTask, ProcessingTaskUpdate


QUEUE_NAME = "processing_q_1"


router = APIRouter()


@router.post("/processing")
def send_data_processing_request(processing_request: ProcessingRequest, db: Session = Depends(get_db)):
    """
    User-facing endpoint.

    1. Take a user processing request
    2. Assign a uuid
    3. Send the processing request to the queue
    4. Return the uuid to the user
    """

    uuid_code = str(uuid.uuid4())

    task_config = ProcessingTask(
        uuid=uuid_code,
        process=processing_request.process,
        complete=False,
    )

    create_new_task(db, task_config)

    producer = Producer()
    producer.send(QUEUE_NAME, json.dumps(task_config.dict()))
    
    return {"task_uuid": uuid_code}


@router.get("/processing/{uuid}", response_model=ProcessingTask)
def get_processed_data(uuid: str, db: Session = Depends(get_db)):
    """
    User-facing endpoint.

    1. Take the uuid of a processing task
    2. Check if the processed task results exist in the database
    3. If they exist, return them to the user
    4. If they don't exist, return a message telling the user
       to try again later
    """

    task = get_task_by_uuid(db, uuid)

    return _format_processing_task_response(task)


@router.put("/processing/update", include_in_schema=False, response_model=ProcessingTask)
def update_task_status(task: ProcessingTaskUpdate, db: Session = Depends(get_db)):
    """
    Internal use endpoint.

    Update the status of the data processing task in the database.
    """
    
    task = update_task(db, task)

    return _format_processing_task_response(task)


def _format_processing_task_response(task: models.Task) -> ProcessingTask:
    data = task.data
    
    return ProcessingTask(
        uuid=task.uuid, 
        process=task.process,
        complete=task.complete,
        data=data
    )