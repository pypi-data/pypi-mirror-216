from abc import ABC, abstractmethod
from typing import List, Optional

from .dependency_checker import DependencyChecker
from .vars_manager import VarsManager
from .workdir_manager import WorkDirManager


class KernelDefinition(ABC):
    @abstractmethod
    def create_vars_manager(self) -> VarsManager:
        raise NotImplementedError

    @abstractmethod
    def create_workdir_manager(self, workdir: str) -> WorkDirManager:
        raise NotImplementedError

    def create_dependency_checker(self) -> Optional[DependencyChecker]:
        return None

    @property
    def kernel_options(self) -> List[str]:
        return []

    @property
    def warmup_command(self) -> str:
        raise NotImplementedError
