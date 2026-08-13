# Shell injection via unsanitized report name in git command

**Tool:** `review`
**Severity:** medium
**Category:** review
**Location:** `archive.py:15`

## What's wrong

`archive_report` builds a shell command string with `path` and `branch`, both derived from `name` via `report_path`/`report_branch`, and runs it with `shell=True`. Although `_SAFE.sub` sanitizes the substituted name inside `report_path`/`report_branch`, the surrounding string is still interpolated into a `shell=True` call, so if `_SAFE` does not strip shell metacharacters like spaces, semicolons, backticks, or `$()`, arbitrary shell commands could be injected via `name`.

If `archive_report` is ever called with a `name` sourced from user input (e.g. a CLI arg or report title), this becomes a command injection vector: the attacker controls part of the string passed to `shell=True`.

Build the command as an argument list and drop `shell=True`, or at minimum pass a list to `subprocess.run` for the `git push`/`git add`/`git commit` steps individually:

```python
subprocess.run(["git", "add", path], check=True)
subprocess.run(["git", "commit", "-m", "add report"], check=True)
subprocess.run(["git", "push", "origin", branch], check=True)
```
