from typing import Any, Dict, Optional

from ..storage import bg_kernel_runner
from .dependency_manager import DependencyManager
from .python import PythonDependencyManager
from .r import RDependencyManager

# kernel_name to DependencyManager
dependency_managers: Dict[str, Any] = {}


def get_dependency_manager(
    kernel_name: str, kernelspec: Dict[str, Any]
) -> Optional[DependencyManager]:
    if kernel_name not in dependency_managers:
        language = kernelspec["spec"]["language"]
        if language == "python":
            dependency_managers[kernel_name] = PythonDependencyManager(
                kernel_name, kernelspec, bg_kernel_runner
            )
        elif language == "R":
            dependency_managers[kernel_name] = RDependencyManager(
                kernel_name, kernelspec, bg_kernel_runner
            )
        else:
            return None

    return dependency_managers[kernel_name]
