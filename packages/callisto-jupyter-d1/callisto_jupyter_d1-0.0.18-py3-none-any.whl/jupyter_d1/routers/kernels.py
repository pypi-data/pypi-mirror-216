import functools
from operator import itemgetter
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ..deps import write_access
from ..models.kernel import KernelIsAlive, KernelsIdle
from ..models.kernel_spec import KernelSpec, KernelSpecsWrapper
from ..settings import callisto_env
from ..storage import kmanager, manager

router = APIRouter()


@router.get("/specs", response_model=KernelSpecsWrapper)
async def list_kernel_specs():
    """
    Return a list of all kernel specs available on the server.

    The order is Python, R, anything else, with default Callisto kernels
    listed first in the language subgroups
    """
    kspecs = list(kmanager.get_all_kernelspecs().values())

    kspecs.sort(key=itemgetter("kernel_name"))

    language_grps = {}
    for spec in kspecs:
        language = spec["spec"]["language"].lower()
        if language in language_grps:
            language_grps[language].append(spec)
        else:
            language_grps[language] = [spec]

    def specSortKey(spec):
        priority = 0

        if (
            callisto_env != "local"
            and spec["spec"]["metadata"].get("conda_env_name", None)
            == "callisto"
        ) or (
            callisto_env == "local"
            and spec["spec"]["display_name"].lower() == "python 3 (ipykernel)"
        ):
            pass
        else:
            priority += 10
        return priority

    for speclist in language_grps.values():
        speclist.sort(key=specSortKey)

    specs = (
        language_grps.pop("python", [])
        + language_grps.pop("r", [])
        + functools.reduce(lambda a, b: a + b, language_grps.values(), [])
    )

    kernel_specs = [KernelSpec(order=i, **s) for i, s in enumerate(specs)]
    return KernelSpecsWrapper(kernel_specs=kernel_specs)


@router.get(
    "/shutdown/{uuid}",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def shutdown_kernel(uuid: UUID):
    """Shutdown the kernel identified by the uuid"""
    await kmanager.shutdown_kernel(uuid)


@router.get(
    "/restart/{uuid}",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def restart_kernel(uuid: UUID):
    """Restart the kernel identified by the uuid"""
    await kmanager.restart_kernel(uuid)


@router.get(
    "/interrupt/{uuid}",
    dependencies=[Depends(write_access)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def interrupt_kernel(uuid: UUID):
    """Interrupt the kernel identified by the uuid"""
    await kmanager.interrupt_kernel(uuid)


@router.get("/is_alive/{uuid}", response_model=KernelIsAlive)
async def kernel_is_alive(uuid: UUID):
    """Check that kernel process is running."""
    is_alive = kmanager.kernel_is_alive(uuid)
    return KernelIsAlive(kernel_is_alive=is_alive, kernel_id=uuid)


@router.get(
    "/idle", status_code=status.HTTP_200_OK, response_model=KernelsIdle
)
async def idle_status():
    """Check if all kernels are idle"""
    if not kmanager.kernels_warmed:
        raise HTTPException(400, "Kernels not warmed up")
    return KernelsIdle(idle=manager.is_idle(), last_idle=manager.last_idle)
