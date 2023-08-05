from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .JSONType import JSONType


class DependencyCommand(BaseModel):
    command: str
    subcommand: str
    args: List[str]
    request_id: UUID


class BaseResponse(BaseModel):
    status: str
    request_id: UUID


class ReceivedResponse(BaseResponse):
    status: str = "received"


class UpdateResponse(BaseResponse):
    status: str = "update"
    stdout: Optional[str] = None
    stderr: Optional[str] = None


class CompleteResponse(BaseResponse):
    status: str = "complete"
    payload: Optional[JSONType] = None


class FailedResponse(BaseResponse):
    status = "failed"
    info: str


class MissingDependenciesWrapper(BaseModel):
    missing_dependencies: List[str]
