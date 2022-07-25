from typing import Optional

from pydantic import BaseModel


class ProcessingRequest(BaseModel):
    process: str


class ProcessingTaskUUID(BaseModel):
    uuid: str


class ProcessingTask(ProcessingTaskUUID, ProcessingRequest):
    complete: bool = False
    data: Optional[dict] = None


class ProcessingTaskUpdate(ProcessingTask):
    process: Optional[str] = None