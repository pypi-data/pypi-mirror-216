import asyncio
import os
import signal
import sys
from asyncio.subprocess import Process
from pathlib import Path
from typing import List, Optional

import httpx
from pydantic import BaseModel


class Service(BaseModel):
    cmd: List[str]
    cwd: str
    socket: Optional[str]
    port: Optional[int]


class RunConfig(BaseModel):
    backend: Optional[Service]
    frontend: Optional[Service]
    nginx: Optional[Service]
    svc_wait_time: int


async def run(cmd, cwd=None, pipe_output=False, extra_env=None) -> Process:
    """
    Run a process
    :param cmd: Command to run
    :param cwd: Working directory
    :param pipe_output: Whether to pipe the output or print it on screen instead
    :param extra_env: Extra environment variables
    :return: Process
    """
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    proc = await asyncio.create_subprocess_exec(
        cmd[0],
        *cmd[1:],
        stdout=asyncio.subprocess.PIPE if pipe_output else sys.stdout,
        stderr=asyncio.subprocess.PIPE if pipe_output else sys.stderr,
        cwd=cwd,
        env=env,
    )

    return proc


def debug_msg(msg: str) -> None:
    """
    Print message only when DEBUG environment variable is set
    :param msg: Message to print
    """
    if os.environ.get("DEBUG"):
        print(str)


async def run_and_wait(cmd, cwd=None):
    proc = await run(cmd, cwd)
    code = await proc.wait()
    if code != 0:
        raise RuntimeError(f"{cmd} failed with code {code}")


async def get_output(cmd, cwd=None) -> bytes:
    """
    Run command and get its stdout if completed successfully
    :param cmd: Command to run
    :param cwd: Working directory
    :return: Bytes from stdout
    """
    proc = await run(cmd, cwd, pipe_output=True)
    out, err = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"{cmd} failed with code {proc.returncode}")
    return out


async def stop_process(proc: Process, timeout=3.0) -> None:
    """
    Try to stop the process gracefully, otherwise killing it
    :param proc: Process to stop
    :param timeout: How long to wait for a graceful stop
    """
    if proc.returncode is not None:
        return
    proc.terminate()
    await asyncio.wait_for(proc.wait(), timeout=timeout)
    if proc.returncode is not None:
        return
    else:
        proc.kill()


async def setup_nginx() -> None:
    """
    Prepare Nginx.
    Optionally setup HTTP Basic Auth, if environment variables are provided.
    Process Nginx templates to build actual configuration files.
    """
    if user := os.environ.get("HTTP_BASIC_AUTH_USER"):
        pwd = os.environ["HTTP_BASIC_AUTH_PASSWORD"]
        await run_and_wait(["htpasswd", "-b", "-c", "/run/nginx/.htpasswd", user, pwd])
        if not os.environ.get("HTTP_BASIC_AUTH_REALM"):
            os.environ["HTTP_BASIC_AUTH_REALM"] = "Private area"

    for f in ["/etc/nginx/conf.d/default.conf", "/etc/nginx/dataspace-headers.conf"]:
        final_config = await get_output(["parse-template", f])
        Path(f).write_bytes(final_config)
        print(f"{f} is generated")

        if os.environ.get("NGINX_DEBUG"):
            print(f"=== {f} ===")
            print(Path(f).read_text("utf8") + "\n")


async def start_service(svc: Service, extra_env: Optional[dict] = None) -> Process:
    """
    Start a service.
    :param svc: Service to run
    :param extra_env: Extra environment variables
    :return: Process
    """
    debug_msg(f"Starting service: {svc.cmd}")
    return await run(svc.cmd, cwd=svc.cwd, extra_env=extra_env)


async def wait_for_service(svc: Service, timeout: int):
    """
    Wait until a service and up and listening for either a port or socket.
    Port takes precedence over a socket if both defined.
    :param svc: Service to wait for
    :param timeout: How long to wait in seconds
    """
    if not svc.socket and not svc.port:
        raise RuntimeError("Either socket or port should be defined")

    url = "http://localhost"
    transport = httpx.AsyncHTTPTransport(uds=svc.socket)

    if svc.port:
        transport = httpx.AsyncHTTPTransport()
        url += f":{svc.port}"

    async with httpx.AsyncClient(transport=transport) as client:
        wait_step = 0.3
        max_attempts = int(timeout / wait_step)
        for _ in range(max_attempts):
            try:
                await client.get(url)
            except httpx.ConnectError:
                await asyncio.sleep(wait_step)
            else:
                debug_msg(f"Connection established: {url}")
                break
        else:
            print("Service is not responding", svc)
            raise TimeoutError("Service is not responding")


class Runner:
    def __init__(self, cfg: RunConfig):
        self.cfg = cfg
        self._stop = asyncio.Event()

    def stop(self, *args):
        self._stop.set()

    async def start(self):
        # Handle Ctrl+C gracefully by stopping all running services
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, self.stop)
        loop.add_signal_handler(signal.SIGTERM, self.stop)
        cfg = self.cfg

        prerequisites = []
        procs = []

        if cfg.backend:
            procs.append(await start_service(cfg.backend))
            prerequisites.append(wait_for_service(cfg.backend, cfg.svc_wait_time))

        if cfg.frontend:
            frontend_svc = await start_service(
                cfg.frontend, extra_env={"PORT": str(cfg.frontend.port)}
            )
            procs.append(frontend_svc)
            prerequisites.append(wait_for_service(cfg.frontend, cfg.svc_wait_time))

        if cfg.nginx:
            prerequisites.append(setup_nginx())

        await asyncio.gather(*prerequisites)

        if cfg.nginx:
            procs.append(await start_service(cfg.nginx))

        tasks = [p.wait() for p in procs]
        tasks.append(self._stop.wait())
        await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        print("Shutting down all processes")
        await asyncio.gather(*[stop_process(proc) for proc in procs])
