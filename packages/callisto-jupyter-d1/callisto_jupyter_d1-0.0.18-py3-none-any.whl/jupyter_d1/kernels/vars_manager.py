from abc import ABC, abstractmethod
from typing import List, Optional, Union

from ..models.kernel_variable import KernelVariable, KernelVariableStats
from ..models.notebook import Filter
from ..utils import NotebookNode

# TODO: Send updates as diffs


class VarsManager(ABC):
    def __init__(self):
        self._vars = []
        self._tmp_vars = []

    @abstractmethod
    def get_vars_code(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_single_var_code(
        self,
        var_name: str,
        page_size: Optional[int],
        page: int,
        sort_by: Optional[List[Union[str, int]]] = None,
        ascending: Optional[Optional[List[bool]]] = None,
        filters: Optional[List[Filter]] = None,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_single_var_stats_code(
        self, var_name: str, column: Optional[str] = None
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_vars_response(
        self, vars_response: NotebookNode
    ) -> List[KernelVariable]:
        raise NotImplementedError

    @abstractmethod
    def parse_single_var_response(
        self, var_response: NotebookNode
    ) -> Optional[KernelVariable]:
        return None

    @abstractmethod
    def parse_single_var_stats_response(
        self, var_response: NotebookNode
    ) -> Optional[KernelVariableStats]:
        return None

    @property
    def vars(self) -> List[KernelVariable]:
        return self._vars

    def parse_output(self, vars_output: NotebookNode):
        vars = self.parse_vars_response(vars_output)
        self._tmp_vars += vars

    def on_request_start(self):
        self._tmp_vars = []

    def on_request_end(self) -> List[KernelVariable]:
        self._vars = self._tmp_vars
        return self._vars
