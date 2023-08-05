from typing import List, Optional, Union

from ...logger import logger
from ...models.kernel_variable import KernelVariable, KernelVariableStats
from ...models.notebook import Filter
from ...utils import NotebookNode
from ..vars_manager import VarsManager

raw_get_vars_code = """
env
"""  # noqa


class ZshVarsManager(VarsManager):
    def get_vars_code(self) -> str:
        return raw_get_vars_code

    def get_single_var_code(
        self,
        var_name: str,
        page_size: Optional[int],
        page: int,
        sort_by: Optional[List[Union[str, int]]] = None,
        ascending: Optional[Optional[List[bool]]] = None,
        filters: Optional[List[Filter]] = None,
    ) -> str:
        return ""

    def parse_vars_response(
        self, vars_response: NotebookNode
    ) -> List[KernelVariable]:
        vars = []
        try:
            line = vars_response.text.strip()
            name, value = line.split("=", 1)

            vars.append(
                KernelVariable(
                    name=name,
                    type=None,
                    value={"single_value": value},
                    summary=value,
                )
            )
        except Exception as e:
            logger.debug(
                f"Exception parsing var for zsh kernel: {e}, "
                f"{vars_response.text}"
            )
        return vars

    def parse_single_var_response(
        self, var_response: NotebookNode
    ) -> Optional[KernelVariable]:
        return None

    def get_single_var_stats_code(
        self,
        var_name: str,
        column: Optional[str] = None,
    ) -> str:
        return ""

    def parse_single_var_stats_response(
        self, var_response: NotebookNode
    ) -> Optional[KernelVariableStats]:
        return None
