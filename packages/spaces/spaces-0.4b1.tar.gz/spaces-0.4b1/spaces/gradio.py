"""
"""
from __future__ import annotations

from typing import overload

from . import utils
from .gpu.decorator import GPU
from .utils import CallableT


gradio_auto_wrap_disabled = False

def disable_gradio_auto_wrap():
    global gradio_auto_wrap_disabled
    gradio_auto_wrap_disabled = True


@overload
def gradio_auto_wrap(task: CallableT) -> CallableT: ...
@overload
def gradio_auto_wrap(task: None) -> None: ...

def gradio_auto_wrap(task: CallableT | None) -> (CallableT | None):
    """
    """
    if gradio_auto_wrap_disabled:
        return task
    if not callable(task):
        return task
    if utils.is_zero_gpu():
        return GPU(task) # type: ignore
    return task
