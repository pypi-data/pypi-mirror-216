"""
"""
from __future__ import annotations

import inspect
from typing import Callable

from ..config import Config
from ..utils import CallableT
from . import client
from .wrappers import regular_function_wrapper
from .wrappers import generator_function_wrapper


decorated_cache: dict[Callable, Callable] = {}


def GPU(task: CallableT) -> CallableT:

    if not Config.zero_gpu:
        return task

    if task in decorated_cache:
        return decorated_cache[task] # type: ignore

    if inspect.iscoroutinefunction(task):
        raise NotImplementedError

    if inspect.isgeneratorfunction(task):
        decorated = generator_function_wrapper(task)
    else:
        decorated = regular_function_wrapper(task)

    client.startup_report()
    decorated_cache.update({
        task:      decorated,
        decorated: decorated,
    })

    return decorated # type: ignore
