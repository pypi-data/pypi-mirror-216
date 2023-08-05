from abc import ABC, abstractmethod
from typing import List

from ..utils import NotebookNode


class DependencyChecker(ABC):
    def __init__(self):
        self._missing_packages = []

    @property
    def missing_packages(self) -> List[str]:
        return self._missing_packages

    @abstractmethod
    def get_check_dependencies_code(self, notebook_code: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_check_dependencies_response(
        self, response: NotebookNode
    ) -> List[str]:
        raise NotImplementedError
