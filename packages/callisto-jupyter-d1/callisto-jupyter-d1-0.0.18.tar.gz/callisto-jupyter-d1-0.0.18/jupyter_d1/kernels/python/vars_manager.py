import json
from typing import List, Optional, Union

from ...logger import logger
from ...models.kernel_variable import KernelVariable, KernelVariableStats
from ...models.notebook import Filter
from ...settings import settings
from ...utils import NotebookNode
from ..vars_manager import VarsManager

# Prints list of current vars to stdout.
# Strange var names used to avoid affecting users
# variables.
raw_get_vars_code = """
try:
    import callisto as __d1_callisto
    print(__d1_callisto.format_vars(vars(), abbrev_len={abbrev_len}, no_preview=True))
except Exception as e:
    print(e)
"""  # noqa

raw_get_single_var_code = """
try:
    import callisto as __d1_callisto
    print(
        __d1_callisto.format_var(
            {var_name},
            "{var_name}",
            page_size={page_size},
            page={page},
            sort_by={sort_by},
            ascending={ascending},
            filters={filters},
        )
    )
except Exception as e:
    print(e)
"""  # noqa

raw_get_single_var_stats_code = """
try:
    import callisto as __d1_callisto
    print(
        __d1_callisto.get_var_stats(
            {var_name},
            "{var_name}",
            column={column},
        )
    )
except Exception as e:
    print(e)
"""  # noqa


class PythonVarsManager(VarsManager):
    def get_vars_code(self) -> str:
        return raw_get_vars_code.format(abbrev_len=settings.VAR_ABBREV_LEN)

    def get_single_var_code(
        self,
        var_name: str,
        page_size: Optional[int],
        page: int,
        sort_by: Optional[List[Union[str, int]]] = None,
        ascending: Optional[Optional[List[bool]]] = None,
        filters: Optional[List[Filter]] = None,
    ) -> str:
        return raw_get_single_var_code.format(
            var_name=var_name,
            page_size=page_size,
            page=page,
            sort_by=sort_by,
            ascending=ascending,
            filters=[vars(filter) for filter in filters] if filters else None,
        )

    def get_single_var_stats_code(
        self, var_name: str, column: Optional[str] = None
    ) -> str:
        return raw_get_single_var_stats_code.format(
            var_name=var_name, column=f"'{column}'" if column else "None"
        )

    def parse_vars_response(
        self, vars_response: NotebookNode
    ) -> List[KernelVariable]:
        vars: List[KernelVariable] = []
        if "text" not in vars_response:
            return vars
        try:
            json_vars = json.loads(vars_response.text)
            for json_var in json_vars:
                vars.append(
                    KernelVariable(
                        name=json_var.get("name"),
                        type=json_var.get("type"),
                        abbreviated=json_var.get("has_next_page"),
                        has_next_page=json_var.get("has_next_page"),
                        value=json_var.get("value"),
                        summary=json_var.get("summary"),
                    )
                )
        except Exception as e:
            logger.debug(
                f"Exception parsing vars for python kernel: {e}, "
                f"{vars_response.text}"
            )
        return vars

    def parse_single_var_response(
        self, var_response: NotebookNode
    ) -> Optional[KernelVariable]:
        var = None
        if "text" not in var_response:
            return var
        try:
            json_var = json.loads(var_response.text)
            var = KernelVariable(
                name=json_var.get("name"),
                type=json_var.get("type"),
                abbreviated=json_var.get("has_next_page"),
                has_next_page=json_var.get("has_next_page"),
                value=json_var.get("value"),
                summary=json_var.get("summary"),
            )
        except Exception as e:
            logger.debug(
                f"Exception parsing var for python kernel: {e}, "
                f"{var_response.text}"
            )
        return var

    def parse_single_var_stats_response(
        self, var_response: NotebookNode
    ) -> Optional[KernelVariableStats]:
        var = None
        if "text" not in var_response:
            return var
        try:
            json_var = json.loads(var_response.text)
            var = KernelVariableStats(stats=json_var)
        except Exception as e:
            logger.debug(
                f"Exception parsing variable stats for python kernel: {e}, "
                f"{var_response.text}"
            )
        return var
