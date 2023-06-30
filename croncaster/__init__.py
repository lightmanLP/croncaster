from multiprocessing.pool import ThreadPool
import subprocess
import platform
import importlib.metadata

from .config import Config
from .state import State

__version__: str | None
try:
    __version__ = importlib.metadata.version("croncaster")
except importlib.metadata.PackageNotFoundError:
    __version__ = None


def run():
    cfg = Config()
    state = State().get()
    pool = ThreadPool(cfg.thread_pool_size)

    for cast in cfg.tasks:
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
