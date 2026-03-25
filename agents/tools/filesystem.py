import os
from pathlib import Path

WORKSPACE = Path("/workspace")


def _safe_path(relative: str) -> Path:
    """Resolve path and block traversal outside /workspace."""
    target = (WORKSPACE / relative).resolve()
    if not str(target).startswith(str(WORKSPACE.resolve())):
        raise ValueError(f"Path traversal blocked: {relative}")
    return target


def read_file(path: str) -> str:
    """Read a file from /workspace. Returns file content as string."""
    full = _safe_path(path)
    if not full.exists():
        return f"ERROR: file not found: {path}"
    return full.read_text(encoding="utf-8")


def write_file(path: str, content: str) -> str:
    """Write content to a file in /workspace. Creates parent dirs if needed."""
    full = _safe_path(path)
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")
    return f"OK: written {full.stat().st_size} bytes to {path}"


def list_files(subdir: str = "") -> list:
    """List all files (recursively) in /workspace or a subdirectory."""
    base = _safe_path(subdir) if subdir else WORKSPACE
    if not base.exists():
        return []
    return [str(p.relative_to(WORKSPACE)) for p in base.rglob("*") if p.is_file()]


def delete_file(path: str) -> str:
    """Delete a file from /workspace."""
    full = _safe_path(path)
    if not full.exists():
        return f"ERROR: file not found: {path}"
    full.unlink()
    return f"OK: deleted {path}"
