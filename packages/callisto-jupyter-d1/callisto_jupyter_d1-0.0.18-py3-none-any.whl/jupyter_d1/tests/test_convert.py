import json
import tempfile
from io import StringIO
from typing import Dict

import pytest  # type: ignore
from pytest_mock import MockFixture

from .D1TestClient import TestClient
from .utils import compare_cells


def compare_notebooks(actual, expected):
    resp_cells = actual.pop("cells")
    expected_cells = expected.pop("cells")
    assert len(resp_cells) == len(expected_cells)
    for idx in range(len(resp_cells)):
        compare_cells(resp_cells[idx], expected_cells[idx])

    # Notebooks should match with the cells popped
    assert actual == expected


@pytest.mark.asyncio
async def test_convert_rmd_to_ipynb(
    client: TestClient,
    readonly_token_headers: Dict[str, str],
) -> None:
    with open("jupyter_d1/tests/notebooks/worldpop.Rmd", "rb") as f1:
        response = await client.post(
            "/convert/rmd_to_ipynb",
            files={"file": ("worldpop.Rmd", f1)},
            headers=readonly_token_headers,
        )
        with open("jupyter_d1/tests/notebooks/worldpop.ipynb", "rb") as f2:
            with tempfile.TemporaryFile() as ff:
                ff.write(response.content)
            resp_nb = json.loads(response.content.decode("utf-8"))
            expected_nb = json.load(f2)
            compare_notebooks(resp_nb, expected_nb)

    assert (
        response.headers["content-disposition"]
        == 'attachment; filename="worldpop.ipynb"'
    )


@pytest.mark.asyncio
async def test_convert_rmd_with_R_to_ipynb(
    client: TestClient,
    readonly_token_headers: Dict[str, str],
) -> None:
    with open("jupyter_d1/tests/notebooks/rmd_example.Rmd", "rb") as f1:
        response = await client.post(
            "/convert/rmd_to_ipynb",
            files={"file": ("rmd_example.Rmd", f1)},
            headers=readonly_token_headers,
        )
        with open("jupyter_d1/tests/notebooks/rmd_example.ipynb", "rb") as f2:
            resp_nb = json.loads(response.content.decode("utf-8"))
            expected_nb = json.load(f2)
            compare_notebooks(resp_nb, expected_nb)
            assert resp_nb["metadata"]["kernelspec"] == {
                "name": "ir",
                "language": "R",
                "display_name": "R",
            }

    assert (
        response.headers["content-disposition"]
        == 'attachment; filename="rmd_example.ipynb"'
    )


@pytest.mark.asyncio
async def test_convert_rmd_with_R_to_ipynb_no_R_kernel(
    client: TestClient,
    readonly_token_headers: Dict[str, str],
    mocker: MockFixture,
) -> None:
    kmanager = mocker.patch("jupyter_d1.routers.convert.kmanager")
    kmanager.get_kernelspec_by_name.return_value = (
        "python",
        {"spec": {"language": "python"}},
    )

    with open("jupyter_d1/tests/notebooks/rmd_example.Rmd", "rb") as f1:
        response = await client.post(
            "/convert/rmd_to_ipynb",
            files={"file": ("rmd_example.Rmd", f1)},
            headers=readonly_token_headers,
        )
        with open("jupyter_d1/tests/notebooks/rmd_example.ipynb", "rb") as f2:
            resp_nb = json.loads(response.content.decode("utf-8"))
            expected_nb = json.load(f2)
            compare_notebooks(resp_nb, expected_nb)
            assert resp_nb["metadata"]["kernelspec"] == {
                "name": "ir",
                "language": "R",
                "display_name": "R",
            }

    assert (
        response.headers["content-disposition"]
        == 'attachment; filename="rmd_example.ipynb"'
    )


@pytest.mark.asyncio
async def test_convert_rmd_to_ipynb_bogus_file(
    client: TestClient,
    readonly_token_headers: Dict[str, str],
    mocker: MockFixture,
) -> None:
    mock_jupytext = mocker.patch("jupyter_d1.routers.convert.jupytext")
    mock_jupytext.side_effect = KeyError("it did not work")

    response = await client.post(
        "/convert/rmd_to_ipynb",
        files={
            "file": (
                "meta_info.json",
                StringIO("%%%5not valid file\n````{{yurp}}\nprint(g)\n```"),
            )
        },
        headers=readonly_token_headers,
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Failed to convert Rmd file to ipynb, do you have "
        "an R kernel installed and added to the kernelspecs?"
    )


@pytest.mark.asyncio
async def test_convert_ipynb_to_rmd(
    client: TestClient,
    readonly_token_headers: Dict[str, str],
) -> None:
    with open("jupyter_d1/tests/notebooks/rmd_example.ipynb", "rb") as f1:
        response = await client.post(
            "/convert/ipynb_to_rmd",
            files={"file": ("rmd_example.ipynb", f1)},
            headers=readonly_token_headers,
        )
        with open("jupyter_d1/tests/notebooks/rmd_example.Rmd", "rb") as f2:
            lines = f2.readlines()
            rmd_content = b"".join(lines[4:])
            assert rmd_content in response.content

    assert (
        response.headers["content-disposition"]
        == 'attachment; filename="rmd_example.Rmd"'
    )
