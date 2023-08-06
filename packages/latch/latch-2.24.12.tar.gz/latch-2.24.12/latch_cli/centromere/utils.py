import builtins
import contextlib
import os
import random
import string
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Iterator, List, Optional

import docker
import paramiko
from flytekit.core.context_manager import FlyteContext, FlyteContextManager
from flytekit.core.data_persistence import FileAccessProvider
from flytekit.tools import module_loader

from latch_cli.constants import latch_constants


@contextlib.contextmanager
def _add_sys_paths(paths: List[Path]) -> Iterator[None]:
    paths = [os.fspath(p) for p in paths]
    try:
        for p in paths:
            sys.path.insert(0, p)
        yield
    finally:
        for p in paths:
            sys.path.remove(p)


def _import_flyte_objects(paths: List[Path], module_name: str = "wf"):
    with _add_sys_paths(paths):

        class FakeModule(ModuleType):
            def __getattr__(self, key):
                # This value is designed to be used in the execution of top
                # level code without throwing errors but need not do anything.
                # Here are some cases where this value can be used:
                #
                # ```
                # from foo import bar
                #
                # # Referencing an attribute from an attribute
                # a = bar.x
                #
                # # Calling an attribute
                # b = bar()
                #
                # # Subclassing from an attribute
                # class C(bar):
                # ```
                #     ...
                class FakeAttr:
                    def __new__(*args, **kwargs):
                        return None

                return FakeAttr

            __all__ = []

        real_import = builtins.__import__

        def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
            try:
                return real_import(
                    name,
                    globals=globals,
                    locals=locals,
                    fromlist=fromlist,
                    level=level,
                )
            except (ModuleNotFoundError, AttributeError) as e:
                return FakeModule(name)

        # Temporary ctx tells lytekit to skip local execution when
        # inspecting objects
        fap = FileAccessProvider(
            local_sandbox_dir=tempfile.mkdtemp(prefix="foo"),
            raw_output_prefix="bar",
        )
        tmp_context = FlyteContext(fap, inspect_objects_only=True)

        FlyteContextManager.push_context(tmp_context)
        builtins.__import__ = fake_import

        mods = list(module_loader.iterate_modules([module_name]))

        builtins.__import__ = real_import
        FlyteContextManager.pop_context()

        return mods


def _construct_dkr_client(ssh_host: Optional[str] = None):
    """Try many methods of establishing valid connection with client.

    This was helpful -
    https://github.com/docker/docker-py/blob/a48a5a9647761406d66e8271f19fab7fa0c5f582/docker/utils/utils.py#L321

    If `ssh_host` is passed, we attempt to make a connection with a remote
    machine.
    """

    def _from_env():
        host = environment.get("DOCKER_HOST")

        # empty string for cert path is the same as unset.
        cert_path = environment.get("DOCKER_CERT_PATH")
        if cert_path == "":
            cert_path = None

        # empty string for tls verify counts as "false".
        # Any value or 'unset' counts as true.
        tls_verify = environment.get("DOCKER_TLS_VERIFY") != ""

        enable_tls = tls_verify or cert_path is not None

        dkr_client = None
        try:
            if not enable_tls:
                dkr_client = docker.APIClient(host)
            else:
                if not cert_path:
                    cert_path = os.path.join(os.path.expanduser("~"), ".docker")

                tls_config = docker.tls.TLSConfig(
                    client_cert=(
                        os.path.join(cert_path, "cert.pem"),
                        os.path.join(cert_path, "key.pem"),
                    ),
                    ca_cert=os.path.join(cert_path, "ca.pem"),
                    verify=tls_verify,
                )
                dkr_client = docker.APIClient(host, tls=tls_config)

        except docker.errors.DockerException as de:
            raise OSError(
                "Unable to establish a connection to Docker. Make sure that"
                " Docker is running and properly configured before attempting"
                " to register a workflow."
            ) from de

        return dkr_client

    if ssh_host is not None:
        try:
            return docker.APIClient(ssh_host, use_ssh_client=True)
        except docker.errors.DockerException as de:
            raise OSError(
                f"Unable to establish a connection to remote docker host {ssh_host}."
            ) from de

    environment = os.environ
    host = environment.get("DOCKER_HOST")
    if host is not None and host != "":
        return _from_env()
    else:
        try:
            # TODO: platform specific socket defaults
            return docker.APIClient(base_url="unix://var/run/docker.sock")
        except docker.errors.DockerException as de:
            raise OSError(
                "Docker is not running. Make sure that"
                " Docker is running before attempting to register a workflow."
            ) from de


def _construct_ssh_client(internal_ip: str, username: str) -> paramiko.SSHClient:
    gateway = paramiko.SSHClient()
    gateway.load_system_host_keys()
    gateway.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy)
    gateway.connect(latch_constants.jump_host, username=latch_constants.jump_user)

    transport = gateway.get_transport()
    if transport is None:
        raise ConnectionError("unable to create connection to jump host")
    sock = transport.open_channel(
        kind="direct-tcpip",
        dest_addr=(internal_ip, 22),
        src_addr=("", 0),
    )

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy)
    ssh.connect(internal_ip, username=username, sock=sock)
    return ssh


class _TmpDir:

    """Represents a temporary directory that can be local or on a remote machine."""

    def __init__(
        self,
        remote=False,
        internal_ip: Optional[str] = None,
        username: Optional[str] = None,
    ):
        if remote and (internal_ip is None or username is None):
            raise ValueError("Must provide an ssh connection if remote is True.")

        self.remote = remote
        self.internal_ip = internal_ip
        self.username = username
        self._tempdir = None

    def __enter__(self, *args):
        return self.create(*args)

    def __exit__(self, *args):
        self.cleanup(*args)

    def create(self, *args):
        if not self.remote:
            self._tempdir = tempfile.TemporaryDirectory()
            return Path(self._tempdir.name).resolve()

        if self.internal_ip is None or self.username is None:
            raise ValueError("Must provide an ssh connection if remote is True.")

        td = "".join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8
            )
        )

        self._tempdir = f"/tmp/{td}"

        client = _construct_ssh_client(self.internal_ip, self.username)
        client.exec_command(f"mkdir {self._tempdir}")
        return self._tempdir

    def cleanup(self, *args):
        if (
            not self.remote
            and self._tempdir is not None
            and not isinstance(self._tempdir, str)
        ):
            self._tempdir.cleanup()
        elif not (self.internal_ip is None or self.username is None):
            client = _construct_ssh_client(self.internal_ip, self.username)
            client.exec_command(f"rm -rf {self._tempdir}")
