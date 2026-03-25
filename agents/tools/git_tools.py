import subprocess
from pathlib import Path

WORKSPACE = "/workspace"


def _run(cmd: str) -> str:
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=WORKSPACE
    )
    output = result.stdout.strip() or result.stderr.strip()
    return output if output else "(no output)"


def git_init() -> str:
    """Initialize a git repository in /workspace."""
    return _run("git init")


def git_add(path: str = ".") -> str:
    """Stage files for commit. Defaults to staging everything."""
    return _run(f"git add {path}")


def git_commit(message: str) -> str:
    """Create a git commit with the given message."""
    safe_message = message.replace('"', '\\"')
    return _run(f'git commit -m "{safe_message}"')


def git_diff() -> str:
    """Show unstaged and staged diffs."""
    return _run("git diff HEAD")


def git_log(n: int = 5) -> str:
    """Show the last n commits."""
    return _run(f"git log --oneline -n {n}")
