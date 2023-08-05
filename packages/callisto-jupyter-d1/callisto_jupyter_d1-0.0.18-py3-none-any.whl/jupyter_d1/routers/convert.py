import json
import shutil
import traceback
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Optional, Tuple

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from jupytext.cli import jupytext  # type: ignore
from starlette.responses import StreamingResponse

from ..d1_response import D1Response
from ..logger import logger
from ..storage import kmanager

COPY_BUFSIZE = 64 * 1024

router = APIRouter(default_response_class=D1Response)


@router.post(
    "/rmd_to_ipynb",
    status_code=status.HTTP_200_OK,
)
def convert_rmd_to_ipynb(file: UploadFile = File(...)):
    kinfo: Optional[
        Tuple[str, Dict[str, Any]]
    ] = kmanager.get_kernelspec_by_name("ir", language="r")
    if kinfo is not None and kinfo[1]["spec"]["language"].lower() != "r":
        kinfo = None

    out_file = NamedTemporaryFile(mode="rb", suffix=".ipynb")
    try:

        with NamedTemporaryFile(mode="wb", suffix=".Rmd") as f:
            shutil.copyfileobj(file.file, f)
            f.seek(0)

            jupytext_command = [
                f.name,
                "--from",
                "rmarkdown",
                "--to",
                "notebook",
                "--output",
                out_file.name,
            ]

            # Set kernelspec manually, if no R kernel was found then best
            # effort to set language to R
            if kinfo is not None:
                kspec = {
                    "name": kinfo[0],
                    "language": kinfo[1]["spec"]["language"],
                    "display_name": kinfo[1]["spec"]["display_name"],
                }
            else:
                kspec = {"name": "ir", "language": "R", "display_name": "R"}

            raw_metadata = json.dumps({"kernelspec": kspec})

            jupytext_command += ["--update-metadata", raw_metadata]

            jupytext(jupytext_command)
    except Exception as e:
        logger.info(
            f"Failed to convert Rmd file to ipynb {e} \n"
            f"{traceback.format_exc()}"
        )
        msg = "Failed to convert Rmd file to ipynb"
        if isinstance(e, KeyError):
            msg += ", do you have an R kernel installed and added to the kernelspecs?"
        raise HTTPException(400, msg)

    filename = file.filename
    if filename is None or len(filename) < 1:
        filename = "notebook"
    headers = {
        "content-disposition": f'attachment; filename="{Path(filename).stem}.ipynb"'
    }
    out_file.seek(0)

    def iterfile():
        yield from out_file

    return StreamingResponse(
        content=iterfile(),
        headers=headers,
        media_type="application/x-ipynb+json",
    )


@router.post(
    "/ipynb_to_rmd",
    status_code=status.HTTP_200_OK,
)
def convert_ipynb_to_rmd(file: UploadFile = File(...)):

    out_file = NamedTemporaryFile(mode="rb", suffix=".Rmd")
    try:

        with NamedTemporaryFile(mode="wb", suffix=".ipynb") as f:
            shutil.copyfileobj(file.file, f)
            f.seek(0)

            jupytext_command = [
                f.name,
                "--from",
                "notebook",
                "--to",
                "rmarkdown",
                "--output",
                out_file.name,
            ]

            jupytext(jupytext_command)
    except Exception as e:
        msg = "Failed to convert ipynb file to Rmd"
        logger.info(
            f"{msg} {e} \n"
            f"{traceback.format_exc()}"
        )
        raise HTTPException(400, msg)

    filename = file.filename
    if filename is None or len(filename) < 1:
        filename = "notebook"
    headers = {
        "content-disposition": f'attachment; filename="{Path(filename).stem}.Rmd"'
    }
    out_file.seek(0)

    def iterfile():
        yield from out_file

    return StreamingResponse(
        content=iterfile(),
        headers=headers,
        media_type="text/plain",
    )
