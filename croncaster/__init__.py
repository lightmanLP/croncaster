from typing import Final
from multiprocessing.pool import ThreadPool
import subprocess

from .config import Config
from .state import State

POOL_SIZE: Final[int] = 5


def run():
    state = State().get()
    pool = ThreadPool(POOL_SIZE)

    for cast in Config().tasks:
        if state % cast.step == 0:
            pool.apply_async(
                subprocess.call,
                (
                    ("cmd", "/c", cast.command),
                )
            )

    if state >= Config().max:
        state = state % Config().max
    state += 1
    State().set(state)

    pool.close()
    pool.join()
