"""
"""
from __future__ import annotations

from typing import overload

from .config import Config
from .gpu.decorator import GPU
from .utils import CallableT


gradio_auto_wrap_enabled = Config.gradio_auto_wrap

def disable_gradio_auto_wrap():
    global gradio_auto_wrap_enabled
    gradio_auto_wrap_enabled = False

def enable_gradio_auto_wrap():
    global gradio_auto_wrap_enabled
    gradio_auto_wrap_enabled = True


@overload
def gradio_auto_wrap(task: CallableT) -> CallableT: ...
@overload
def gradio_auto_wrap(task: None) -> None: ...

def gradio_auto_wrap(task: CallableT | None) -> (CallableT | None):
    """
    """
    if not gradio_auto_wrap_enabled:
        return task
    if not callable(task):
        return task
    return GPU(task) # type: ignore
