from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from .base_wrapper import BaseWrapper
from .JSONType import JSONType


class KernelVariable(BaseModel):
    name: str
    type: Optional[str]
    abbreviated: Optional[bool] = False
    has_next_page: Optional[bool] = False
    value: Optional[JSONType]
    summary: Optional[str]


class KernelVariableWrapper(BaseWrapper):
    single_var: KernelVariable


class KernelVariablesWrapper(BaseWrapper):
    vars: List[KernelVariable]


class ColumnStats(BaseModel):
    type: str
    min: Optional[Union[float, int, str]]
    max: Optional[Union[float, int, str]]
    mean: Optional[Union[float, int, str]]
    top_values: Optional[Dict[str, int]]
    unique_count: Optional[int]
    na_count: int


class KernelVariableStats(BaseModel):
    stats: Dict[str, ColumnStats]
