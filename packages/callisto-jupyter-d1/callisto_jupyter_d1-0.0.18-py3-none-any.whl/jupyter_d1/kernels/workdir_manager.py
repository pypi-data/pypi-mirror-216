from abc import ABC, abstractmethod
from typing import Optional

from ..utils import NotebookNode


class WorkDirManager(ABC):
    def __init__(self, workdir: str):
        self._workdir = workdir
        self._last_set_workdir: Optional[str] = None

    @property
    def workdir(self) -> str:
        return self._workdir

    @property
    def last_set_workdir(self) -> Optional[str]:
        """
        The last workdir that was set explicitly (i.e. via the
        change-working-directory UI, not as a byproduct of code
        the user ran), stored for use after kernel restart
        """
        return self._last_set_workdir

    @abstractmethod
    def get_chdir_code(self, directory: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_cwd_code(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_chdir_response(self, response: NotebookNode) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_cwd_response(self, response: NotebookNode) -> str:
        raise NotImplementedError

    def parse_chdir_output(self, output: NotebookNode) -> str:
        self._workdir = self.parse_chdir_response(output)
        self._last_set_workdir = self._workdir
        return self._workdir

    def parse_cwd_output(self, output: NotebookNode) -> str:
        self._workdir = self.parse_cwd_response(output)
        return self._workdir
