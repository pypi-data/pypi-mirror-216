#!/usr/bin/env python3

"""Common stuff shared among modules"""

import asyncio
import logging
import os
import shlex
from functools import wraps
from pathlib import Path
from subprocess import DEVNULL, CalledProcessError, check_output, run

# we need 3.8 compatible typing (python on build nodes)
from typing import Callable, Coroutine, Iterator, Union, cast

from asyncinotify import Event, Inotify, Mask

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("docker-shaper.utils")


def setup_logging(level: str = "INFO") -> None:
    """Make logging fun"""
    for lev in LOG_LEVELS:
        logging.addLevelName(getattr(logging, lev), f"({lev[0] * 2})")

    logging.basicConfig(
        format=(
            "%(levelname)s: %(message)s"
            if os.environ.get("USER") == "root"
            else "%(levelname)s %(asctime)s %(name)s: %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG if level == "ALL_DEBUG" else logging.WARNING,
    )
    logging.getLogger().setLevel(getattr(logging, level.split("_")[-1]))
    logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)


def watchdog(
    afunc: Callable[..., Coroutine[object, object, object]]
) -> Callable[..., Coroutine[object, object, object]]:
    """Watch for async functions to throw an unhandled exception"""

    @wraps(afunc)
    async def run(*args: object, **kwargs: object) -> object:
        """Run wrapped function and handle exceptions"""
        try:
            return await afunc(*args, **kwargs)
        except asyncio.CancelledError:
            log().info("Task cancelled: `%s`", afunc.__name__)
        except KeyboardInterrupt:
            log().info("KeyboardInterrupt in `%s`", afunc.__name__)
        except Exception:  # pylint: disable=broad-except
            log().exception("Exception in `%s`:", afunc.__name__)
            asyncio.get_event_loop().stop()
        return None

    return run


async def fs_changes(
    *paths: Path,
    queue: asyncio.Queue = asyncio.Queue(),
    mask: Mask = Mask.CLOSE_WRITE | Mask.MOVED_TO | Mask.CREATE,
    postpone: bool = False,
    timeout: float = 2,
) -> Iterator[Path]:
    """Controllable, timed filesystem watcher"""

    # pylint: disable=too-many-locals

    async def fuse_fn(queue: asyncio.Queue, timeout: float) -> None:
        await asyncio.sleep(timeout)
        await queue.put("timeout")

    def task(name: str) -> asyncio.Task:
        """Creates a task from a name identifying a data source to read from"""
        return asyncio.create_task(
            cast(Union[asyncio.Queue, Inotify], {"inotify": inotify, "mqueue": queue}[name]).get(),
            name=name,
        )

    with Inotify() as inotify:
        for path in paths:
            inotify.add_watch(path, mask)
        fuse = None
        changed_files = set()
        tasks = set(map(task, ("inotify", "mqueue")))

        while True:
            done, tasks = await asyncio.wait(
                fs=tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )
            for event in done:
                event_type, event_value = event.get_name(), event.result()
                tasks.add(task(event_type))
                if event_type == "inotify":
                    assert isinstance(event_value, Event)
                    if event_value.path:
                        changed_files.add(event_value.path)
                    if postpone and fuse:
                        fuse.cancel()
                        del fuse
                        fuse = None
                    if not fuse:
                        fuse = asyncio.create_task(fuse_fn(queue, timeout))
                elif event_type == "mqueue":
                    if event_value == "timeout":
                        del fuse
                        fuse = None
                        for file in changed_files:
                            yield file
                        changed_files.clear()


async def read_process_output(cmd: str) -> None:
    """Run a process asynchronously and handle each line on stdout using provided callback"""
    process = await asyncio.create_subprocess_exec(
        *shlex.split(cmd),
        stdout=asyncio.subprocess.PIPE,
    )
    assert process.stdout
    while True:
        if not (line := (await process.stdout.readline()).decode().strip("\n")):
            break
        yield line


def process_output(cmd: str) -> str:
    """Return command output as one blob"""
    return check_output(shlex.split(cmd), stderr=DEVNULL, text=True)
