import os
import yaml
from typing import Optional, Any

from config import SETTINGS
from app.schemas import Build
from app.errors import OperationError
from redis_staorage.connector import RedisConnector


def get_path():
    return os.path.join(os.path.dirname(os.path.abspath(SETTINGS.ROOT_DIRECTORY)), SETTINGS.YAML_DIRECTORY)


# TODO delete duplicates load_builds and load_tasks (one function)

def load_builds():
    path = get_path()

    with open(os.path.join(path, f"{SETTINGS.BUILDS_YAML_NAME}.{SETTINGS.YAML_EXTENSION}")) as file:
        builds = yaml.load(file, Loader=yaml.FullLoader)

    if builds is None:
        raise OperationError(
            status=1003,
            message="Empty yaml file with builds",
        )

    # TODO if not key name and key tasks in yaml file
    builds_with_task = {
        build_info["name"]: build_info["tasks"]
        for build_info in builds.get("builds", list())
    }

    if builds_with_task is None:
        raise OperationError(
            status=1004,
            message="Not key 'builds' in yaml file",
        )

    return builds_with_task


def load_tasks():
    path = get_path()

    with open(os.path.join(path, f"{SETTINGS.TASKS_YAML_NAME}.{SETTINGS.YAML_EXTENSION}")) as file:
        tasks = yaml.load(file, Loader=yaml.FullLoader)

    if tasks is None:
        raise OperationError(
            status=1005,
            message="Empty yaml file with tasks",
        )

    # TODO if not key name and key dependencies in yaml file
    tasks_with_dependencies = {
        task_info["name"]: task_info["dependencies"]
        for task_info in tasks.get("tasks", list())
    }

    if tasks_with_dependencies is None:
        raise OperationError(
            status=1006,
            message="Not key 'tasks' in yaml file",
        )

    return tasks_with_dependencies


def get_tasks_in_build(
    builds: dict[str, Any],
    build_name: str,
) -> Optional[list[str]]:
    """
    Gets a list of tasks for a build

    Args:
        builds: builds with tasks
        build_name: name of build

    Returns:
        List of tasks in build or None if there is no such build name
    """
    return builds.get(build_name)


def search_dependencies(
    all_tasks: dict[str, Any],
    upper_task: str,
    order_tasks: list[str] = None,
) -> list[str]:
    """
    Algorithm for determining tasks dependencies

    Args:
        all_tasks: tasks with dependencies
        upper_task: upper task node
        order_tasks: current tasks in order

    Returns:
        List of tasks for current node
    """
    if order_tasks is None:
        order_tasks = list()

    task_dependencies = all_tasks.get(upper_task)
    if task_dependencies is None:
        raise OperationError(
            status=1002,
            message="Not correct task name: it is missing from the system",
        )

    for task in task_dependencies:
        search_dependencies(
            all_tasks=all_tasks,
            upper_task=task,
            order_tasks=order_tasks
        )
        order_tasks.append(task)
    return order_tasks


def get_order_tasks(
    build: Build,
    connector: RedisConnector,
) -> list[str]:
    """
    Gets all tasks in build in order

    Args:
        build: pydantic model build
        connector: connector for redis

    Returns:
        List of tasks in order
    """
    tasks = list()

    all_builds: dict[str, Any] = connector.get_dict(key=SETTINGS.BUILDS_YAML_NAME)
    all_tasks: dict[str, Any] = connector.get_dict(key=SETTINGS.TASKS_YAML_NAME)

    tasks_in_build = get_tasks_in_build(
        builds=all_builds,
        build_name=build.build
    )

    if tasks_in_build is None:
        raise OperationError(
            status=1001,
            message="Not correct build name: it is missing from the system",
        )

    for task in tasks_in_build:
        tasks = search_dependencies(
            all_tasks=all_tasks,
            upper_task=task,
            order_tasks=tasks,
        )
        tasks.append(task)

    return tasks

