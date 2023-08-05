from typing import List, Optional, Union

from pydantic import BaseModel

from .base_wrapper import BaseWrapper
from .JSONType import JSONType


class NotebookWrapper(BaseWrapper):
    notebook: JSONType


class NotebooksWrapper(BaseWrapper):
    notebooks: List[JSONType]


class NotebookPath(BaseWrapper):
    path: str


class Filter(BaseModel):
    col: Union[str, int]
    search: Optional[str] = None
    min: Optional[Union[int, float]] = None
    max: Optional[Union[int, float]] = None


class MetadataWrapper(BaseWrapper):
    metadata: JSONType
