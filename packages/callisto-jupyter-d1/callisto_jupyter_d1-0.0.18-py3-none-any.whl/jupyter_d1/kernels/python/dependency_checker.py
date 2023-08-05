import json
from typing import List

from ...logger import logger
from ...utils import NotebookNode
from ..dependency_checker import DependencyChecker
from .import_to_lib import import_to_lib

raw_check_dependencies_code = """
def __d1_check_dependencies():
    import ast
    import sys
    import json

    parsed = ast.parse({python_string})
    top_imported = set()
    for node in ast.walk(parsed):
        if isinstance(node, ast.Import):
            for name in node.names:
                top_imported.add(name.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level > 0:
                # Relative imports always refer to the current package.
                continue
            assert node.module
            top_imported.add(node.module.split('.')[0])

    import importlib.util
    missing_imports = []
    for imp in top_imported:
        if importlib.util.find_spec(imp) is None:
            missing_imports.append(imp)
    print(json.dumps(missing_imports))

__d1_check_dependencies()
"""


class PythonDependencyChecker(DependencyChecker):
    def get_check_dependencies_code(self, notebook_code: str) -> str:
        return raw_check_dependencies_code.format(
            python_string=f"import callisto\n{notebook_code}".encode("utf-8")
        )

    def parse_check_dependencies_response(
        self, response: NotebookNode
    ) -> List[str]:
        deps: List[str] = []
        if "text" not in response:
            return deps
        try:
            raw_deps = json.loads(response.text)
            for raw_dep in raw_deps:
                if raw_dep in import_to_lib:
                    deps.append(import_to_lib[raw_dep])
                else:
                    deps.append(raw_dep)
            return deps
        except Exception as e:
            logger.debug(
                f"Exception parsing dependency checker response for python kernel: {e},"
                f" {response.text}"
            )
        return deps
