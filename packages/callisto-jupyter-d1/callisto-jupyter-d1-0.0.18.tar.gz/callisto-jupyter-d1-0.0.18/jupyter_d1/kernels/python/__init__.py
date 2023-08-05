from pathlib import Path
from typing import List, Optional

from ..kernel_definition import KernelDefinition
from .dependency_checker import DependencyChecker, PythonDependencyChecker
from .vars_manager import PythonVarsManager, VarsManager
from .workdir_manager import PythonWorkDirManager, WorkDirManager


class PythonKernelDefinition(KernelDefinition):
    def create_vars_manager(self) -> VarsManager:
        return PythonVarsManager()

    def create_workdir_manager(self, workdir: str) -> WorkDirManager:
        return PythonWorkDirManager(workdir)

    def create_dependency_checker(self) -> Optional[DependencyChecker]:
        return PythonDependencyChecker()

    @property
    def kernel_options(self) -> List[str]:
        return [
            f"--IPKernelApp.exec_files='{Path(__file__).parent.resolve()}"
            f"/startup/callisto_startup.py'"
        ]

    @property
    def warmup_command(self) -> str:
        return "6+7"


kernel_definition = PythonKernelDefinition()
