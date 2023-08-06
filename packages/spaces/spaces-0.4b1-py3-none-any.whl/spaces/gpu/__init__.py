"""
"""

from .. import utils
from . import torch

if utils.is_zero_gpu():
    if torch.is_in_bad_fork():
        raise RuntimeError(
            "CUDA has been initialized before importing the `spaces` package"
        )
    torch.patch() # pragma: no cover
