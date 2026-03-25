import subprocess
from pathlib import Path

WORKSPACE = "/workspace"
BLOCKED = ["rm -rf /", "sudo", "shutdown", "reboot", "mkfs", "dd if="]


def run_command(cmd: str, timeout: int = 30) -> dict:
    """
    Run a shell command in /workspace.
    Returns {"stdout": str, "stderr": str, "returncode": int}.
    Blocks dangerous commands and enforces a configurable timeout.
    """
    for blocked in BLOCKED:
        if blocked in cmd:
            return {
                "stdout": "",
                "stderr": f"BLOCKED: command contains forbidden pattern '{blocked}'",
                "returncode": 1,
            }

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=WORKSPACE,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"ERROR: command timed out after {timeout}s",
            "returncode": 124,
        }
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": 1}
