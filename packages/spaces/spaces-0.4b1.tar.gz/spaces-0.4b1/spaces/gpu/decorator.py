"""
"""
from __future__ import annotations

import inspect
from typing import Callable

from ..utils import CallableT
from . import client
from .wrappers import regular_function_wrapper
from .wrappers import generator_function_wrapper


already_decorated: set[Callable] = set()


def GPU(task: CallableT) -> CallableT:

    if task in already_decorated:
        return task

    if inspect.iscoroutinefunction(task):
        raise NotImplementedError

    if inspect.isgeneratorfunction(task):
        decorated = generator_function_wrapper(task)
    else:
        decorated = regular_function_wrapper(task)

    client.startup_report()
    already_decorated.add(decorated)

    return decorated # type: ignore
