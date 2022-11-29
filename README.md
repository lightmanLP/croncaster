# croncaster
Simple tool for periodic events based on timeout. Cron is supposed to be used as runtime base.

## How to use
Just add cron that runs croncaster every `n`.
```crontab
@hourly python3 -m croncaster
```
Then use `n` as one step in config. Pretty simple.
