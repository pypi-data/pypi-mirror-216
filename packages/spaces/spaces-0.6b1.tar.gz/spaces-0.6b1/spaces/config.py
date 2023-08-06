"""
"""
from __future__ import annotations

from pydantic import BaseSettings


class Settings(BaseSettings):

    zero_gpu: bool = False
    zero_device_api_url: str | None = None

    gradio_auto_wrap: bool = False

    class Config:
        env_prefix = 'spaces_'


Config = Settings()


if Config.zero_gpu:
    assert Config.zero_device_api_url is not None, (
        'SPACES_ZERO_DEVICE_API_URL env must be set '
        'on ZeroGPU Spaces (identified by SPACES_ZERO_GPU=true)'
    )
