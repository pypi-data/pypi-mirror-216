try:
    import pandas as pd

    pd.set_option("display.html.table_schema", True)

    import sys

    import IPython

    showtraceback = (
        IPython.core.interactiveshell.InteractiveShell.showtraceback
    )

    def __d1_exception_hook(self, *args, **kwargs):
        exc_info = sys.exc_info()

        if exc_info[0] and issubclass(exc_info[0], ModuleNotFoundError):
            name = exc_info[1].name
            print(
                f"___callisto_d1_command___"
                f'{{"command_type": "handle_import_error", "name": "{name}"}}'
                f"___callisto_d1_command___",
                end="",
            )
        showtraceback(self, *args, **kwargs)

    IPython.core.interactiveshell.InteractiveShell.showtraceback = (  # type: ignore
        __d1_exception_hook
    )
except Exception:
    pass
