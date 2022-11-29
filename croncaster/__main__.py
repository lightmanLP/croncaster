from pathlib import Path
import sys

from .config import Config
from . import run

match len(sys.argv):
    case 1:
        Config.from_dump(Path.cwd() / "config.yml")
    case 2:
        Config.from_dump(Path(sys.argv[1]))
    case _:
        raise AssertionError()
run()
