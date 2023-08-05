import json
from typing import Dict
from unittest import TestCase

import pytest  # type: ignore
from pytest_mock import MockFixture  # type: ignore

from jupyter_d1.storage import kmanager
from jupyter_d1.storage.kernel_manager import KernelManager

from .D1TestClient import TestClient

pytestmark = pytest.mark.asyncio


class TestKernels:
    def assert_zsh_spec(self, kern):
        assert kern["kernel_name"] == "zsh"
        assert kern["resource_dir"][-11:] == "kernels/zsh"
        spec = kern["spec"]
        assert "python" in spec["argv"][0]
        assert spec["argv"][1:] == [
            "-m",
            "zsh_jupyter_kernel",
            "-f",
            "{connection_file}",
        ]
        assert spec["env"] == {}
        assert spec["metadata"] == {}
        assert spec["display_name"] == "Z shell"
        assert spec["language"] == "zsh"
        assert spec["interrupt_mode"] == "signal"

    def assert_python3_spec(self, kern):
        assert kern["kernel_name"] == "python3"
        assert kern["resource_dir"][-15:] == "kernels/python3"
        spec = kern["spec"]
        assert "python" in spec["argv"][0]
        assert spec["argv"][1:] == [
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}",
        ]
        assert spec["env"] == {}
        assert spec["metadata"] == {"debugger": True}
        assert spec["display_name"] == "Python 3 (ipykernel)"
        assert spec["language"] == "python"
        assert spec["interrupt_mode"] == "signal"

    def assert_bash_spec(self, kern):
        assert kern["kernel_name"] == "bash"
        assert kern["resource_dir"][-12:] == "kernels/bash"
        spec = kern["spec"]
        assert "python" in spec["argv"][0]
        assert spec["argv"][1:] == [
            "-m",
            "bash_kernel",
            "-f",
            "{connection_file}",
        ]
        assert spec["env"] == {"PS1": "$"}
        assert spec["metadata"] == {}
        assert spec["display_name"] == "Bash"
        assert spec["language"] == "bash"
        assert spec["interrupt_mode"] == "signal"

    def assert_r_spec(self, kern):
        assert kern["kernel_name"] == "ir"
        assert kern["resource_dir"][-10:] == "kernels/ir"
        spec = kern["spec"]
        assert "/R" in spec["argv"][0]
        assert spec["argv"][1:] == [
            "--slave",
            "-e",
            "IRkernel::main()",
            "--args",
            "{connection_file}",
        ]
        assert spec["env"] == {}
        assert spec["metadata"] == {}
        assert spec["display_name"] == "R"
        assert spec["language"] == "R"
        assert spec["interrupt_mode"] == "signal"

    async def test_specs(
        self, client: TestClient, superuser_token_headers: Dict[str, str]
    ):
        response = await client.get(
            "/kernels/specs", headers=superuser_token_headers
        )
        assert response.status_code == 200
        specs = response.json()["kernel_specs"]
        assert len(specs) >= 4

        count = 0
        for kern in specs:
            if kern["kernel_name"] == "zsh":
                self.assert_zsh_spec(kern)
            elif kern["kernel_name"] == "python3":
                self.assert_python3_spec(kern)
            elif kern["kernel_name"] == "bash":
                self.assert_bash_spec(kern)
            elif kern["kernel_name"] == "ir":
                self.assert_r_spec(kern)
            assert kern["order"] == count
            count += 1

    async def test_specs_order_d1(
        self,
        client: TestClient,
        mocker: MockFixture,
        superuser_token_headers: Dict[str, str],
    ):
        """
        Several kernels, order should be python, r, others, with
        callisto env kernels first
        """
        mock_kmanager = mocker.patch("jupyter_d1.routers.kernels.kmanager")
        with open(
            "jupyter_d1/tests/mock_responses/kernelspecs.json", "r"
        ) as f:
            kerns = json.load(f)
        for k, v in kerns.items():
            v["kernel_name"] = k
        mock_kmanager.get_all_kernelspecs.return_value = kerns
        mocker.patch("jupyter_d1.routers.kernels.callisto_env", "staging")

        response = await client.get(
            "/kernels/specs", headers=superuser_token_headers
        )
        assert response.status_code == 200
        specs = response.json()["kernel_specs"]
        assert len(specs) == 8
        kernel_names = [s["kernel_name"] for s in specs]
        assert kernel_names == [
            "conda-env-callisto-py",
            "conda-env-jupyter_d1-py",
            "python3",
            "conda-env-callisto-r",
            "ir",
            "conda-env-callisto-bash",
            "bash",
            "conda-env-callisto-zsh",
        ]

    async def test_specs_order_local(
        self,
        client: TestClient,
        mocker: MockFixture,
        superuser_token_headers: Dict[str, str],
    ):
        """
        Local kernels, order should be python, r, others, with
        "Python 3 (ipykernel)" first
        """
        mock_kmanager = mocker.patch("jupyter_d1.routers.kernels.kmanager")
        with open(
            "jupyter_d1/tests/mock_responses/kernelspecs.json", "r"
        ) as f:
            kerns = json.load(f)
        for k, v in kerns.items():
            v["kernel_name"] = k
        mock_kmanager.get_all_kernelspecs.return_value = kerns
        mocker.patch("jupyter_d1.routers.kernels.callisto_env", "local")

        response = await client.get(
            "/kernels/specs", headers=superuser_token_headers
        )
        assert response.status_code == 200
        specs = response.json()["kernel_specs"]
        assert len(specs) == 8
        kernel_names = [s["kernel_name"] for s in specs]
        assert kernel_names == [
            "python3",
            "conda-env-callisto-py",
            "conda-env-jupyter_d1-py",
            "conda-env-callisto-r",
            "ir",
            "bash",
            "conda-env-callisto-bash",
            "conda-env-callisto-zsh",
        ]

        mocker.patch("jupyter_d1.routers.kernels.callisto_env", "staging")


class TestKernelsPermissions:
    async def test_specs(
        self,
        client: TestClient,
        readonly_token_headers: Dict[str, str],
        permissionless_token_headers: Dict[str, str],
    ):
        response = await client.get(
            "/kernels/specs", headers=permissionless_token_headers
        )
        assert response.status_code == 403
        response = await client.get(
            "/kernels/specs", headers=readonly_token_headers
        )
        assert response.status_code == 200


class TestKernelManager:
    @pytest.mark.asyncio
    async def test_warmup_python(self):
        assert await kmanager.warmup("python3")

    @pytest.mark.asyncio
    async def test_warmup_r(self):
        return
        assert await kmanager.warmup("ir", timeout=420)

    @pytest.mark.asyncio
    async def test_warmup_kernels(self):
        kernel_manager = KernelManager()
        assert kernel_manager.kernels_warmed is False
        kernel_manager.warmup_kernels(["python3", "ir"])
        await kernel_manager.parent_warmup_task
        assert kernel_manager.kernels_warmed is True

    @pytest.mark.asyncio
    async def test_warmup_kernels_prewarmed(self):
        kernel_manager = KernelManager()
        assert kernel_manager.kernels_warmed is False
        kernel_manager.warmup_kernels(
            ["python3", "ir"],
            "jupyter_d1/tests/mock_responses/prewarmed_kernels.json",
        )
        assert kernel_manager.kernels_warmed is True

    def test_get_all_kernelspecs_work_node_d1(
        self, mocker: MockFixture, ututils: TestCase
    ):
        mock_spec_manager = mocker.MagicMock()
        with open(
            "jupyter_d1/tests/mock_responses/kernelspecs.json", "r"
        ) as f:
            mock_spec_manager.get_all_specs.return_value = json.load(f)

        mocker.patch(
            "jupyter_d1.storage.kernel_manager.callisto_env", "staging"
        )

        kernel_manager = KernelManager()
        kernel_manager._specManager = mock_spec_manager

        specs = kernel_manager.get_all_kernelspecs()
        assert len(specs) == 6
        kernel_names = specs.keys()
        ututils.assertCountEqual(
            kernel_names,
            [
                "conda-env-callisto-py",
                "conda-env-callisto-r",
                "ir",
                "conda-env-callisto-bash",
                "bash",
                "conda-env-callisto-zsh",
            ],
        )

    def test_get_all_kernelspecs_local(
        self, mocker: MockFixture, ututils: TestCase
    ):
        mock_spec_manager = mocker.MagicMock()
        with open(
            "jupyter_d1/tests/mock_responses/kernelspecs.json", "r"
        ) as f:
            mock_spec_manager.get_all_specs.return_value = json.load(f)

        mocker.patch("jupyter_d1.storage.kernel_manager.callisto_env", "local")

        kernel_manager = KernelManager()
        kernel_manager._specManager = mock_spec_manager

        specs = kernel_manager.get_all_kernelspecs()
        assert len(specs) == 8
        kernel_names = specs.keys()
        ututils.assertCountEqual(
            kernel_names,
            [
                "python3",
                "conda-env-callisto-py",
                "conda-env-jupyter_d1-py",
                "conda-env-callisto-r",
                "ir",
                "bash",
                "conda-env-callisto-bash",
                "conda-env-callisto-zsh",
            ],
        )
