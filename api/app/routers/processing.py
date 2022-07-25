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
    Send a data processing request to the application.
    
    A universally unique identifier (UUID) is produced for the processing request
    and returned to the user. This can be used later to retrieve the results of the
    data processing.

    The processing request is send to the queue, which is consumed by the data 
    processing service.
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
    Retrieve the processed data results from the application, using the UUID code
    assigned for the specific processing task.

    The resulting processed data is stored under the "data" key in the response JSON.
    """

    task = get_task_by_uuid(db, uuid)

    return _format_processing_task_response(task)


@router.put("/processing/update", include_in_schema=False, response_model=ProcessingTask)
def update_processing_task(task: ProcessingTaskUpdate, db: Session = Depends(get_db)):
    """
    Update a processing task in the database.

    This endpoint is called internally by the data processing service of the
    application, and is used to update the task in the database with the results
    of the data processing.
    """
    
    task = update_task(db, task)

    return _format_processing_task_response(task)


def _format_processing_task_response(task: models.Task) -> ProcessingTask:
    return ProcessingTask(
        uuid=task.uuid, 
        process=task.process,
        complete=task.complete,
        data=task.data
    )