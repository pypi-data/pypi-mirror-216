import json
from typing import Any, List, Optional, Union

from ...logger import logger
from ...models.kernel_variable import KernelVariable, KernelVariableStats
from ...models.notebook import Filter
from ...settings import settings
from ...utils import NotebookNode
from ..vars_manager import VarsManager

raw_install_callistor_github_code = """
        if (!("remotes" %in% (.packages()))) {{
            if (length(find.package("remotes", quiet=TRUE)) < 1) {{
                install.packages("remotes")
            }}
        }}
        remotes::install_github("OakCityLabs/callisto-r", ref="{ref}", upgrade="never", quiet=FALSE)
"""  # noqa

raw_install_callistor_cran_code = """
        install.packages("callistor")
"""  # noqa

raw_load_callistor_code = """
if (!("callistor" %in% (.packages()))) {{
    tryCatch(
        {{
            if (
                length(find.package("callistor", quiet=TRUE)) < 1 ||
                packageVersion("callistor") != '{expected_version}'
            ) {{
                {install_callistor_code}
            }}
            library("callistor")
        }},
        error=function(err) {{
            cat('[{{"name": "callisto-r install error", "type": "error", "summary": "There was a problem installing callisto-r, try installing with remotes::install_github(\\'OakCityLabs/callisto-r\\', ref=\\'{ref}\\', upgrade=\\'never\\')", "has_next_page": false, "value": {{ "single_value": "error" }} }}]')
            stop(err)
        }}
    )
}}
"""  # noqa

raw_get_vars_code = """
{load_callistor_code}

cat(callistor::format_vars(environment(), {abbrev_len}, no_preview=TRUE))
"""  # noqa

# Note: we try to access the var first so it throws if it doesn't exist
raw_get_single_var_code = """
{load_callistor_code}

cat(callistor::format_var(environment(), "{var_name}", {page_size}, {page}, {sort_by}, {ascending}, {filters}))
"""  # noqa


raw_get_single_var_stats_code = """
{load_callistor_code}

cat(callistor::get_var_stats(environment(), "{var_name}", {column}))
"""  # noqa


def create_r_vector_from_python_list(list_in: List[Any]) -> str:
    """Create a string representation of an R vector"""

    def convertToR(item: Any) -> str:
        if isinstance(item, str):
            # Add quotation marks around strings
            return f'"{item}"'
        elif isinstance(item, bool):
            return str(item).upper()
        elif item is None:
            return "NA"
        else:
            return str(item)

    converted = ",".join([convertToR(x) for x in list_in])
    return f"c({converted})"


def create_filter_data_frame(list_in: List[Filter]) -> str:
    """Construct data.frame with columns 'col', 'search', 'min', and 'max'"""

    cols_str = create_r_vector_from_python_list([item.col for item in list_in])
    search_str = create_r_vector_from_python_list(
        [item.search for item in list_in]
    )
    min_str = create_r_vector_from_python_list([item.min for item in list_in])
    max_str = create_r_vector_from_python_list([item.max for item in list_in])

    return f"""
    data.frame(
        col={cols_str},
        search={search_str},
        min={min_str},
        max={max_str}
    )
    """


def get_load_callistor_code(from_github=True) -> str:
    return raw_load_callistor_code.format(
        install_callistor_code=raw_install_callistor_github_code.format(
            ref=settings.CALLISTOR_VERSION_TAG
        )
        if from_github
        else raw_install_callistor_cran_code,
        ref=settings.CALLISTOR_VERSION_TAG,
        expected_version=settings.CALLISTOR_VERSION,
    )


class RVarsManager(VarsManager):
    def get_vars_code(self) -> str:
        return raw_get_vars_code.format(
            load_callistor_code=get_load_callistor_code(
                settings.LOAD_CALLISTOR_FROM_GITHUB
            ),
            abbrev_len=settings.VAR_ABBREV_LEN,
        )

    def get_single_var_code(
        self,
        var_name: str,
        page_size: Optional[int],
        page: int,
        sort_by: Optional[List[Union[str, int]]] = None,
        ascending: Optional[List[bool]] = None,
        filters: Optional[List[Filter]] = None,
    ) -> str:
        sort_param = (
            create_r_vector_from_python_list(sort_by) if sort_by else "NULL"
        )
        asc_param = (
            create_r_vector_from_python_list(ascending)
            if ascending
            else "NULL"
        )
        filter_param = create_filter_data_frame(filters) if filters else "NULL"

        return raw_get_single_var_code.format(
            load_callistor_code=get_load_callistor_code(
                settings.LOAD_CALLISTOR_FROM_GITHUB
            ),
            var_name=var_name,
            page_size=page_size if page_size else "NULL",
            page=page,
            sort_by=sort_param,
            ascending=asc_param,
            filters=filter_param,
        )

    def get_single_var_stats_code(
        self,
        var_name: str,
        column: Optional[str] = None,
    ) -> str:
        return raw_get_single_var_stats_code.format(
            load_callistor_code=get_load_callistor_code(
                settings.LOAD_CALLISTOR_FROM_GITHUB
            ),
            var_name=var_name,
            column=f"'{column}'" if column else "NULL",
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
                        summary=str(json_var.get("summary")),
                        value=json_var.get("value"),
                    )
                )
        except Exception as e:
            print(e)
            logger.debug(
                f"Exception parsing vars for R kernel: {e}, "
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
                f"Exception parsing var for R kernel: {e}, "
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
                f"Exception parsing variable stats for R kernel: {e}, "
                f"{var_response.text}"
            )
        return var
