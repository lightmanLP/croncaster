from pathlib import Path
import sys

from .config import Config
from . import run


if len(sys.argv):
    Config.from_dump(Path.cwd() / "config.yml")
    run()
else:
    for i in sys.argv[1:]:
        Config.wipe()
        Config.from_dump(Path(i))
        run()
