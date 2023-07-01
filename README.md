# croncaster
[![PyPI version](https://badge.fury.io/py/croncaster.svg)](https://badge.fury.io/py/croncaster)
![PyPI downloads per mounth](https://img.shields.io/pypi/dm/croncaster)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/lightmanLP/croncaster)

Simple tool for periodic events based on timeout. Cron is supposed to be used as runtime base.

## How to use
Just add cron that runs croncaster every `n`.
```crontab
@hourly python3 -m croncaster
```
Then use `n` as one step in config. Pretty simple.
