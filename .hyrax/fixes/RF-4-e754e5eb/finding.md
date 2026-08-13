# Shell injection via unsanitized format into os.system

**Tool:** `review`
**Severity:** high
**Category:** review
**Location:** `hooks.py:16`

## What's wrong

`run_hook` builds a shell command string by formatting `build.name` directly into `command_template` and passes it to `os.system`, which executes through `/bin/sh -c`. Any build name containing shell metacharacters (e.g. `; rm -rf /`, backticks, `$(...)`) is executed as part of the shell command.

Since `build.name` typically originates from build metadata (job/project names, which may be attacker- or user-influenced), this is a command injection vector rather than just a theoretical edge case.

Use `subprocess.run` with an argument list (no shell) or at minimum `shlex.quote` the interpolated values before formatting:
```python
import shlex
os.system(command_template.format(name=shlex.quote(build.name), seconds=build.seconds))
```
