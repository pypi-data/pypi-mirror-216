#!/usr/bin/env python3

import asyncio
import importlib
import logging
import os
import time
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import MutableMapping

from aiodocker import Docker
from quart import Quart

from docker_shaper import dynamic
from docker_shaper.utils import fs_changes, read_process_output, watchdog

CONFIG_FILE = Path("~/.docker_shaper/config.py").expanduser()


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("docker-shaper.server")


@dataclass
class GlobalState:
    intervals: MutableMapping[str, float]

    image_ids: MutableMapping[str, object]

    images: MutableMapping[str, object]
    containers: MutableMapping[str, object]

    event_horizon: int
    last_referenced: MutableMapping[str, int]

    tag_rules: MutableMapping[str, int]

    def __init__(self):
        self.intervals = {
            "state": 2,
            "image_stats": 2,
            "image_update": 2,
            "container_update": 2,
            "container_stats": 2,
        }
        self.image_ids = {}
        self.images = {}
        self.containers = {}
        self.event_horizon = int(time.time())
        self.last_referenced = {}
        self.tag_rules = {}
        self.counter = 0


@watchdog
async def print_container_stats(global_state):
    while True:
        try:
            await dynamic.print_container_stats(global_state)
            await asyncio.sleep(global_state.intervals.get("container_stats"), 1)
        except Exception:
            log().exception("Unhandled exception caught!")
            await asyncio.sleep(5)


@watchdog
async def print_state(global_state):
    while True:
        try:
            await dynamic.dump_global_state(global_state)
            await asyncio.sleep(global_state.intervals.get("state", 1))
        except Exception:
            log().exception("Unhandled exception caught!")
            await asyncio.sleep(5)


@watchdog
async def watch_containers(global_state):
    # TODO: also use events to register
    try:
        docker = Docker()
        while True:
            try:
                await dynamic.watch_containers(docker, global_state)
                await asyncio.sleep(global_state.intervals.get("container_update", 1))
            except Exception:
                log().exception("Unhandled exception caught!")
                await asyncio.sleep(5)
    finally:
        await docker.close()


@watchdog
async def watch_images(global_state):
    # TODO: also use events to register
    try:
        docker = Docker()
        while True:
            try:
                await dynamic.watch_images(docker, global_state)
                await asyncio.sleep(global_state.intervals.get("image_update", 1))
            except Exception:
                log().exception("Unhandled exception caught!")
                await asyncio.sleep(5)
    finally:
        await docker.close()


def load_config(path, global_state):
    spec = spec_from_file_location("dynamic_config", path)
    if not (spec and spec.loader):
        raise RuntimeError("Could not load")
    module = module_from_spec(spec)
    print(module)
    # assert module
    # assert isinstance(spec.loader, SourceFileLoader)
    loader: SourceFileLoader = spec.loader
    loader.exec_module(module)
    try:
        module.modify(global_state)
    except AttributeError:
        log().warning("File %s does not provide a `modify(global_state)` function")


@watchdog
async def watch_fs_changes(global_state):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    async for changed_file in fs_changes(
        Path(dynamic.__file__).parent, CONFIG_FILE.parent, timeout=1
    ):
        log().info("file %s changed - reload module", changed_file)
        try:
            if changed_file == Path(dynamic.__file__):
                importlib.reload(dynamic)
            elif changed_file == CONFIG_FILE:
                load_config(CONFIG_FILE, global_state)

        except Exception:
            log().exception("Reloading dynamic part failed!")
            await asyncio.sleep(5)
    assert False


@watchdog
async def handle_docker_events(global_state):
    async for line in read_process_output("docker events"):
        try:
            await dynamic.handle_docker_event_line(global_state, line)
        except Exception:
            log().exception("Unhandled exception caught!")
            await asyncio.sleep(5)


def no_serve():
    global_state = GlobalState()
    load_config(CONFIG_FILE, global_state)
    with suppress(KeyboardInterrupt, BrokenPipeError):
        asyncio.ensure_future(watch_fs_changes(global_state))
        asyncio.ensure_future(print_container_stats(global_state))
        asyncio.ensure_future(print_state(global_state))
        asyncio.ensure_future(watch_containers(global_state))
        asyncio.ensure_future(watch_images(global_state))
        asyncio.ensure_future(handle_docker_events(global_state))
        asyncio.get_event_loop().run_forever()


def serve():
    """"""
    app = Quart(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    global_state = GlobalState()
    load_config(CONFIG_FILE, global_state)

    @app.route("/shutdown")  # , methods=['POST'])
    def shutdown():
        app.terminator.set()
        return "Server shutting down..."

    @watchdog
    async def self_destroy():
        await app.terminator.wait()
        print("BOOM")
        app.shutdown()
        asyncio.get_event_loop().stop()
        print("!!!!")

    @app.route("/", methods=["GET", "POST"])
    async def dashboard():
        return await dynamic.dashboard(global_state)

    @app.before_serving
    async def create_db_pool():
        asyncio.ensure_future(self_destroy())
        asyncio.ensure_future(watch_fs_changes(global_state))
        # asyncio.ensure_future(print_container_stats(global_state))
        asyncio.ensure_future(print_state(global_state))
        asyncio.ensure_future(watch_containers(global_state))
        asyncio.ensure_future(watch_images(global_state))
        asyncio.ensure_future(handle_docker_events(global_state))

    app.terminator = asyncio.Event()
    app.run(
        host="0.0.0.0",
        port=5432,
        debug=False,
        use_reloader=False,
        loop=asyncio.get_event_loop(),
    )
