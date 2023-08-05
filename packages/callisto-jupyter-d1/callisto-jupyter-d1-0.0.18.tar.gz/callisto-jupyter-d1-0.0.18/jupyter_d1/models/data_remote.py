from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .base_wrapper import BaseWrapper


class DataRemoteBase(BaseModel):
    id: int
    name: str
    remote_type: str
    owner_id: int
    organization_id: Optional[int] = None
    account_email: Optional[str] = None
    account_name: Optional[str] = None
    last_modified: datetime


class DataRemoteIn(DataRemoteBase):
    pass


class DataRemote(DataRemoteBase):
    path: str


class DataRemotesWrapper(BaseWrapper):
    data_remotes: List[DataRemote]
