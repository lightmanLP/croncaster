from pathlib import Path
import sys
import os

from .config import Config
from . import run


if len(sys.argv) == 1:
    Config.from_dump(Path.cwd() / "config.yml")
    run()
else:
    for path in tuple(Path(i).resolve() for i in sys.argv[1:]):
        os.chdir(path.parent)
        Config.wipe()
        Config.from_dump(path)
        run()
