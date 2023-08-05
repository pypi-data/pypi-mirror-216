#!/usr/bin/env python3

"""Functionality that might change during runtime
"""
import asyncio
import logging
import os
import re
import time
from contextlib import suppress
from datetime import datetime, timedelta
from subprocess import CalledProcessError
from typing import MutableMapping, Optional

from aiodocker import DockerError
from quart import render_template

from docker_shaper.utils import process_output, watchdog


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("docker-shaper.dynamic")


def short_id(docker_id: str) -> str:
    """Return the 10-digit variant of a long docker ID
    >>> short_id("sha256:abcdefghijklmnop")
    'abcdefghij'
    """
    if not docker_id:
        return docker_id
    assert docker_id.startswith("sha256:")
    return docker_id[7:17]


def age_str(seconds: Optional[int]) -> str:
    """Turn a number of seconds into something human readable"""
    if seconds is None:
        return "Unknown"
    return str(timedelta(seconds=seconds))


def timestamp_from(string):
    with suppress(ValueError):
        return datetime.strptime(string[:26], "%Y-%m-%dT%H:%M:%S.%f")
    return None


def event_from(line: str):
    """Reads a line from event log and turns it into a tuple containing the data"""
    match = re.match(r"^(.*) \((.*)\)$", line)
    assert match, f"line did not match the expected format: {line!r}"
    cmd, params = match.groups()
    timestamp, object_type, operator, *cmd, uid = cmd.split(" ")
    assert len(timestamp) == 35
    assert (operator in {"exec_create:", "exec_start:", "health_status:"}) == bool(
        cmd
    ), f"{operator=} {cmd=} {line=}"
    assert object_type in {
        "container",
        "network",
        "image",
        "volume",
        "builder",
    }, f"{object_type}"
    assert operator in {
        "create",
        "destroy",
        "attach",
        "connect",
        "disconnect",
        "start",
        "die",
        "pull",
        "push",
        "tag",
        "save",
        "delete",
        "untag",
        "prune",
        "commit",
        "unpause",
        "resize",
        "exec_die",
        "exec_create:",
        "exec_start:",
        "health_status:",
        "mount",
        "unmount",
        "archive-path",
        "rename",
        "kill",
        "stop",
        "top",
        "pause",
    }, f"{operator}"
    assert len(uid) == 64 or (object_type, operator) in {
        ("image", "pull"),
        ("image", "push"),
        ("image", "tag"),
        ("image", "untag"),
        ("image", "save"),
        ("image", "delete"),
        ("image", "prune"),
        ("volume", "prune"),
        ("container", "prune"),
        ("network", "prune"),
        ("builder", "prune"),
    }, f"{len(uid)=} {(object_type, operator)}"
    return (
        int(
            datetime.strptime(
                f"{timestamp[:26]}{timestamp[-6:]}", "%Y-%m-%dT%H:%M:%S.%f%z"
            ).timestamp()
        ),
        object_type,
        operator,
        cmd,
        uid,
        dict(p.split("=") for p in params.split(", ")),
    )


def id_from(name: str) -> Optional[str]:
    """Looks up name using `docker inspect` and returns a 12 digit Docker ID"""
    with suppress(CalledProcessError):
        log().debug("resolve %s", name)
        return short_id(
            name
            if name.startswith("sha256:")
            else process_output(f"docker inspect --format='{{{{.Id}}}}' {name}")
        )
    return None


def lookup_id(ids: MutableMapping[str, Optional[str]], name: str) -> Optional[str]:
    """Looks up a given @name in @ids and resolves it first if not yet given"""
    if name not in ids:
        ids[name] = id_from(name)
    return ids[name]


async def handle_docker_event_line(global_state, line):
    """Read a `docker events` line and maintain the last-used information"""

    tstamp, object_type, operator, _cmd, _uid, params = event_from(line)
    if not object_type == "container" or operator == "prune":
        return
    # log().debug("docker event: %s", line)
    log().debug("handle docker event %s", (tstamp, _uid[:12], operator, params["image"]))
    if not (referenced_image_id := lookup_id(global_state.image_ids, params["image"])):
        return

    #    print(tstamp, object_type, operator, _cmd, _uid, params)

    global_state.event_horizon = min(global_state.event_horizon, tstamp)
    global_state.last_referenced[referenced_image_id] = max(
        global_state.last_referenced.setdefault(referenced_image_id, tstamp), tstamp
    )


def jobname_from(binds):
    candidates = [
        d.replace("/home/jenkins/workspace/", "").replace("/checkout", "")
        for b in binds or []
        for d in (b.split(":")[0],)
        if "workspace" in d
    ]
    if not len(candidates) == len(set(candidates)):
        print(binds)
    return candidates and candidates[0] or "--"


def cpu_perc(cpu_stats, last_cpu_stats):
    if not (
        cpu_stats
        and "system_cpu_usage" in cpu_stats
        and last_cpu_stats
        and "system_cpu_usage" in last_cpu_stats
    ):
        return 0
    return (
        (cpu_stats["cpu_usage"]["total_usage"] - last_cpu_stats["cpu_usage"]["total_usage"])
        / (cpu_stats["system_cpu_usage"] - last_cpu_stats["system_cpu_usage"])
        * cpu_stats["online_cpus"]
    )


def label_filter(label_values):
    return ",".join(
        w.replace("artifacts.lan.tribe29.com:4000", "A")
        for key, l in label_values.items()
        if key
        in (
            "org.tribe29.base_image",
            "org.tribe29.cmk_branch",
            "org.tribe29.cmk_edition_short",
            "org.tribe29.cmk_hash",
            "org.tribe29.cmk_version",
        )
        for w in l.split()
        if not (w.startswith("sha256") or len(w) == 64)
    )


async def dump_global_state(global_state):
    global_state.counter += 1
    print(global_state.intervals)
    print(f"counter: {global_state.counter}")
    print(f"images: {len(global_state.images)}")
    print(f"containers: {len(global_state.containers)}")
    print(f"tag_rules: {len(global_state.tag_rules)}")


async def dashboard(global_state):
    return await render_template(
        "dashboard.html",
        data={
            "refresh_interval": 3,
            "event_horizon": age_str(int(time.time() - global_state.event_horizon)),
            "containers": [
                {
                    "short_id": cnt["short_id"],
                    "name": cnt["name"],
                    "usage": mem_stats.get("usage", 0),
                    "cmd": " ".join(cnt["show"]["Config"]["Cmd"]),
                    "job": jobname_from(
                        cnt["show"]["HostConfig"]["Binds"]
                        or list(cnt["show"]["Config"]["Volumes"] or [])
                    ),
                    "cpu": cpu_perc(cpu_stats, last_cpu_stats),
                    "created_at": timestamp_from(cnt["show"]["Created"]),
                    "started_at": timestamp_from(cnt["show"]["State"]["StartedAt"]),
                    "status": cnt["show"]["State"]["Status"],
                    "hints": label_filter(cnt["show"]["Config"]["Labels"]),
                    "pid": int(cnt["show"]["State"]["Pid"]),
                    # "container": cnt["container"],
                }
                for cnt, mem_stats, cpu_stats, last_cpu_stats in (
                    (
                        c,
                        c["stats"].get("memory_stats", {}),
                        c["stats"]["cpu_stats"],
                        c["last_stats"].get("cpu_stats"),
                    )
                    for c in global_state.containers.values()
                    if c.keys() > {"short_id", "name", "stats"}
                )
            ],
            "images": [
                {
                    "short_id": image["short_id"],
                    "tags": image["tags"],
                    "created_at": image["created_at"],
                    "last_referenced": "abc",  # timestamp_from(cnt["show"]["Created"]),
                }
                for image in global_state.images.values()
            ],
        },
    )


async def print_container_stats(global_state):
    hostname = open("/etc/hostname").read().strip()
    stats = [
        {
            "short_id": cnt["short_id"],
            "name": cnt["name"],
            "usage": mem_stats.get("usage", 0),
            "cmd": " ".join(cnt["show"]["Config"]["Cmd"]),
            "job": jobname_from(
                cnt["show"]["HostConfig"]["Binds"] or list(cnt["show"]["Config"]["Volumes"] or [])
            ),
            "cpu": cpu_perc(cpu_stats, last_cpu_stats),
            "created_at": timestamp_from(cnt["show"]["Created"]),
            "started_at": timestamp_from(cnt["show"]["State"]["StartedAt"]),
            "status": cnt["show"]["State"]["Status"],
            "hints": label_filter(cnt["show"]["Config"]["Labels"]),
            "pid": int(cnt["show"]["State"]["Pid"]),
            "container": cnt["container"],
        }
        for cnt, mem_stats, cpu_stats, last_cpu_stats in (
            (
                c,
                c["stats"].get("memory_stats", {}),
                c["stats"]["cpu_stats"],
                c["last_stats"].get("cpu_stats"),
            )
            for c in global_state.containers.values()
            if c.keys() > {"short_id", "name", "stats"}
        )
    ]

    os.system("clear")
    print(f"=[ {hostname} ]======================================")
    print(
        f"{'ID':<12}  {'NAME':<25}"
        f" {'PID':>9}"
        f" {'CPU':>9}"
        f" {'MEM':>9}"
        f" {'UP':>9}"
        f" {'STATE':>9}"
        f" {'JOB':<60}"
        f" {'HINTS'}"
    )
    now = datetime.now()
    for s in sorted(stats, key=lambda e: e["pid"]):
        tds = int((now - (s["started_at"] or s["created_at"])).total_seconds())
        col_td = "\033[1m\033[91m" if tds // 3600 > 5 else ""
        dur_str = f"{tds//86400:2d}d+{tds//3600%24:02d}:{tds//60%60:02d}"
        col_mem = "\033[1m\033[91m" if s["usage"] >> 30 > 2 else ""
        mem_str = f"{(s['usage']>>20)}MiB"
        col_cpu = "\033[1m\033[91m" if s["cpu"] > 2 else ""
        container_is_critical = (
            (s["started_at"] and tds // 3600 > 5) or s["status"] == "exited" or not s["started_at"]
        )
        col_cpu = "\033[1m\033[91m" if s["cpu"] > 2 else ""
        print(
            f"{s['short_id']:<12}  {s['name']:<25}"
            f" {s['pid']:>9}"
            f" {col_cpu}{int(s['cpu'] * 100):>8}%\033[0m"
            f" {col_mem}{mem_str:>9}\033[0m"
            f" {col_td}{dur_str}\033[0m"
            f" {s['status']:>9}"
            f" {s['job']:<60}"
            f" {s['hints']}"
        )
        # if (
        #    (s["started_at"] and tds // 3600 > 5)
        #    or s["status"] == "exited"
        #    or not s["started_at"]
        # ):
        #    log(f"remove {s['short_id']}")
        #    await s["container"].delete(force=True)
    print(
        f"{'TOTAL':<12}  {len(stats):<25}"
        f" {'':>9}"
        f" {int(sum(s['cpu'] for s in stats)*1000) / 10:>8}%\033[0m"
        f" {int(sum(s['usage'] for s in stats) / (1<<30)*10) / 10:>6}GiB\033[0m"
        f" {''}"
        f" {'':>9}"
        f" {'':<60}"
        f" {''}"
    )


@watchdog
async def watch_container(container, containers):
    name = "unknown"
    try:
        containers[container.id]["container"] = container
        containers[container.id]["short_id"] = (short_id := container.id[:12])
        containers[container.id]["show"] = await container.show()
        containers[container.id]["name"] = (name := containers[container.id]["show"]["Name"][1:])
        log().info(">> new container: %s %s", short_id, name)
        async for stats in container.stats():
            containers[container.id]["last_stats"] = containers[container.id].get("stats", {})
            containers[container.id]["stats"] = stats
            containers[container.id]["show"] = await container.show()
    except DockerError as exc:
        log().error("DockerError: %s", exc)
    finally:
        log().info("<< container terminated: %s %s", short_id, name)
        del containers[container.id]


async def watch_images(docker_client, global_state):
    # TODO: also use events to register
    log().info("crawl images..")
    for image in await docker_client.images.list(all=True):
        log().debug(image)
        if True or image["Id"] not in global_state.images:
            global_state.images[image["Id"]] = {
                "short_id": short_id(image["Id"]),
                "created_at": image["Created"],
                "tags": image["RepoTags"],
                "size": image["Size"],
                "parent": short_id(image["ParentId"]),
            }


async def watch_containers(docker_client, global_state):
    # TODO: also use events to register
    log().info("crawl containers..")
    for container in await docker_client.containers.list(all=True):
        if container.id not in global_state.containers:
            global_state.containers[container.id] = {}
            asyncio.ensure_future(watch_container(container, global_state.containers))
