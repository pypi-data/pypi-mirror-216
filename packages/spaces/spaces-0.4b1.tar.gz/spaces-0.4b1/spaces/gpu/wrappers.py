"""
"""
from __future__ import annotations

import multiprocessing
import os
import signal
import traceback
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pickle import PicklingError
from threading import Thread
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Generator
from typing import Generic
from typing import TypeVar
from typing_extensions import ParamSpec

import psutil

from ..utils import drop_params
from ..utils import SimpleQueue as Queue
from . import client
from . import torch


Process = multiprocessing.get_context('fork').Process

Arg = tuple[tuple[Any], dict[str, Any]]
Res = TypeVar('Res')
Param = ParamSpec('Param')
NvidiaIndex = int


class Worker(Generic[Res]):
    process: Process
    arg_queue: Queue[Arg]
    res_queue: Queue[Res]
    _sentinel: Thread

    def __init__(
        self,
        target: Callable[[Queue[Arg], Queue[Res], NvidiaIndex, list[int]], None],
        nvidia_index: int,
    ):
        self._sentinel = Thread(target=self._close_on_exit)
        self.arg_queue = Queue()
        self.res_queue = Queue()
        fds = [c.fd for c in psutil.Process().connections()]
        args = self.arg_queue, self.res_queue, nvidia_index, fds
        if TYPE_CHECKING:
            target(*args)
        self.process = Process(
            target=target,
            args=args,
            daemon=True,
        )
        self.process.start()
        self._sentinel.start()

    def _close_on_exit(self):
        self.process.join()
        self.res_queue.close()


def regular_function_wrapper(
    task:
     Callable[Param, Res],
) -> Callable[Param, Res]:

    workers: dict[NvidiaIndex, Worker[list[Res] | Exception]] = {}

    def process_wrapper(*args: Param.args, **kwargs: Param.kwargs) -> Res:

        schedule_response = client.schedule()
        nvidia_index = schedule_response.nvidiaIndex
        release = partial(client.release, nvidia_index=nvidia_index)

        worker = workers.get(nvidia_index)
        if worker is None or not worker.process.is_alive():
            worker = Worker(thread_wrapper, nvidia_index)
            workers[nvidia_index] = worker

        try:
            worker.arg_queue.put((args, kwargs))
        except PicklingError:
            release(fail=True)
            raise

        try:
            res = worker.res_queue.get()
        except EOFError:
            release(fail=True)
            raise RuntimeError("Operation aborted")
        if isinstance(res, Exception):
            release(fail=True)
            raise res
        release()
        return res[0]


    def thread_wrapper(
        arg_queue: Queue[Arg],
        res_queue: Queue[list[Res] | Exception],
        nvidia_index: int,
        fds: list[int],
    ):
        torch.unpatch()
        torch.move(nvidia_index)
        for fd in fds:
            os.close(fd)
        signal.signal(signal.SIGTERM, drop_params(arg_queue.close))
        while True:
            try:
                args, kwargs = arg_queue.get()
            except OSError:
                break
            with ThreadPoolExecutor() as executor:
                future = executor.submit(task, *args, **kwargs)
            try:
                res = [future.result()]
            except Exception as e:
                traceback.print_exc()
                res = e
            try:
                res_queue.put(res)
            except PicklingError as e:
                res_queue.put(e)
    
    return process_wrapper


def generator_function_wrapper(
    task:
     Callable[Param, Generator[Res, None, None]],
) -> Callable[Param, Generator[Res, None, None]]:

    workers: dict[NvidiaIndex, Worker[list[Res] | Exception | None]] = {}

    def process_wrapper(*args: Param.args, **kwargs: Param.kwargs) -> Generator[Res, None, None]:

        schedule_response = client.schedule()
        nvidia_index = schedule_response.nvidiaIndex
        release = partial(client.release, nvidia_index=nvidia_index)

        worker = workers.get(nvidia_index)
        if worker is None or not worker.process.is_alive():
            worker = Worker(thread_wrapper, nvidia_index)
            workers[nvidia_index] = worker

        try:
            worker.arg_queue.put((args, kwargs))
        except PicklingError:
            release(fail=True)
            raise

        yield_queue: Queue[list[Res] | Exception | None] = Queue()
        def fill_yield_queue(worker: Worker[list[Res] | Exception | None]):
            while True:
                try:
                    res = worker.res_queue.get()
                except Exception:
                    release(fail=True)
                    yield_queue.close()
                    return
                if isinstance(res, Exception):
                    release(fail=True)
                    yield_queue.put(res)
                    return
                if res is None:
                    release()
                    yield_queue.put(None)
                    return
                yield_queue.put(res)

        with ThreadPoolExecutor() as e:
            e.submit(fill_yield_queue, worker)
            while True:
                try:
                    res = yield_queue.get()
                except Exception:
                    raise RuntimeError("Operation aborted")
                if isinstance(res, Exception):
                    raise res
                if res is None:
                    break
                yield res[0]


    def thread_wrapper(
        arg_queue: Queue[Arg],
        res_queue: Queue[list[Res] | Exception | None],
        nvidia_index: int,
        fds: list[int],
    ):
        torch.unpatch()
        torch.move(nvidia_index)
        for fd in fds:
            os.close(fd)
        signal.signal(signal.SIGTERM, drop_params(arg_queue.close))
        while True:
            try:
                args, kwargs = arg_queue.get()
            except OSError:
                break
            def iterate():
                gen = task(*args, **kwargs) # type: ignore
                while True:
                    try:
                        res = next(gen)
                    except StopIteration:
                        break
                    except Exception as e:
                        res_queue.put(e)
                        break
                    try:
                        res_queue.put([res])
                    except PicklingError as e:
                        res_queue.put(e)
                        break
                    else:
                        continue
            with ThreadPoolExecutor() as executor:
                executor.submit(iterate)
            res_queue.put(None)

    return process_wrapper
