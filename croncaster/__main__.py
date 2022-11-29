from pathlib import Path
import sys

from .config import Config
from . import run

if sys.argv == 1:
    Config.from_dump(Path.cwd() / "config.yml")
elif sys.argv == 2:
    Config.from_dump(Path(sys.argv[1]))
else:
    raise AssertionError()
run()
