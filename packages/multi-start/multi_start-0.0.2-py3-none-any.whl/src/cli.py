import asyncio
import shlex
from typing import Optional

import typer
from typer import Typer

from .starter import RunConfig, Runner, Service

cli = Typer()


@cli.command()
def main(
    backend: bool = typer.Option(
        default=False,
        help="Enable backend service",
    ),
    backend_cmd: str = typer.Option(
        default="poetry run invoke serve",
        help="Command to start backend service",
    ),
    backend_dir: str = typer.Option(
        default=".",
        help="Working directory for a backend",
    ),
    backend_port: Optional[int] = typer.Option(
        default=None,
        help="Port number that backend is running at if port is used",
    ),
    backend_socket: str = typer.Option(
        default="/run/nginx/uvicorn.sock",
        help="UNIX socket path that backend is running at if socket is used",
    ),
    frontend: bool = typer.Option(
        default=False,
        help="Enable frontend service",
    ),
    frontend_port: Optional[int] = typer.Option(
        default=3000,
        help="Port number that frontend is running at",
    ),
    frontend_cmd: str = typer.Option(
        default="pnpm run start",
        help="Command to start frontend service",
    ),
    frontend_dir: str = typer.Option(
        default="../frontend",
        help="Working directory for a frontend",
    ),
    nginx: bool = typer.Option(
        default=False,
        help="Enable nginx",
    ),
    nginx_cmd: str = typer.Option(
        default='nginx -g "daemon off;"',
        help="Command to start Nginx",
    ),
    service_wait_time: int = typer.Option(
        default=3,
        help="How long to wait for a service to be up an running (sec)",
    ),
):
    if not any([backend, frontend, nginx]):
        raise RuntimeError("At least one service must be enabled")

    cfg = RunConfig(
        backend=Service(
            cmd=shlex.split(backend_cmd),
            cwd=backend_dir,
            port=backend_port,
            socket=backend_socket,
        )
        if backend
        else None,
        frontend=Service(
            cmd=shlex.split(frontend_cmd),
            cwd=frontend_dir,
            port=frontend_port,
        )
        if frontend
        else None,
        nginx=Service(
            cmd=shlex.split(nginx_cmd),
            cwd=".",
        )
        if nginx
        else None,
        svc_wait_time=service_wait_time,
    )

    asyncio.run(Runner(cfg).start())
