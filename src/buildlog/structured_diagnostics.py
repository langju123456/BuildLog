"""Opt-in local capture for failed structured model responses."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

FAILED_STRUCTURED_OUTPUT_MAX_BYTES = 32 * 1024
_SAFE_STEP_NAME = re.compile(r"[a-z0-9_-]+")


@dataclass(frozen=True)
class FailedStructuredOutputCapture:
    """Paths for one sensitive, local-only diagnostic capture."""

    response_path: Path
    metadata_path: Path


def capture_failed_structured_output(
    run_dir: Path,
    step_name: str,
    content: str,
    *,
    max_bytes: int = FAILED_STRUCTURED_OUTPUT_MAX_BYTES,
) -> FailedStructuredOutputCapture:
    """Persist one bounded response and non-sensitive capture metadata."""
    if _SAFE_STEP_NAME.fullmatch(step_name) is None:
        raise ValueError("invalid diagnostic step name")
    if max_bytes < 1:
        raise ValueError("max_bytes must be positive")

    raw_bytes = content.encode("utf-8")
    captured_text = raw_bytes[:max_bytes].decode("utf-8", errors="ignore")
    captured_bytes = captured_text.encode("utf-8")
    debug_dir = run_dir / "debug"
    debug_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name == "posix":
        debug_dir.chmod(0o700)

    response_path = debug_dir / f"failed_{step_name}_response.txt"
    metadata_path = debug_dir / f"failed_{step_name}_response.json"
    metadata = {
        "schema_version": "1",
        "artifact_type": "failed_structured_output",
        "step_name": step_name,
        "sensitive": True,
        "encoding": "utf-8",
        "sha256": sha256(raw_bytes).hexdigest(),
        "original_bytes": len(raw_bytes),
        "original_characters": len(content),
        "captured_bytes": len(captured_bytes),
        "captured_characters": len(captured_text),
        "capture_limit_bytes": max_bytes,
        "truncated": len(captured_bytes) < len(raw_bytes),
        "response_file": response_path.name,
    }

    _write_private_file(response_path, captured_bytes)
    _write_private_file(
        metadata_path,
        (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        ),
    )
    return FailedStructuredOutputCapture(response_path, metadata_path)


def _write_private_file(path: Path, content: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as file_handle:
            file_handle.write(content)
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise
    if os.name == "posix":
        path.chmod(0o600)
