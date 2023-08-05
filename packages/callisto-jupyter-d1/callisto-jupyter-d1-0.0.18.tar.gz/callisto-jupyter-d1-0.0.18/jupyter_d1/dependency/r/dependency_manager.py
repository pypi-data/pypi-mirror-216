from typing import List

from ..dependency_manager import CommandType, DependencyManager


def install_command(names: List[str]) -> str:
    local_flag = "--local"
    if local_flag in names:
        names.remove(local_flag)
        repo = "NULL"
        src = "type='source'"
    else:
        repo = "'https://cran.microsoft.com'"
        src = ""

    nameStr = ", ".join(f'"{x}"' for x in names)  # quote and join with ,
    cmd = f"""
    install.packages(c({nameStr}), repos={repo}, {src})
    """
    return cmd


def remove_command(names: List[str]) -> str:
    nameStr = ", ".join(f'"{x}"' for x in names)  # quote and join with ,
    cmd = f"""
    remove.packages(c({nameStr}))
    """
    return cmd


def list_command() -> str:
    cmd = r"""
    my_packages <- as.data.frame(installed.packages()[ , c(1, 3:4)])

    json <- "["
    for(i in 1:nrow(my_packages)) {       # for-loop over rows
      row <- my_packages[i,]
      line <- sprintf("{\"name\": \"%s\", \"version\": \"%s\"}", row[[1]], row[[2]])
      json <- paste(json, line)
      if (i != nrow(my_packages)) {
        json <- paste(json, ",")
      }
      json <- paste(json, "\n")
    }
    json <- paste(json, "]\n")

    cat(json)
    """
    return cmd


class RDependencyManager(DependencyManager):
    async def execute(self, request_id, command, subcommand, args) -> str:

        command_type = CommandType.UNKOWNN
        source = f"warning('unknown command: {command} {subcommand} {args}')"
        if command == "rip":
            if subcommand == "list":
                command_type = CommandType.PIP_LIST
                source = list_command()
            elif subcommand == "install":
                command_type = CommandType.PIP_INSTALL
                source = install_command(args)
            elif subcommand == "uninstall":
                command_type = CommandType.PIP_UNINSTALL
                source = remove_command(args)

        await self.dispatch_execute(
            request_id=request_id, source=source, command_type=command_type
        )

        return source
