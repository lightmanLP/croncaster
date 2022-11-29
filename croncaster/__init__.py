from typing import Final
from multiprocessing.pool import ThreadPool
import subprocess
import platform

from .config import Config
from .state import State

POOL_SIZE: Final[int] = 5


def run():
    state = State().get()
    pool = ThreadPool(POOL_SIZE)

    for cast in Config().tasks:
        if state % cast.step == 0:
            match platform.system().upper():
                case "WINDOWS":
                    command = ("cmd", "/c", cast.command)
                case "LINUX":
                    command = ("bash", "-c", cast.command)
                case _:
                    raise NotImplementedError()
            pool.apply_async(
                subprocess.call,
                (command, )
            )

    if state >= Config().max:
        state = state % Config().max
    state += 1
    State().set(state)

    pool.close()
    pool.join()
