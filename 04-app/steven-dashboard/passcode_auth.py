"""Hardened local passcode helper for Steven Dashboard."""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple

AUTH_FILE_NAME = "passcodes.json"
SESSION_TTL = timedelta(hours=8)


def _auth_path(data_dir: Path) -> Path:
    return data_dir / AUTH_FILE_NAME


def _now() -> datetime:
    return datetime.now()


def _legacy_marker() -> str:
    return "__legacy_nonempty__"


def _read_auth(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def _write_auth(path: Path, data: dict) -> None:
    try:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass


def _hash_secret(secret: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", secret.encode("utf-8"), salt.encode("utf-8"), 200_000).hex()


def setup_passcode(data_dir: Path, passcode: str) -> Tuple[bool, str]:
    if not passcode or not passcode.strip():
        return False, "Passcode cannot be empty."
    passcode = passcode.strip()
    path = _auth_path(data_dir)
    data = _read_auth(path)
    if data.get("mode") == _legacy_marker() and "hash" not in data:
        # migrate old non-empty only auth to hashed auth
        current = data.get("current", "")
        current = current.strip() if isinstance(current, str) else ""
        if not current:
            current = passcode
    else:
        current = passcode

    salt = os.urandom(16).hex()
    phash = _hash_secret(current, salt)
    payload = {
        "mode": "hardened",
        "salt": salt,
        "hash": phash,
        "iterations": 200_000,
        "algorithm": "pbkdf2_hmac_sha256",
        "len": len(current),
        "created": _now().isoformat(),
        "updated": _now().isoformat(),
    }
    _write_auth(path, payload)
    return True, "Passcode saved with hardened hash."


def verify_passcode(data_dir: Path, passcode: str, session_state: dict | None = None) -> Tuple[bool, str]:
    if session_state is None:
        session_state = {}
    path = _auth_path(data_dir)
    data = _read_auth(path)
    if not data:
        return False, "No passcode set yet."

    if not passcode or not passcode.strip():
        return False, "Enter a passcode."

    passcode = passcode.strip()
    mode = data.get("mode")
    if mode == _legacy_marker() and not data.get("hash"):
        stored = data.get("current", "")
        stored = stored.strip() if isinstance(stored, str) else ""
        ok = bool(stored) and hmac.compare_digest(stored, passcode)
        if ok:
            return True, ""
        return False, "Wrong passcode."

    if mode != "hardened" or not data.get("hash") or not data.get("salt"):
        return False, "Passcode file is invalid."

    salt = str(data.get("salt", ""))
    phash = str(data.get("hash", ""))
    candidate = _hash_secret(passcode, salt)
    ok = hmac.compare_digest(phash, candidate)
    if not ok:
        return False, "Wrong passcode."
    session_state["auth_expires"] = int((_now() + SESSION_TTL).timestamp())
    session_state["authenticated"] = True
    return True, ""


def reset_auth(data_dir: Path) -> Tuple[bool, str]:
    path = _auth_path(data_dir)
    if path.exists():
        try:
            path.unlink()
        except Exception:
            pass
    return True, "Auth reset."


def is_session_valid(session_state: dict | None = None) -> bool:
    if not session_state:
        return False
    if not session_state.get("authenticated"):
        return False
    expires = session_state.get("auth_expires")
    if not isinstance(expires, (int, float)):
        return False
    return datetime.fromtimestamp(int(expires)) >= _now()
