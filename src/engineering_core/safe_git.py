# summary: "Runs fixed read-only Git probes with optional locks, fsmonitor, untracked-cache integration, and pathspec interpretation disabled."
# read_when:
#   - "When adding repository identity, revision, status, ancestry, or tracked-blob probes."

from __future__ import annotations

import os
import subprocess
from pathlib import Path


class SafeGitError(ValueError):
    pass


def read_git(repo: Path, *args: str, binary: bool = False, timeout: int = 10) -> str | bytes:
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_LITERAL_PATHSPECS": "1"}
    command = ["git", "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false", "-C", str(repo), *args]
    try:
        output = subprocess.check_output(command, text=not binary, stderr=subprocess.DEVNULL, timeout=timeout, env=env)
        return output if binary else output.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise SafeGitError(f"fixed read-only Git probe failed: {' '.join(args)}") from exc
